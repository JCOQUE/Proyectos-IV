# -*- coding: utf-8 -*-
# from odoo import http


# class Consumer(http.Controller):
#     @http.route('/consumer/consumer', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/consumer/consumer/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('consumer.listing', {
#             'root': '/consumer/consumer',
#             'objects': http.request.env['consumer.consumer'].search([]),
#         })

#     @http.route('/consumer/consumer/objects/<model("consumer.consumer"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('consumer.object', {
#             'object': obj
#         })
