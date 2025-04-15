odoo.define('ehr_cdss.change_button_color', function (require) {
    'use strict';
    
    var $ = require('jquery');
    
    $(document).ready(function () {
        // Attach click event to all buttons in the header with 'oe_highlight' class
        $('header button').on('click', function () {
            // Remove the 'clicked-button' class from all buttons
            $('header button').removeClass('clicked-button');
            
            // Add the 'clicked-button' class to the clicked button
            $(this).addClass('clicked-button');
        });
    });
});
