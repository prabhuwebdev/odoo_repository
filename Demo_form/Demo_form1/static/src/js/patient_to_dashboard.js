// ehr_cdss_dashboard.js
import { registry } from "@web/core/registry";
import { Component, onWillStart } from "@odoo/owl";
import { useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";

export class PatientToDashboard extends Component {
    static template = "ehr_cdss.PatientListView";
    setup() {
        this.state = useState({
            patients: []
        });
        this.action=useService('action');

        onWillStart(async () => {
            await this.loadPatients();  // Just call the reusable function
        });
        this.rpc = rpc;

    }

    async loadPatients() {
        try {
            const results = await this.rpc("/ehr_cdss/patient_dashboard",{});
            this.state.patients = results;
        } catch (error) {
            console.error("Failed to load patients:", error);
        }
    }

  goToDashboard(patientId) {
    console.log("Dashboard button clicked", patientId); // test log

    if (!this.action) {
        console.error("Action service is not initialized");
        return;
    }

    this.action.doAction("dashboard.understanding", {
    context: {
        default_patient_id: patientId,
    },
});
}
}


// Register the dashboard as a JS action
registry.category("actions").add("patient_to_dashboard.understanding", PatientToDashboard);
