from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# Desk Order model:
# sale.order
# product.product (varient)
# order_quantity
# customer
# materials used (for -> inventory and manufacturing)
# total cost of the desk order
# state

class DeskOrder(models.Model):
    _name = 'desk.order'
    _description = 'Desk Manufacturing Order'
    _inherit = ['mail.thread']

    name = fields.Char(
        string='Reference',
        required=True,
        # When a new desk.order is created and no name is provided, automatically use the next available sequence value for 'desk.order'
        # DO-0001 - example
        default=lambda self: self.env['ir.sequence'].next_by_code('desk.order')
    )
    sale_order_id = fields.Many2one('sale.order', string='Source Sale Order')
    product_id = fields.Many2one(
        'product.product', string='Desk Product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    customer_id = fields.Many2one(
        'res.partner', string='Customer', required=True)

    material_ids = fields.One2many(
        'desk.material.line', 'order_id', string='Materials Used')

    total_cost = fields.Float(
        string='Total Cost',
        compute='_compute_total_cost',
        store=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], default='draft', tracking=True)

    @api.depends('quantity', 'product_id')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.quantity * rec.product_id.list_price
