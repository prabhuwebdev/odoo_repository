from odoo import tools
from odoo import fields, models,api


class SalePivotReport(models.Model):
    _name = "report.sale.aging"
    _auto = False

    section=fields.Char(string="Section")
    aging_days=fields.Char(string="Month-Year")
    sale_value=fields.Float(string="Sale Value")

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_sale_aging')
        self._cr.execute('''
         CREATE OR REPLACE VIEW report_sale_aging AS
        SELECT row_number() OVER() as id,
        a.section as section,
        CASE
        WHEN a.year = 2024 AND a.month = 1 THEN 'Jan-2024'
        WHEN a.year = 2024 AND a.month = 2 THEN 'Feb-2024'
        WHEN a.year = 2024 AND a.month = 3 THEN 'Mar-2024'
        WHEN a.year = 2024 AND a.month = 4 THEN 'Apr-2024'
        WHEN a.year = 2024 AND a.month = 5 THEN 'May-2024'
        WHEN a.year = 2024 AND a.month = 6 THEN 'Jun-2024'
        WHEN a.year = 2024 AND a.month = 7 THEN 'July-2024'
        WHEN a.year = 2024 AND a.month = 8 THEN 'Aug-2024'
        WHEN a.year = 2024 AND a.month = 9 THEN 'Sep-2024'
        END AS aging_days,
        SUM(a.salqty * a.salrate) as sale_value
        FROM loomlytics_analytics as a
        GROUP BY a.section,aging_days  
        ''')