from odoo import models, fields, api
from datetime import datetime, date, timedelta

class ReportDailySaleStock(models.Model):
    _name = 'report.daily_sale_stock'
    _description = 'Daily Sales and Stock'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, name'

    # Existing fields
    name = fields.Char(string='Name', compute='_compute_name', store=True)  # Add store=True
    date = fields.Date(string='Date', required=True, tracking=True)
    state = fields.Selection([
        ('not_viewed', 'Not Viewed'),
        ('viewed', 'Viewed'),
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ], string='Status', default='not_viewed', group_expand="_read_group_stage_ids")
    
    # New fields for sales and stock data
    total_sales = fields.Float(string='Total Sales', compute='_compute_total_sales_stock', store=True)
    total_stock = fields.Float(string='Total Stock', compute='_compute_total_sales_stock', store=True)
    last_year_sales = fields.Float(string='Last Year Sales', compute='_compute_total_sales_stock', store=True)
    daily_sales_stock_ids = fields.One2many('daily.sales.stock.report', 'daily_sale_stock_id', string='Daily Sales Stock Reports')
    
    @api.model
    def _read_group_stage_ids(self,stages,domain):
        return [key for key, _ in self._fields['state'].selection]
    @api.depends('date')
    def _compute_name(self):
        """
        Compute the name based on the date.
        """
        for record in self:
            if record.date:
                record.name = f"Sales and Stock - {record.date.strftime('%Y-%m-%d')}"
            else:
                record.name = "Sales and Stock - No Date"


    @api.depends('daily_sales_stock_ids.sales', 'daily_sales_stock_ids.stock_days', 'daily_sales_stock_ids.last_year_sales')
    def _compute_total_sales_stock(self):
        """
        Compute total sales, total stock, and last year sales.
        """
        for record in self:
            record.total_sales = sum(record.daily_sales_stock_ids.mapped('sales'))
            record.total_stock = sum(record.daily_sales_stock_ids.mapped('stock_days'))
            record.last_year_sales = sum(record.daily_sales_stock_ids.mapped('last_year_sales'))
            
    
    @api.onchange('date')
    def _onchange_date(self):
        """
        Triggered when the date is changed.
        Compare the selected date with the daily.sales.stock.report model and filter data.
        """
        for record in self:
            if record.date:
                # Filter records from daily.sales.stock.report based on the selected date
                filtered_records = self.env['daily.sales.stock.report'].search([('date', '=', record.date)])
                record.daily_sales_stock_ids = filtered_records
            else:
                record.daily_sales_stock_ids = False
    
    def write(self, vals):
        # Custom logic when the state is updated
        if 'state' in vals:
            new_state = vals['state']
            if new_state == 'viewed':
                # Add custom logic for the "viewed" state
                print(f"Record {self.name} is moved to viewed state.")
            elif new_state == 'pending':
                # Add custom logic for the "Pending" state
                print(f"Record {self.name} is moved to Pending state.")
            elif new_state == 'completed':
                # Add custom logic for the "Completed" state
                print(f"Record {self.name} is moved to Completed state.")
            # Add more conditions for other states if needed

        # Call the super method to perform the actual write operation
        return super(ReportDailySaleStock, self).write(vals)