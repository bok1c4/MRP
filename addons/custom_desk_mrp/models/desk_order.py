from odoo import models, fields, api, _
import logging


class DeskOrder(models.Model):
    _name = "desk.order"
    _inherit = ["mail.thread"]  # chatter
    _description = "Custom Desk Order"

    name = fields.Char(string="Order Reference",
                       required=True, default=lambda self: _('New'))

    customer_id = fields.Many2one(
        "res.partner", string="Customer", required=True)

    desk_product_id = fields.Many2one(
        "product.template", string="Desk Type", required=True)

    # One2many: one DeskOrder → many material lines
    material_ids = fields.One2many(
        "desk.material.line", "order_id", string="Materials Used")

    total_cost = fields.Float(compute="_compute_total_cost", store=True)

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('in_production', 'In Production'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )

    @api.depends('material_ids.quantity', 'material_ids.unit_price')
    def _compute_total_cost(self):
        for order in self:
            order.total_cost = sum(
                line.quantity * line.unit_price for line in order.material_ids)

    def fetch_sale_order_details(self):
        for order in self:
            sale_order = self.env['sale.order'].search(
                [('origin', '=', order.name)], limit=1
            )
            if sale_order:
                for line in sale_order.order_line:
                    logging()._logger.info(line.product_id.name)
