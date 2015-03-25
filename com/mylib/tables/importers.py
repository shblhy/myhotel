#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import messages


class CsvImporter(object):
    """ CSV文件导入器

    Attributes:
        reader: csv.reader()的返回结果，是所有数据行的迭代器
        table: Table对象，需要用到里面的column信息，以及反向数据访问器reverse_accessors
        form_class: django form类，用于数据校验
        model_class: django model类，用于数据库插入记录

    """

    def __init__(self, reader, table, form_class, model_class):
        self.reader = reader
        self.table = table
        self.form_class = form_class
        self.model_class = model_class

    def _import(self):
        col_name_dict = dict([(column.sTitle, column) for column in self.table.columns])
        try:
            # 读取文件
            result, bad_num, col_index_dict = {}, 0, {}
            for row, row_data in enumerate(self.reader):
                if row == 0:  # 读取列头信息
                    col_index_dict = {}
                    for index, col_name in enumerate(row_data):
                        col_name = col_name.decode('gbk', 'ignore').strip()
                        if col_name not in col_name_dict:
                            message_level = messages.ERROR
                            message = u'CSV文件列名错误'
                            return message_level, message
                        col_index_dict[index] = col_name
                else:  # 读取数据
                    row_dict = {}
                    for col_index, value in enumerate(row_data):
                        col_name_cn = col_index_dict.get(col_index, '')
                        column = col_name_dict.get(col_name_cn)
                        if column:
                            value = value.decode('gbk', 'ignore').strip()
                            if column.field in self.table.reverse_accessors:
                                value = self.table.reverse_accessors[column.field](value)
                            row_dict[column.field] = value
                    self.table.check_unique()
                    if self.table.unique_column:  # 如果表格设置了唯一列，使用唯一列的值做key
                        if row_dict[self.table.unique_column] in result:  # 唯一列重复，错误记录数加1
                            bad_num += 1
                        result[row_dict[self.table.unique_column]] = row_dict
                    else:  # 使用csv的行数做key
                        result[row] = row_dict
            # 插入数据库
            new_obj_list = []
            for ret in result.values():
                form = self.form_class(ret)
                for field, validators in self.table.validators.items():
                    form.fields[field].validators = validators
                if form.is_valid():
                    new_obj_list.append(form.populate_obj(self.model_class()))
                else:
                    bad_num += 1
            if new_obj_list: self.model_class.objects.bulk_create(new_obj_list)
            message_level = messages.SUCCESS
            message = u'导入数据：成功%s条，失败%s条' % (len(new_obj_list), bad_num)
        except UnicodeDecodeError:
            message_level = messages.ERROR
            message = u'文件编码格式错误'
        return message_level, message
