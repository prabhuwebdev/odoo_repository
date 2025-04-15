import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class PastMedications extends Component {
    static template = "past_medications.container";

    setup() {
        this.state = useState({


        });

        onWillStart(async () => {
            // Fetch data here if needed
        });

        this.rpc = rpc;
    }




}

// Register the dashboard as a JS action
registry.category("actions").add("past_medications.understanding", PastMedications);
