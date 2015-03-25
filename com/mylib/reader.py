# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@author:hy 
读取器，常见读取动作
'''

def read_csv(reader,col_name_dict):
    result, col_index_dict = [], {}
    for row, row_data in enumerate(reader):
        if row == 0:
            col_index_dict = {}
            for index, col_name in enumerate(row_data):
                #col_name = col_name.decode('utf-8', 'ignore').strip()
                col_name = col_name.decode('gbk', 'ignore').strip()
                if col_name not in col_name_dict:
                    raise Exception(u'CSV文件列名错误')
                    '''
                    if index == 0 and col_name[1:] not in col_name_dict:
                        return HttpResponseBadRequest(u'CSV文件列名错误', content_type='application/javascript')
                    elif index <>0:
                        return HttpResponseBadRequest(u'CSV文件列名错误', content_type='application/javascript')
                    '''
                col_index_dict[index] = col_name
        else:
            row_dict = {}
            for col_index, value in enumerate(row_data):
                col_name_cn = col_index_dict.get(col_index, '')
                col_name_en = col_name_dict.get(col_name_cn, 'undefined')
                row_dict[col_name_en] = value.decode('gbk', 'ignore').strip()
            result.append(row_dict)
    return result