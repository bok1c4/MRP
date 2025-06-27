from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class DeskOrderController(http.Controller):

    @http.route('/api/desks/customer/<int:partner_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_customer_desk_orders(self, partner_id, **kwargs):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return {'error': 'Customer not found'}

        orders = request.env['desk.order'].sudo().search([
            ('customer_id', '=', partner_id)
        ])

        result = []
        for order in orders:
            materials = [
                {
                    'product': line.product_id.name,
                    'quantity': line.quantity,
                    'unit_price': line.unit_price
                }
                for line in order.material_ids
            ]

            result.append({
                'order_id': order.id,
                'order_ref': order.name,
                'customer': order.customer_id.name,
                'desk': order.desk_product_id.name,
                'total_cost': order.total_cost,
                'state': order.state,
                'materials': materials
            })

        return {'orders': result}

    @http.route('/api/test', type='http', auth='public', methods=['GET'], csrf=False)
    def test_route(self, **kwargs):
        _logger.warning("🧪 test_route was called!")
        return "Hello, sk API"
