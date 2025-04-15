


import { Component,onWillStart,onWillUpdateProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { renderToElement } from "@web/core/utils/render";

export class CustomColorWidget extends Component {
    setup() {
        this.totalColors = [1, 2, 3, 4, 5, 6];
//        onWillStart(()=>{
//        this.loadCategInformation()
//        })
//        onWillUpdateProps(()=>{
//        this.loadCategInformation()
//        })
        super.setup();
    }

    clickPill(value) {
        this.props.record.update({ [this.props.name]: value });
    }

    categoryInfo(ev) {
        var target = ev.target;  // ✅ Use `target` instead of `$target`
        var data = target.getAttribute("data-value");  // ✅ Correctly fetch data-value

        // ✅ Find the closest parent that contains `.CategInformationPanel`
        var panel = target.closest("div").querySelector(".CategInformationPanel");

        if (panel) {  // ✅ Ensure the panel exists before modifying innerHTML
            panel.innerHTML = renderToElement(
                "CustomColorWidget.CategInformation",
                {
                    value: data, // ✅ Use `data` directly
                    widget: this,
                }
            ).outerHTML; // ✅ Correctly set HTML content
        } else {
            console.warn("CategInformationPanel not found");  // ✅ Debugging message
        }
    }
//    async loadCategInformation(){
//        var self=this;
//        var categInfo={};
//        var modelRef=self.env.model.root.resModel
//        var domain=[];
//        var field=["category"]
//        var groupby=["category"]
//        const categInfoPromise=self.env.services.orm.readGroup(modelRef,domain,field,groupby)
//    }
//    const categInfoPromise.map((val)=>{
//        self.categInfo[val.category]= val.category_count
//    })
}

CustomColorWidget.template = "CustomColorWidget.CustomColorField";
CustomColorWidget.supportedTypes = ["Integer"];
registry.category("fields").add("category_color", { component: CustomColorWidget });

