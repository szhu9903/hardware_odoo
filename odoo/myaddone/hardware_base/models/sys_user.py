#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：sys_user.py
@Author  ：szhu9903
@Date    ：2023/8/2 09:10 
'''

from odoo import fields, models, api
from werkzeug.security import generate_password_hash

class SysUser(models.Model):
    _name = 'sys.user'
    _description = '用户信息'
    _rec_name = 'su_username'
    _sql_constraints = [
        ('uk_sys_user_su_account', 'UNIQUE (su_account)', 'user su_account unique!'),
    ]

    su_account = fields.Char('web账号', required=True)
    su_pwd = fields.Char('web密码', required=True)
    su_sex = fields.Selection([('男','男'),('女','女')], '性别', default='男')
    su_username = fields.Char('用户名', required=True, default='')
    su_userphoto = fields.Binary('头像')
    su_phone = fields.Char('电话', default='')
    su_email = fields.Char('邮箱', default='')
    su_isadmin = fields.Selection([('0','否'),('1','是')], '后台用户', default='1')
    su_delflag = fields.Selection([('0','有效'),('1','无效')],'有效状态', default='0')

    su_odoouser_id = fields.Many2one('res.users', '关联odoo用户')
    role_ids = fields.Many2many('sys.role', 'ur_relation', 'ur_userid', 'ur_roleid', '角色')


    # 创建新纪录时执行方法
    @api.model
    def create(self, vals_list):
        if vals_list['su_pwd']:
            vals_list['su_pwd'] = generate_password_hash(vals_list['su_pwd'])
        res = super(SysUser, self).create(vals_list)
        return res

    # 修改记录时执行方法
    def write(self, vals):
        res = super(SysUser, self).write(vals)
        return res

    def button_modify_pwd(self):
        print('修改密码！')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '未成功下线',
                'message': '未成功下线，可能该会话已过期',
                'sticky': False,
                'className': 'bg-warning'
            }
        }
