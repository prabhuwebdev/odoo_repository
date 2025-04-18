from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'school_management.library.book'
    _description = 'Library Book'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Book Title")
    isbn = fields.Char(string="ISBN")
    author = fields.Char(string="Author")
    publisher = fields.Char(string="Publisher")
    edition = fields.Char(string="Edition")
    category_id = fields.Many2one('school_management.library.category', string="Category")
    subject_id = fields.Many2one('school_management.subject', string="Subject")
    price = fields.Float(string="Price", default=0.0)
    pages = fields.Integer(string="Pages", default=0)
    publication_date = fields.Date(string="Publication Date")
    location = fields.Char(string="Location")
    barcode = fields.Char(string="Barcode")
    quantity = fields.Integer(string="Quantity", default=1)
    available_quantity = fields.Integer(string="Available Quantity", compute="_compute_available_quantity", store=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('issued', 'Issued'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
        ('discarded', 'Discarded')],
        default='available', string="Status"
    )
    procurement_date = fields.Date(string="Procurement Date")
    notes = fields.Text(string="Notes")

    @api.depends('quantity')
    def _compute_available_quantity(self):
        for rec in self:
            # Placeholder logic, integrate with issued tracking
            rec.available_quantity = rec.quantity

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.author:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.author}"
