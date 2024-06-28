#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：hardware_tcp_server 
@File    ：create_command.py
@Author  ：szhu9903
@Date    ：2023/6/19 10:30 
'''

# import re
#
# pattern = re.compile('.{2}')
#
# def fingerprint_command(cmd_type, date_len, cmd_code, cmd_data):
#     command_head = bytes([0xEF, 0x01])
#     fingerprint_address = bytes([0xFF, 0xFF, 0xFF, 0xFF])
#
#     cmd_body = cmd_type + date_len + cmd_code + cmd_data
#     cmd_check = sum(cmd_body) & 0xFFFF
#
#     cmd_bytes = command_head + fingerprint_address + cmd_body + cmd_check.to_bytes(2, byteorder='big')
#     return cmd_bytes
#
#
# if __name__ == '__main__':
#     cmd_type = bytes([0x01])
#     date_len = bytes([0x00, 0x07])
#     cmd_code = bytes([0x3C])
#     cmd_data = bytes([0xFA, 0x80, 0x07, 0x00])
#     cmd_bytes = fingerprint_command(cmd_type, date_len, cmd_code, cmd_data)
#     cmd_str_list = pattern.findall(cmd_bytes.hex().upper())
#     print(' '.join(cmd_str_list))


# 导入依赖包
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor

# 创建连接对象

conn = psycopg2.connect(database="hardware_db",
                        user="hardware",
                        password="hardware",
                        host="127.0.0.1",
                        port="5432")

cur = conn.cursor(cursor_factory=RealDictCursor)  # 创建指针对象description

# 获取结果
cur.execute("UPDATE hardware_equip SET he_equipstatus='BROKEN' WHERE he_num=%s", (1002,))
last_id = cur.lastrowid

conn.commit()
cur.close()
conn.close()



