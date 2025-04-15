from odoo import http
from odoo.http import request

class FetchingPatientRecords(http.Controller):
    @http.route("/patient_record", type="json",auth="public")
    def get_patient(self,**kwargs):
        id=kwargs.get("Pat_Id")
        if not id:
            return {"error":"cannot get the id"}
        patients=request.env["patient.record"].sudo().search([('id', "=",int(id))])

        if not patients:
            return {"error":"Cannot get the information for the specific patient"}

        return patients.records()

