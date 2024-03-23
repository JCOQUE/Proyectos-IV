# -*- coding: utf-8 -*-
# from odoo import http


# class Pedidos(http.Controller):
#     @http.route('/pedidos/pedidos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pedidos/pedidos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pedidos.listing', {
#             'root': '/pedidos/pedidos',
#             'objects': http.request.env['pedidos.pedidos'].search([]),
#         })

#     @http.route('/pedidos/pedidos/objects/<model("pedidos.pedidos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pedidos.object', {
#             'object': obj
#         })
