//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { Component, useState, onWillStart } from "@odoo/owl";
//import { rpc } from "@web/core/network/rpc";
//
//export class NewRecord extends Component {
//    static template = "new_record.container";
//
//    setup() {
//        this.state = useState({
//            Name:"",
//            Age:"",
//            Gender:"",
//            DOB:"",
//            Contact:"",
//            Smoking:"",
//            Alcohol:"",
//            Exercise:""
//
//        });
//
//        onWillStart(async () => {
//            // Fetch data here if needed
//        });
//
//        this.rpc = rpc;
//    }
//
//
//
//
//}
//
//// Register the dashboard as a JS action
//registry.category("actions").add("new_record.understanding", NewRecord);



import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class NewRecord extends Component {
    static template = "new_record.container";

    setup() {
        this.state = useState({
            name: '',
            image_type: '',
            body_region: '',
            study_date: '',
            provider: '',
            physician: '',
            contrast_used: false,
            run_ai: false,
            record_id: null, // To track if this is a new or existing record
        });

        this.notification = useService("notification");

        // Check if a record ID was passed in the context (for editing)
        onWillStart(async () => {
            if (this.props.context && this.props.context.record_id) {
                const recordId = this.props.context.record_id;
                await this.loadRecordData(recordId);
            }
        });
    }

    async loadRecordData(recordId) {
        try {
            const result = await rpc("/web/dataset/call_kw", {
                model: "patient.image.record",
                method: "read",
                args: [[recordId]],
                kwargs: { fields: ['name', 'image_type', 'body_region', 'study_date', 'provider', 'physician', 'contrast_used', 'run_ai'] },
            });

            if (result && result.length > 0) {
                const record = result[0];
                this.state.name = record.name;
                this.state.image_type = record.image_type;
                this.state.body_region = record.body_region;
                this.state.study_date = record.study_date;
                this.state.provider = record.provider;
                this.state.physician = record.physician;
                this.state.contrast_used = record.contrast_used;
                this.state.run_ai = record.run_ai;
                this.state.record_id = recordId; // Store record_id for updating later
            }
        } catch (error) {
            console.error("Failed to load record:", error);
            this.notification.add("Failed to load record data.", { type: "danger" });
        }
    }

    async saveRecord() {
        console.log("Form data:", this.state);
        this.state.saving = true;

        try {
            const payload = {
                name: this.state.name,
                image_type: this.state.image_type,
                body_region: this.state.body_region,
                study_date: this.state.study_date,
                provider: this.state.provider,
                physician: this.state.physician,
                contrast_used: this.state.contrast_used,
                run_ai: this.state.run_ai,
            };

            let result;
            if (this.state.record_id) {
                // Update existing record
                result = await rpc("/web/dataset/call_kw", {
                    model: "patient.image.record",
                    method: "write",
                    args: [[this.state.record_id], payload],
                    kwargs: {},
                });
                this.notification.add("Record updated successfully!", { type: "success" });
            } else {
                // Create new record
                result = await rpc("/web/dataset/call_kw", {
                    model: "patient.image.record",
                    method: "create",
                    args: [payload],
                    kwargs: {},
                });
                this.notification.add("Record saved successfully!", { type: "success" });
            }

            // Clear form after save (optional)
            Object.keys(this.state).forEach(key => {
                this.state[key] = typeof this.state[key] === "boolean" ? false : "";
            });
            this.state.record_id = null; // Reset the record_id after saving

        } catch (error) {
            console.error("Failed to save record:", error);
            this.notification.add("Failed to save record.", { type: "danger" });
        } finally {
            this.state.saving = false;
        }
    }
}

registry.category("actions").add("new_record.understanding", NewRecord);

