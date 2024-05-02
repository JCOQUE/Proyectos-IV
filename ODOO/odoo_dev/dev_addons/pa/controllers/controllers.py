# -*- coding: utf-8 -*-
# from odoo import http


# class Pa(http.Controller):
#     @http.route('/pa/pa', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pa/pa/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pa.listing', {
#             'root': '/pa/pa',
#             'objects': http.request.env['pa.pa'].search([]),
#         })

#     @http.route('/pa/pa/objects/<model("pa.pa"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pa.object', {
#             'object': obj
#         })
