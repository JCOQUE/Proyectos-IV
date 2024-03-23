# -*- coding: utf-8 -*-
# from odoo import http


# class Borrar(http.Controller):
#     @http.route('/borrar/borrar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/borrar/borrar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('borrar.listing', {
#             'root': '/borrar/borrar',
#             'objects': http.request.env['borrar.borrar'].search([]),
#         })

#     @http.route('/borrar/borrar/objects/<model("borrar.borrar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('borrar.object', {
#             'object': obj
#         })
