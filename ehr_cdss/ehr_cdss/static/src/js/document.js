/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class DocumentWorkspace extends Component {
    setup() {
        this.state = useState({
            documents: [],
            title: "All Documents",
        });

        this.docTypes = [
            ['soap_note', 'SOAP Note'],
            ['progress_note', 'Progress Note'],
            ['initial_assessment', 'Initial Assessment'],
            ['treatment_plan', 'Treatment Plan'],
            ['safety_plan', 'Safety Plan'],
            ['discharge_summary', 'Discharge Summary'],
            ['clinical_review', 'Clinical Review Update'],
            ['referral', 'Referral'],
            ['consent_form', 'Consent Form'],
            ['lab_result', 'Lab Result'],
            ['imaging_result', 'Imaging Result'],
            ['prescription', 'Prescription'],
            ['insurance', 'Insurance Document'],
            ['correspondence', 'Correspondence'],
            ['other', 'Other'],
        ];

        onWillStart(() => this.loadDocuments());
    }

    async loadDocuments(type = null) {
        const domain = type && type !== 'all' ? [['document_type', '=', type]] : [];
        const documents = await this.env.services.orm.searchRead('ehr_cdss.document', domain, ['name', 'patient_id','document_type', 'document_date']);
        this.state.documents = documents;
        this.state.title = type === 'all' || !type ? 'All Documents' : this.docTypes.find(d => d[0] === type)?.[1] || '';
    }

    selectType(type) {
        this.loadDocuments(type);
    }

    openDocument(id) {
        this.env.services.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'ehr_cdss.document',
            res_id: id,
            views: [[false, 'form']],
            target: 'current',
        });
    }
}

DocumentWorkspace.template = 'ehr_cdss.DocumentWorkspace';
registry.category('actions').add('ehr_cdss.document_workspace', DocumentWorkspace);
