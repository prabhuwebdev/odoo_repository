from odoo import http
from odoo.http import request


class DemoFormController(http.Controller):
    @http.route("/demo_form/get_demo",type="json")
    def get_demo_date(self,your_id=False):
        if your_id:
            return {"your_name":"","your_age":"","your_country":""}

        your_data=request.env["demo.form"].browse(int(your_id))
        if not your_data.existe():
            return {"your_name":"","your_age":"","your_country":""}
        return your_data.get_demo()