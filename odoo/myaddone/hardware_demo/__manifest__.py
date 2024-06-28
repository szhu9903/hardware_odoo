# -*- coding: utf-8 -*-
{
    'name': "hardware Demo ",
    'description': "Demo设备控制管理",
    'author': "ZSJ",
    # any module necessary for this one to work correctly
    'depends': ['hardware_base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/demo_env.xml',
        'views/demo_led.xml',

        'views/demo_menu.xml',
    ],

    'application': False,
}
