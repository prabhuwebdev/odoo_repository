import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class EmployeeLazyForm extends Component {
    static template = "embedded_forms.EmbeddedFormContainer";
    
    setup() {
        console.log("Employee Lazy Form initialized!");
        this.state = useState({
            activeForm: 'info',
            isLoading: false,
            loadedForms: {
                info: false,
                address: false,
                medical_history:false
            },
            employee: {
                id: this.props.employeeId || false,
                firstName: '',
                lastName: '',
                city: '',
                pin: '',
            },
            medicalHistories:[],
            comorbidity:[],
            curr_meditation:[],
            past_medication:[],
            chemotherapy:[],
            supportive_med:[],
            otc_med:[],
            drug:[],
            immune:[],
        });

        this.notification = useService("notification");
        this.rpc = rpc
        // const rpc = useService("rpc");
        console.log("notification:")
        onWillStart(async () => {
            // Only pre-load the info form data initially
            await this.loadInfoData();
            this.state.loadedForms.info = true;
        });
        this.fetchComorbidities()
        this.fetchCurrentMeditation()
        this.fetchChemotherapyDrugs()
        this.fetchSupportiveMedications()
        this.fetchOtcMedications()
        this.fetchDrugAllergies()
        this.fetchImmunizations()
    }


    async fetchComorbidities(){
        try{
            var res= await this.rpc('/medical/comorbidities',{})
            this.state.comorbidity=res
        }catch(error){
            console.log("cannot found value",error)
        }
    }
    async fetchCurrentMeditation(){
        try{
            var value=await this.rpc("/medical/meditation",{})
            this.state.curr_meditation=value

        }catch(error){
            console.log("cannot found the value",error)
        }
    }

    async fetchPastMedication(){
        try{
            var value=await this.rpc("/medical/past_medication",{})
            this.state.past_medication=value

        }catch(error){
            console.log("cannot found the value",error)
        }
    }


    async fetchChemotherapyDrugs(){
        try{
            var value=await this.rpc("/medicat/chemotherapy_drugs",{})
            this.state.chemotherapy=value
        }catch(error){
            console.log("there is an error to get the chemotherapy data",error)
        }

    }

    async fetchSupportiveMedications(){
        try{
            var value=await this.rpc("/medicat/supportive_medications",{})
            this.state.supportive_med=value
        }catch(error){
            console.log("there is an error to get the supportive medications data",error)
        }
    }

    async fetchOtcMedications(){
        try{
            var val=await this.rpc("/medicat/otc_medications")
            this.state.otc_med=val
        }catch(error){
            console.log("there is an error to get the otc medications data",error)
        }
    }


    async fetchDrugAllergies(){
        try{
            var val=await this.rpc("/medicat/drug_allergies")
            this.state.drug=val
        }catch(error){
            console.log("there is an error to get the drug allergies data",error)
        }
    }


    async fetchImmunizations(){
        try{
            var val=await this.rpc("/medicat/immunization")
            this.status.immune=val
        }catch(error){
            console.log("there is an error to get the immunization data",error)
        }
    }




    async loadInfoData() {
        if (this.state.loadedForms.info) {
            return; // Already loaded
        }
        
        this.state.isLoading = true;
        try {
            const result = await rpc("/employee_lazy/get_info", {
                employee_id: this.state.employee.id,
            });
            
            this.state.employee.firstName = result.first_name;
            this.state.employee.lastName = result.last_name;
            this.state.loadedForms.info = true;
        } catch (error) {
			
            //this.notification.add(this.env._t("Error loading employee info"), {
            //    type: "danger",
            //});
			
            console.error("Error loading info data:", error);
        } finally {
            this.state.isLoading = false;
        }
    }

    async loadAddressData() {
        if (this.state.loadedForms.address) {
            return; // Already loaded
        }
        
        this.state.isLoading = true;
        try {
            const result = await rpc("/employee_lazy/get_address", {
                employee_id: this.state.employee.id,
            });
            
            this.state.employee.city = result.city;
            this.state.employee.pin = result.pin;
            this.state.loadedForms.address = true;
        } catch (error) {
            //this.notification.add(this.env._t("Error loading employee address"), {
            //    type: "danger",
            // });
            console.error("Error loading address data:", error);
        } finally {
            this.state.isLoading = false;
        }
    }

    async loadMedicalHistoryData(){
        if(this.state.loadedForms.medical_history) return

        this.state.isLoading=true

        try{
            const result=await rpc('/medical_history/get_all',{})
            const selectionFieldsResult=await rpc('/medical_history/get_selection_fields',{})
            if (Array.isArray(result)){
                this.state.medicalHistories=result
                this.state.loadedForms.medical_history=true
            }else{
                console.log("invalid response got:",result)

            }if(selectionFieldsResult){
                this.state.selectionFields=selectionFieldsResult

            }
        }catch(error){
            console.error("Error loading medical history:", error)
        }finally{
            this.state.isLoading=false
        }

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
        } else if (formName === 'medical_history'){
            await this.loadMedicalHistoryData();
        }
    }
    
    async saveData() {
        const formType = this.state.activeForm;
        console.log("formtypes: ",formType)
        this.state.isLoading = true;
        
        try {
            const formData = formType === 'info' 
                ? {
                    first_name: this.state.employee.firstName,
                    last_name: this.state.employee.lastName,
                }
                : {
                    city: this.state.employee.city,
                    pin: this.state.employee.pin,
                };
                
            const result = await rpc("/employee_lazy/save_data", {
                employee_id: this.state.employee.id,
                form_type: formType,
                data: formData,
            });
            
            if (result.success) {
                if (!this.state.employee.id) {
                    this.state.employee.id = result.employee_id;
                }
                console.log("success")
                //this.notification.add(this.env._t("Data saved successfully"), {
                //    type: "success",
                //});
            }
        } catch (error) {
            //console.log("error",this.env._t,this.env)
            //this.notification.add(this.env._t("Error saving data"), {
            //    type: "danger",
            //});
            console.error("Error saving data:", error);
        } finally {
            this.state.isLoading = false;
        }
    }
    
    onInputChange(field, event) {
        this.state.employee[field] = event.target.value;
    }
    onInputChangeForMany(field,event){
        this.state[field]=event.target.value;
    }
}

EmployeeLazyForm.props = {
    employeeId: { type: Number, optional: true },
};


registry.category("actions").add("embedded_forms.employee_lazy_form", EmployeeLazyForm);




























