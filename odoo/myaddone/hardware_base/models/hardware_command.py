#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：odoo 
@File    ：hardware_command.py
@Author  ：szhu9903
@Date    ：2023/8/7 17:06 
'''

import logging
import time
import asyncio
from dateutil.relativedelta import relativedelta
from odoo import fields, models

_logger = logging.getLogger(__name__)

class HardwareCommand(models.Model):
    _name = 'hardware.command'
    _description = '设备命令'




