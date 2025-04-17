/** @odoo-module **/

import { registry } from "@web/core/registry";
import { PivotView } from "@web/views/pivot/pivot_view";
import { PivotModel } from "@web/views/pivot/pivot_model";
import { PivotRenderer } from "@web/views/pivot/pivot_renderer";
import { PivotController } from "@web/views/pivot/pivot_controller";

class CustomPivotController extends PivotController {
    setup() {
        super.setup();
        this.exportCSV = this.exportCSV.bind(this);
    }

    exportCSV() {
        const { exportData } = this.model.getPivotData();
        const csvContent = exportData.map(row => row.join(",")).join("\n");

        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.setAttribute("download", "dealer_purchase_pivot.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    get buttons() {
        return [
            {
                name: "export_csv",
                label: "Export CSV",
                onClick: this.exportCSV,
                className: "btn btn-primary",
            },
        ];
    }
}

registry.category("views").add("dealer_pivot_export", {
    type: "pivot",
    display_name: "Dealer Pivot Export",
    icon: "fa fa-table",
    view: PivotView,
    Model: PivotModel,
    Renderer: PivotRenderer,
    Controller: CustomPivotController,
});
