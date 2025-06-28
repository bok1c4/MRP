from odoo import models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()

        _logger.info("🟢 Entered custom action_confirm for SaleOrder")

        for order in self:
            _logger.info("📦 Processing SaleOrder %s (ID: %s)",
                         order.name, order.id)

            for line in order.order_line:
                tmpl = line.product_id.product_tmpl_id
                _logger.info(
                    "🔍 Line: product=%s, type=%s, desk_custom=%s",
                    line.product_id.name,
                    line.product_id.type,
                    tmpl.desk_custom
                )

                if line.product_id.type == 'product' and tmpl.desk_custom:
                    try:
                        # ❗ FIX: "order.line.product_id" is incorrect — should be "line.product_id"
                        name = self.env['ir.sequence'].next_by_code(
                            'desk.order') or f"{order.name} - {line.product_id.display_name}"

                        new_desk_order = self.env['desk.order'].create({
                            'name': name,
                            'sale_order_id': order.id,
                            'product_id': line.product_id.id,
                            'quantity': line.product_uom_qty,
                            'customer_id': order.partner_id.id,
                        })

                        _logger.info("✅ Created desk.order %s (ID: %s)",
                                     new_desk_order.name, new_desk_order.id)

                    except Exception as e:
                        _logger.error(
                            "❌ Failed to create desk.order for product %s: %s", line.product_id.name, e)

        return res
