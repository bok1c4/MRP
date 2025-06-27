from odoo import models, fields


class DeskMaterialLine(models.Model):
    _name = "desk.material.line"
    _description = "Materials for Desk"

    # We are using product.product (product variant)
    # Bcs that is the actual product that user is ordering (in cart)
    # The user is not ordering the main product, but the variant of it
    product_id = fields.Many2one("product.product")
    quantity = fields.Float()
    unit_price = fields.Float(related="product_id.standard_price")
    order_id = fields.Many2one("desk.order", ondelete="cascade")
