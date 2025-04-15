odoo.define('ehr.cdss.kanban_buttons', function (require) {
    "use strict";
    const KanbanController = require('web.KanbanController');

    KanbanController.include({
        renderButtons() {
            this._super(...arguments);
            const self = this;
            // Attach custom actions
            this.$el.on('click', '[data-action]', function () {
                const actionName = $(this).data('action');
                self._rpc({
                    model: self.modelName,
                    method: actionName,
                    args: [[]], // Or pass active_ids
                }).then(() => {
                    self.reload();
                });
            });
        },
    });
});
