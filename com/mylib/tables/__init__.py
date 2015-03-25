#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" Table插件

Version: 0.1
Author: Tim
Date: 2014/1/15

你能够很容易将数据转化为HTML表格，特色：
    1. 排序
    2. 分页
    3. 表格操作按钮：新建、导入、删除、导出

术语:
    table: 表格
    button: 表格上面的附加按钮
    column: 列
    accessor: 格式化数据的回调方法
    caller: 返回一个回调方法的方法

Tutorial:

Author: Hy
前端做前端的事，后端做后端的事，数据以json传递给js。
不是很符合我的思想，不过暂且用用，后续归纳。

"""

from __future__ import absolute_import

from com.mylib.tables.tables import *
from com.mylib.tables.buttons import *
from com.mylib.tables.columns import *
from com.mylib.tables.importers import *
