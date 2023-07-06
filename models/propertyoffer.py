from odoo import fields, models

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This will contain the offers of the Property!"
    # _rec_name = "partner_id"
    
    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], compute="_status_check")
    partner_id = fields.Many2one("res.partner", required="True")
    property_id = fields.Many2one("estate.property", required="True")