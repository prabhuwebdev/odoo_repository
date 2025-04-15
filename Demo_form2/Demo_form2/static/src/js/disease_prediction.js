import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";




export class Disease extends Component {
static template = "disease.container";
    setup() {
        this.state = useState({
            people: [],
            selectedAge: "",
        });

        // Fetch data when component loads
        onWillStart(async () => {
            await this.getAge()
        });
        this.rpc=rpc
    }

    async getAge(){
        try{
            var val= await this.rpc("/disease_prediction/person",{})
            if(Array.isArray(val)){
                Object.assign(this.state, {people:val})
            }
        }catch(error){
            console.log("there is an error arised to store the data")
        }
    }

    async selectedName(evert){
        var Name=evert.target.value
        var Person=this.state.people.find(p=> p.name === Name)
        this.state.selectedAge= Person ? Person.age : " "
    }

}

registry.category("actions").add("Disease_prediction.understanding", Disease);
