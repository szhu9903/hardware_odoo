#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：sys_menu.py
@Author  ：szhu9903
@Date    ：2023/8/2 09:12 
'''

from odoo import fields, models

class SysMenu(models.Model):
    """
    系统后台管理菜单
    """
    _name = 'sys.menu'
    _description = '后台管理菜单'
    _rec_name = 'sm_name'
    _sql_constraints = [
        ('uk_sys_menu_sm_name', 'UNIQUE (sm_name)', 'menu sm_name unique!'),
    ]


    sm_name = fields.Char('菜单名称', required=True)
    sm_menupath = fields.Char('path')
    sm_menuup_id = fields.Many2one('sys.menu','父级菜单')
    sm_sort = fields.Integer('菜单顺序', required=True, default=0)

