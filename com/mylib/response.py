# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@author:hy 
渲染器，常见渲染/响应动作
'''
import csv,json
from django.http import HttpResponse
from datetime import datetime
from com.mylib.encoder import base_encode
from django.shortcuts import render_to_response

def render_to_csv_response(csv_filename,rows,columns):
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
            
def conrender(contype, params):
    param = params[contype] 
    if contype == 'html':
        return render_to_response(param[0],param[1])
    elif contype == 'table':
        if type(param)==tuple and param[1]=='with_columns':
            res = {'rows':param.get_rows(to_str=False),'columns':param.get_columns(to_str=False)}
            return HttpJsonResponse(res)
        else:
            return HttpJsonResponse(param.get_rows())
    elif contype == 'csv':
        return render_to_csv_response(param[0],param[1].rows(columns=param[1].columns_exclude_action),[c.sTitle for c in param[1].columns_exclude_action])


class HttpJsonResponse(HttpResponse):
    def __init__(self,res):
        super(HttpJsonResponse, self).__init__(json.dumps(res), content_type='application/javascript')
