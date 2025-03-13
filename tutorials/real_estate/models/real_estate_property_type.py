from odoo import models, fields

class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many('real.estate.property', 'property_type_id', string="Properties")
