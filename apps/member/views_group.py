# -*- coding: utf-8 -*-
import json
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import  login as auth_login,password_change,password_change_done,logout
from django.http import HttpResponse,HttpResponseForbidden,HttpResponseBadRequest
from django.shortcuts import render_to_response,get_object_or_404
#from member.table import GroupTable
from member.admin import GroupListManager
from libs.yhwork.response import render_to_csv_response

def groups(request,contype='html'):
    condition = {}
    q = Group.objects.filter(**condition)
    table = GroupListManager(
        query = q,
        page = 1,
        order_by = '0',
        accessors_out = {
            'action':lambda x:GroupListManager.get_action(x,request.user)
            }
    ).to_table()
    print table.get_columns()
    print table.get_rows()
    if contype == 'html':
        return render_to_response('member/groups.html',locals())
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')
    elif contype == 'csv':
        return render_to_csv_response(u"店面列表.csv",table.to_csv())
    

def group_input(request,action='add',group_id=None):
    if group_id:
        group = get_object_or_404(Group,pk=group_id)
    else:
        group = Group()
    return render_to_response('member/group_input.html',locals())