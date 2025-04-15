import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class DemoLazyForm extends Component {
    static template = "demo_form.container";

    setup() {
        console.log("Employee Lazy Form initialized!");
        this.state = useState({
            activeForm: 'info',
            isLoading: false,
            loadedForms: {
                info: false,
                address: false,
                medical_history: false
            },
            employee: {
                name: '',
                age: '',
                yourId: '',
                country: '',
                dob: '',
            },
            res_data:[],
            partner_ids:[],
        });

        this.notification = useService("notification");
        this.rpc = rpc;
        console.log("notification:");

        onWillStart(async () => {
            // Only pre-load the info form data initially
            await this.loadInfoData();
            this.state.loadedForms.info = true;
            // to get the manytomany data

            await this.partner_data()
        });
    }

    async loadInfoData() {
        if (this.state.loadedForms.medical_history) return;

        this.state.isLoading = true;

        try {
            const result = await rpc("/demo_form/get_demo", { your_id: this.state.employee.yourId });

            if (result) {
                this.state.employee.name = result.your_name || "";
                this.state.employee.age = result.your_age || "";
                this.state.employee.country = result.your_country || "";
            } else {
                console.log("Invalid response received:", result);
            }
        } catch (error) {
            console.error("Error loading medical history:", error);
        } finally {
            this.state.isLoading = false;
        }
    }

    async storeDemoData() {
        this.state.isLoading = true;

        try {
            const result = await rpc("/demo_form/store_data", {
                name: this.state.employee.name,
                age: this.state.employee.age,
                your_id: this.state.employee.yourId ? [[6, 0, [this.state.employee.yourId]]] : [], // FIXED,
                country: this.state.employee.country,
                dob: this.state.employee.dob,
            });

            if (result.success) {
                this.notification.add("Employee data saved successfully!", { type: "success" });
            } else {
                this.notification.add("Failed to save employee data.", { type: "danger" });
            }
        } catch (error) {
            console.error("Error occurred while saving data:", error);
            this.notification.add("Error occurred while saving data.", { type: "danger" });
        } finally {
            this.state.isLoading = false;
        }
    }

    async partner_data() {
    try {
        const result = await this.rpc("/demo_form/partner_data");
        this.state.res_data = result;
    } catch (error) {
        console.error("Error fetching partner data:", error);
    }
}

//    async partner_data(){
//
//    result=await.rpc("/demo_form/partner_data")
//    this.state.res_data=result
//    }

    onInputChange(field, event) {
        this.state.employee[field] = event.target.value;
    }





    async switchForm(formName) {
        if (formName === this.state.activeForm) {
            return;
        }

        this.state.activeForm = formName;

        if (formName === 'info') {
            await this.loadInfoData();
        } else if (formName === 'address') {
            await this.loadAddressData();
        } else if (formName === 'medical_history') {
            await this.loadMedicalHistoryData();
        }
    }
}

registry.category("actions").add("demo_form.form_understanding", DemoLazyForm);











