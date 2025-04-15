from odoo import http
from odoo.http import request


class DemoFormController(http.Controller):
    @http.route("/demo_form/get_demo", type="json")
    def get_demo_date(self, your_id=False):
        if not your_id or not your_id.isdigit():
            return {"your_name": "", "your_age": "", "your_country": ""}

        your_data = request.env["demo.form"].browse(int(your_id))
        if not your_data.exists():
            return {"your_name": "", "your_age": "", "your_country": ""}

        return your_data.get_demo()

    # @http.route("/demo_form/store_data",type="json",auth="public")
    # def save_demo_data(self,**kwargs):
    #     request.env["demo.form"].create(kwargs)
    #     return {"success":True}

    @http.route("/demo_form/store_data", type="json", auth="public")
    def save_demo_data(self, **kwargs):
        # Ensure 'your_id' is a valid Many2many format
        if "your_id" in kwargs and isinstance(kwargs["your_id"], int):
            kwargs["your_id"] = [(6, 0, [kwargs["your_id"]])]

        request.env["demo.form"].create(kwargs)
        return {"success": True}


    @http.route("/demo_form/partner_data",type="json",auth="public")
    def get_partner_data(self):
        partner=request.env["res.partner"].sudo().search([],limit=5)
        return [{"id":p.id,"name":p.name} for p in partner]


class Disease_prediction(http.Controller):

    @http.route("/disease_prediction/person",type="json",auth="public")
    def Get_people(self):

        people=[
            {"name":"prabhu","age":22},
            {"name":"rahul", "age": 24},
            {"name":"gokul", "age":26}
        ]
        return people