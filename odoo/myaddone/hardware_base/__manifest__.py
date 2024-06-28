# -*- coding: utf-8 -*-
{
    'name': "hardware_center",
    'summary': "设备，控制，管理",
    'description': "硬件设备管理",
    'author': "ZSJ",
    'website': "https://zsjblog.com",
    'category': 'myapp/hardware',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'web_notify'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'wizard/assign_code.xml',

        'views/hardware_equip.xml',
        'views/hardware_type.xml',
        'views/hardware_configvar.xml',
        'views/sys_user.xml',
        'views/sys_role.xml',
        'views/sys_purview.xml',
        'views/sys_menu.xml',

        'views/my_schedule.xml',

        'views/base_menu.xml',
    ],

    'application': True,
}
