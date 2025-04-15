odoo.define('ehr_cdss.open_in_new_tab', function (require) {
    'use strict';
    
    var ActionManager = require('web.ActionManager');
    var core = require('web.core');
    
    ActionManager.include({
        _executeAction: function (action) {
            if (action.flags && action.flags.form && action.flags.form.action === 'open_in_new_tab') {
                // Construct the URL for the form view
                var url = '/web#id=' + action.res_id + '&view_type=form&model=' + action.res_model;
                window.open(url, '_blank'); // Open the URL in a new tab
                return $.Deferred().resolve();
            }
            return this._super(action);
        },
    });
});
