from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'
    _order = 'expected_price desc'  # Sort by expected price in descending order

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(string="Availability Date", default=fields.Date.today)

    expected_price = fields.Float(string="Expected Price", required=True)  # Expected selling price
    selling_price = fields.Float(string="Selling Price", readonly=True)  # Final selling price
    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price", store=True)  # Highest received offer

    bedrooms = fields.Integer(string="Number of Bedrooms", default=1)
    living_area = fields.Integer(string="Living Area (m²)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has Garage?")
    garden = fields.Boolean(string="Has Garden?")
    garden_area = fields.Integer(string="Garden Area (m²)")

    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Garden Orientation")

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string="Status", default="new", required=True)

    offer_ids = fields.One2many('real.estate.offer', 'property_id', string="Purchase Offers")  # List of purchase offers
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area", store=True)

    # Relationship with RealEstatePropertyType
    property_type_id = fields.Many2one('real.estate.property.type', string="Property Type")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    # @api.constrains('selling_price')
    # def _check_selling_price(self):
    #     for record in self:
    #         if record.selling_price and record.selling_price > record.expected_price:
    #             raise ValidationError("Selling price cannot be higher than the expected price!")
            
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        """Compute the highest offer price from the list of received offers."""
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.constrains('selling_price')
    def _check_selling_price(self):
        """Ensure the selling price is not lower than 90% of the expected price."""
        for record in self:
            if record.selling_price and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price!")

    def action_sold(self):
        """Mark the property as 'Sold'. Ensure that a canceled property cannot be sold."""
        for record in self:
            if record.state == 'canceled':
                raise ValidationError("Cannot sell a property that has been canceled!")
            record.state = 'sold'
            record.selling_price = record.best_price

    def action_cancel(self):
        """Mark the property as 'Canceled'."""
        for record in self:
            record.state = 'canceled'

