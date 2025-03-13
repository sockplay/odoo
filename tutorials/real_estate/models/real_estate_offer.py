from odoo import models, fields, api

class RealEstateOffer(models.Model):
    _name = 'real.estate.offer'
    _description = 'Real Estate Property Offer'

    property_id = fields.Many2one('real.estate.property', string="Property", required=True)  # Property
    price = fields.Float(string="Offer Price", required=True)  # Offer price

    @api.model_create_multi
    def create(self, vals_list):
        """When creating a new offer, update the property status to 'offer_received'."""
        records = super().create(vals_list)
        for record in records:
            record.property_id.state = 'offer_received'
        return records
