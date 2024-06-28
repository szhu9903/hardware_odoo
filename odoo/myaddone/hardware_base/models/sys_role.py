#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：sys_role.py
@Author  ：szhu9903
@Date    ：2023/8/2 09:10 
'''

from odoo import fields, models

class SysRole(models.Model):
    """
    系统角色
    """
    _name = 'sys.role'
    _description = '角色'
    _rec_name = 'sr_name'
    _sql_constraints = [
        ('uk_sys_role_sr_name', 'UNIQUE (sr_name)', 'role sr_name unique!'),
    ]

    sr_name = fields.Char('角色名称', required=True)
    user_ids = fields.Many2many('sys.user', 'ur_relation', 'ur_roleid', 'ur_userid', '用户')
    purview_ids = fields.Many2many('sys.purview', 'rp_relation', 'rp_roleid', 'rp_purviewid', 'api权限')
    menu_ids = fields.Many2many('sys.menu', 'rm_relation', 'rm_roleid', 'rm_menuid', '后台管理菜单')

