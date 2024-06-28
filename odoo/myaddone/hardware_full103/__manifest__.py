# -*- coding: utf-8 -*-
{
    'name': "hardware Dull103 ",
    'description': "Full103设备控制管理",
    'author': "ZSJ",
    # any module necessary for this one to work correctly
    'depends': ['hardware_base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/full103_env.xml',
        'views/full103_relay.xml',

        'views/full103_menu.xml',
    ],

    'application': False,
}
