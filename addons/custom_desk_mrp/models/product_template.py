from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    desk_custom = fields.Boolean(string='Is Custom Desk')
