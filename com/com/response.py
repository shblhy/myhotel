# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@author:hy 
渲染器，常见渲染/响应动作
'''
import csv,json
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render_to_response
FLOAT_REPR = lambda x:"%.2f" % x

def base_encode(value):
    if isinstance(value, float):
        value = FLOAT_REPR(value)
    return value

def render_to_csv_response(csv_filename,rows,columns=None):
    if type(rows) == tuple and columns is None:
        rows,columns = rows
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % csv_filename.encode('gbk')
    writer = csv.writer(response)
    #writer.writerow([r['sTitle'].encode('gbk') if isinstance(r['sTitle'], basestring) else r for r in columns])
    writer.writerow([r.encode('gbk') if isinstance(r, basestring) else base_encode(r) for r in columns])
    for row in rows:
        line = []
        for r in row:
            if isinstance(r, basestring):
                line.append(r.encode('gbk'))
            else:
                line.append(base_encode(r))
        writer.writerow(line)
    return response

class HttpJsonResponse(HttpResponse):
    def __init__(self,res):
        super(HttpJsonResponse, self).__init__(json.dumps(res), content_type='application/json; charset=UTF-8')
