# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from apps.member.admin import GroupListManager


def groups(request, contype='html'):
    condition = {}
    q = Group.objects.filter(**condition)
    table = GroupListManager(
        queryset=q,
        page=1,
        order_by='0',
        accessors_out={
            'action': lambda x: GroupListManager.get_action(x, request.user)
            }
    ).to_table()
    if contype == 'html':
        return render_to_response('member/groups.html', RequestContext(request, locals()))
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')


def group_input(request, group_id=None):
    if group_id:
        action = 'edit'
        group = get_object_or_404(Group, pk=group_id)
    else:
        action='add'
        group = Group()
    return render_to_response('member/group_input.html', RequestContext(request, locals()))
