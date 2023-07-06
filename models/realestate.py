from odoo import fields, models, api, exceptions


class RealEstate(models.Model):

    _name = "estate.property"
    _description = "Test Model"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    # date_availability = fields.Date(string="Available from" domain="[('date_availability','>', 27/06/2023)]")
    date_availability = fields.Date(string="Available from", domain=[
                                    ('date_availability', '>', '2023-06-27')])

    expected_price = fields.Float(string="Expected Price", required=True)
    best_offer = fields.Float(string="Best Offer")
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Orientation")

    # many2one field
    buyer_id = fields.Many2one("res.partner",  string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")

    # many2many field
    tags_id = fields.Many2many("estate.property.tag", string="Tags")

    # one2many field
    offer_id = fields.One2many(
        "estate.property.offer", "property_id", string="Property Offer")

    # compute method
    total_area = fields.Integer(compute="_total_area")
    best_price = fields.Integer(compute="_best_price")

    # compute method
    @api.depends("living_area", "garden_area")
    def _total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area

    @api.depends('offer_id.price')
    def _best_price(self):
        for property in self:
            prices = property.offer_id.mapped('price')
            if prices:
                property.best_price = max(prices)
            else:
                property.best_price = 0.0

    # on change method
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.orientation = 'north'
        else:
            self.garden_area = 0
            self.orientation = False

    # search
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args += [('date_availability', '>=', '2022-06-27')]
        return super(RealEstate, self).search(args, offset, limit, order, count)

    # unlink method
    def unlink(self):
        for record in self:
            record.offer_id.unlink()
        return super(RealEstate, self).unlink()

    # write method

    def write(self, values):
        if 'date_availability' in values:
            raise UserWarning("PLZ Correct It")
        pass
        return super(RealEstate, self).write(values)

    @api.model
    def get_property_by_postcode(self, postcode):
        properties = self.search([('postcode', '=', postcode)])
        return properties

    