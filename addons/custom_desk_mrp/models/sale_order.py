from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Check if:
    # Is this stockable physical product (type == 'product')
    # Has a custom boolean flag called desk_custom = True
    #
    # Then:
    # We are creating a new desk.order record that links this sales line and captures
    # - product
    # - quantity
    # - customer
    # - link back to the sales order

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            for line in order.order_line:
                if line.product_id.type == 'product' and line.product_id.product_tmpl_id.desk_custom:
                    self.env['desk.order'].create({
                        'sale_order_id': order.id,
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty,
                        'customer_id': order.partner_id.id,
                    })

        return res
