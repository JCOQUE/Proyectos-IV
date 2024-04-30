# -*- coding: utf-8 -*-
# from odoo import http


# class Nvaf(http.Controller):
#     @http.route('/nvaf/nvaf', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nvaf/nvaf/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nvaf.listing', {
#             'root': '/nvaf/nvaf',
#             'objects': http.request.env['nvaf.nvaf'].search([]),
#         })

#     @http.route('/nvaf/nvaf/objects/<model("nvaf.nvaf"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nvaf.object', {
#             'object': obj
#         })
