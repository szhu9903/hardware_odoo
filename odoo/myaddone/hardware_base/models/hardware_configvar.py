#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：hardware_configvar.py
@Author  ：szhu9903
@Date    ：2023/8/2 09:07 
'''

from odoo import fields, models

config_map = {
    '5': '021002',
    '4': '020102',
}

class HardwareConfigVar(models.Model):
    """
    设备配置项
    """
    _name = 'hardware.configvar'
    _description = '设备配置项'
    _rec_name = 'hcv_variablekey'
    _sql_constraints = [
        ('uk_sys_configvar_hcv_type_id_scv_variablekey', 'UNIQUE (hcv_type_id, hcv_variablekey)', 'configvar hcv_type_id hcv_variablekey unique!'),
    ]

    hcv_type_id = fields.Many2one('hardware.type', '设备类型')
    hcv_variablekey = fields.Char('参数项名称', required=True)
    hcv_variablevalue = fields.Integer('参数项取值', required=True)
    hcv_describe = fields.Char('描述')

    def write(self, vals):
        res = super(HardwareConfigVar, self).write(vals)
        # 获取分类全部配置
        config_data = self.search([('hcv_type_id','=',self.hcv_type_id.id)])
        message_data = {config.hcv_variablekey: config.hcv_variablevalue for config in config_data}
        if self.hcv_type_id:
            self.env['util.rabbitmq'].send_to_type_equip(self.hcv_type_id.ht_name, config_map[str(self.hcv_type_id.id)], message_data)
        else:
            self.env['util.rabbitmq'].send_to_all_equip('020002', message_data)
        return res

    # # 修改环境数据
    # def after_deal_put(self):
    #     config_data = SqlExecute.query_sql_data(self.query_config_sql, (g.view_args['record_id'],))
    #     message_data = {config['hcv_variablekey']: config['hcv_variablevalue'] for config in config_data}
    #     if config_data[0]['hcv_type']:
    #         event_name = config_map[str(config_data[0]['hcv_type'])]
    #         FlaskRabbitMQ.send_to_type_equip(config_data[0]['ht_name'],
    #                                          event_meta[event_name]['EVENT'],
    #                                          message_data)
    #
    #     else:
    #         FlaskRabbitMQ.send_to_all_equip(event_meta['COMM_HEARTBEAT_INTER_REQ']['EVENT'], message_data)

