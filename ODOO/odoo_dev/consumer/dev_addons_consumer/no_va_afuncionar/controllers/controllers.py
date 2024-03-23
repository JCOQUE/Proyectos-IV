# -*- coding: utf-8 -*-
# from odoo import http


# class NoVaAfuncionar(http.Controller):
#     @http.route('/no_va_afuncionar/no_va_afuncionar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/no_va_afuncionar/no_va_afuncionar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('no_va_afuncionar.listing', {
#             'root': '/no_va_afuncionar/no_va_afuncionar',
#             'objects': http.request.env['no_va_afuncionar.no_va_afuncionar'].search([]),
#         })

#     @http.route('/no_va_afuncionar/no_va_afuncionar/objects/<model("no_va_afuncionar.no_va_afuncionar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('no_va_afuncionar.object', {
#             'object': obj
#         })
