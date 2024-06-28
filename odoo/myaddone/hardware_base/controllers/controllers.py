# -*- coding: utf-8 -*-
# from odoo import http


# class Hardware(http.Controller):
#     @http.route('/hardware/hardware', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hardware/hardware/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hardware.listing', {
#             'root': '/hardware/hardware',
#             'objects': http.request.env['hardware.hardware'].search([]),
#         })

#     @http.route('/hardware/hardware/objects/<model("hardware.hardware"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hardware.object', {
#             'object': obj
#         })
