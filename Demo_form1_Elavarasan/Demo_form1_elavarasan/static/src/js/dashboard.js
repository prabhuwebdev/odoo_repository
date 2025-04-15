/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class Dashboard extends Component {
    static template = "dashboard.container";

    setup() {
        this.state = useState({
            Name: "Prabhu",
            Age: "22",
            Gender: "male",
            DOB: "01/01/2002",
            Contact: "9876543210",
            Smoking: "no",
            Alcohol: "Occasionally",
            Exercise: "Regular"
        });

        const action = useService("action");
        this.action = action;
        this.rpc = rpc;
    }

    // Open the New Record Form
    async openNewRecordForm() {
        await this.action.doAction("Demo_form1.new_record_form");
    }

    // Open the Edit Form with data pre-filled
    async editRecord(recordId) {
        await this.action.doAction({
            type: "ir.actions.client",
            tag: "new_record.understanding",  // Replace with your actual form component tag
            name: "Edit Record",
            context: {
                record_id: recordId,  // Pass the record ID to the form
            },
        });
    }
}

// Register the dashboard as a JS action
registry.category("actions").add("dashboard.understanding", Dashboard);
