# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseAgreement(http.Controller):
#     @http.route('/purchase_agreement/purchase_agreement', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_agreement/purchase_agreement/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_agreement.listing', {
#             'root': '/purchase_agreement/purchase_agreement',
#             'objects': http.request.env['purchase_agreement.purchase_agreement'].search([]),
#         })

#     @http.route('/purchase_agreement/purchase_agreement/objects/<model("purchase_agreement.purchase_agreement"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_agreement.object', {
#             'object': obj
#         })
