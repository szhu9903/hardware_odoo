#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：sys_purview.py
@Author  ：szhu9903
@Date    ：2023/8/2 09:11 
'''

from odoo import fields, models

class SysPurview(models.Model):
    """
    系统api权限
    """
    _name = 'sys.purview'
    _description = 'api权限'
    _rec_name = 'sp_name'
    _sql_constraints = [
        ('uk_sys_role_sr_name', 'UNIQUE (sp_name)', 'purview sp_name unique!'),
    ]

    sp_name = fields.Char('权限名称', required=True)
    sp_apipath = fields.Char('api_path', required=True)
    sp_type = fields.Selection([('1','查看'),('2','操作')],'权限类型', required=True, default='1')

