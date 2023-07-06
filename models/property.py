from odoo import fields, models

class Property(models.Model):
        _name = 'property.type'
        _description = "Test Model1"
        
        name = fields.Char(string="Name", require=True)
        
        