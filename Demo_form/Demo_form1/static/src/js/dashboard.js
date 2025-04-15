import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class Dashboard extends Component {
    static template = "dashboard.container";

    setup() {
        this.state = useState({
            name: "",
            age: "",
            gender: "",
            dob: "",
            contact: "",
            smoking: "no",
            alcohol: "no",
            exercise: "always",
            pat_id: 1,
            selected_tab: "medical", //default tab when the page loads this only available first
            add_more: "false",
            add_surgical_form: "false",
            new_image_record:"false"
        });

        onWillStart(async () => {
            const patientId = this.env.action?.context?.default_patient_id;
            console.log("successfully fetched the patient id",patientId)

            if (patientId) {
                await this.fetchPatientData(patientId);
            }
        });

        this.rpc = rpc;
    }

    async fetchPatientData(patientId){
        try{
            const result = await this.rpc('/ehr_cdss/get_patient', {
                patient_id: patientId,
            });

            this.state.name = result.name;
            this.state.age = result.age;
            this.state.gender = result.gender;
            this.state.dob = result.birth_date;
            this.state.contact = result.phone_primary;
//            this.state.pat_id = result.id;

        }catch(error){
            console.log("error arised when getting data from patient list to dashboard",error)
        }
    }
}


registry.category("actions").add("dashboard.understanding", Dashboard);

