# -*- coding: utf-8 -*-
#!/usr/bin/env python

import json
import csv
from functools import wraps
import time
import datetime
import types
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import models
from django.core.serializers.json import DateTimeAwareJSONEncoder

from com.mylib.tables.tables import Column
from com.mylib.encoder import base_encode

def parse(data):
    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            #ret = str(data)
            ret = float(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        elif isinstance(data, datetime.datetime):
            ret = data.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data, datetime.date):
            ret = time.strftime("%Y/%m/%d", data.timetuple())
        elif isinstance(data, Column):
            ret = data.__json__()
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        for f in data._meta.fields:
            ret[f.name] = _any(getattr(data, f.attname))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, cls=DateTimeAwareJSONEncoder)


def object_does_not_exist(func=None, redirect=None):
    """
    装饰器：对象不存在，404错误跳转到指定url
    使用：
        @object_does_not_exist(redirect='/')
        def detail(request):
            pass

        @object_does_not_exist
        def foo(request):
            pass
    """
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                if redirect:
                    return HttpResponseRedirect(redirect)
                else:
                    raise Http404()

        return returned_wrapper

    if not func:
        def foo(func):
            return decorator(func)

        return foo

    else:
        return decorator(func)


def render(*formats):
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            template, csv_filename = None, None
            if len(formats) == 0:  # 视图装饰器至少需要一个参数
                raise ValueError('View decorator: render, tasks 1 arguments at least(0 given).')
            if 'format' in kwargs:
                if kwargs['format'] not in ('html', 'json', 'csv'):  # url的后缀格式只支持html/json/csv
                    raise ValueError('View decorator: render, the argument can only be take html, json or csv.')
                format_list = []
                for f in formats:
                    if f.endswith('html'):
                        template = f
                        format_list.append('html')
                    elif f.endswith('csv'):
                        csv_filename = f
                        format_list.append('csv')
                    else:
                        format_list.append(f)
                if kwargs['format'] not in format_list:
                    raise ValueError('View decorator: render, the argument %s is not given.' % kwargs['format'])
                return_format = kwargs['format']
            else:
                if formats[0].endswith('html'):
                    return_format = 'html'
                    template = formats[0]
                elif formats[0].endswith('csv'):
                    return_format = 'csv'
                    csv_filename = formats[0]
                else:
                    return_format = formats[0]

            view_response = func(request, *args, **kwargs)
            if return_format == 'html':
                if isinstance(view_response, HttpResponse):
                    return view_response
                else:
                    return render_to_response(
                        template,
                        view_response,
                        context_instance=RequestContext(request),
                    )
            elif return_format == 'json':
                return HttpResponse(parse(view_response), mimetype='application/json')
            else:  # csv
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="%s"' % csv_filename.encode('gbk')
                writer = csv.writer(response)
                view_response = json.loads(parse(view_response))
                columns = view_response.get('columns', [])
                writer.writerow([r['sTitle'].encode('gbk') if isinstance(r['sTitle'], basestring) else r for r in columns])
                rows = view_response.get('rows', [])
                for row in rows:
                    writer.writerow([r.encode('gbk') if isinstance(r, basestring) else r for r in row])
                return response

        return returned_wrapper
    return decorator


def render_to_csv_response(csv_filename,rows,columns):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % csv_filename.encode('gbk')
    writer = csv.writer(response)
    #writer.writerow([r['sTitle'].encode('gbk') if isinstance(r['sTitle'], basestring) else r for r in columns])
    writer.writerow([r.encode('gbk') if isinstance(r, basestring) else base_encode(r) for r in columns])
    import logging
    log = logging.getLogger('mylog')
    log.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+":")
    for row in rows:
        try:
            line = []
            for r in row:
                if isinstance(r, basestring):
                    line.append(r.encode('gbk'))
                else:
                    line.append(base_encode(r))
            writer.writerow(line)
            #writer.writerow([r.encode('gbk') if isinstance(r, basestring) else base_encode(r) for r in row])
        except Exception,e0:
            log.info(e0.message)
            log.info(row)
    return response
            
def conrender(contype, params):
    param = params[contype] 
    if contype == 'page':
        return render_to_response(param[0],param[1])
    elif contype == 'table':
        return HttpResponse(param.get_rows(),mimetype='application/json')
    elif contype == 'csv':
        return render_to_csv_response(param[0],param[1].rows(columns=param[1].columns_exclude_action),[c.sTitle for c in param[1].columns_exclude_action])

def raise_404(method):
    def wrap(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ObjectDoesNotExist, ex:
            raise Http404(ex.message)

    return wrap
