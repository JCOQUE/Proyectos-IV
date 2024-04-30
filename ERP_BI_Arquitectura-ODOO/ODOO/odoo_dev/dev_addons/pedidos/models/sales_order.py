from odoo import models

class SaleOrder(models.Model):
    _name = 'sale.order'

    def create_sale_order(self, log_data):
        new_order = self.env['sale.order'].create({
            'partner_id': log_data['partner_id'],
            'name': log_data['name'],
            'client_order_ref': log_data['client_order_ref'],
            'date_order': log_data['date_order'],
            'state': 'purchase',  # Replace with appropriate state value
            'company_id': log_data['company_id'],
            'order_line': [(0, 0, line_info) for line_info in log_data['order_line']],
        })
        return new_order