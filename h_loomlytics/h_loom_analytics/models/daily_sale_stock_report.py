from  odoo import fields,models
class DailySalesStockReport(models.Model):
    _name = 'daily.sales.stock.report'
    _description = 'Daily Sales Stock Report'

    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    product_group = fields.Char(string='Product Group', required=True)
    floor = fields.Char(string='Floor')
    section = fields.Char(string='Section')
    days_0_30 = fields.Float(string='0-30 Days')
    days_31_60 = fields.Float(string='31-60 Days')
    days_61_90 = fields.Float(string='60-90 Days')
    days_91_180 = fields.Float(string='90-180 Days')
    days_181_360 = fields.Float(string='180-360 Days')
    sales = fields.Float(string='Sales')

    last_year_sales = fields.Float(string='Last Year Sales')
    stock_days = fields.Float(string='Stock Days')