#-*- coding:utf-8 -*-
import json,csv
from com.mylib.response import conrender
from com.mylib.reader import read_csv
from django.core.paginator import Paginator
from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response,get_object_or_404
#from django.contrib.auth.decorators import login_required
from room.table import RoomTable
from room.forms import RoomQForm,RoomForm,RoomType
from room.models import Room
from com.mylib.response import HttpJsonResponse

def rooms(request,contype='html'):
    form = RoomQForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_text())
    condition = form.get_condition()
    q = Room.objects.filter(**condition)
    table = RoomTable(
        query=q,
        limit=form.cleaned_data['iDisplayLength'],
        offset=form.cleaned_data['iDisplayStart'],
        order_by=form.cleaned_data['orderBy'],
        reverse_accessors = {
            'action':lambda x:RoomTable.get_action(x,request.user)
            }
    )
    print table.get_columns()
    print table.get_rows()
    return conrender(contype,{'html':('room/rooms.html',locals()),
                      'table':table,
                      'csv':(u"房间列表.csv",table),
                      })

def room_list(request,contype='html'):
    '''
    todo.hy
    同一个内容只需要一个方法。该方法在后续重构优化中将与rooms整合。
    之所以出现难于处理不得不分开的原因是：
    django 为了参数接收，做了form机制
    为了数据传出，做了模板渲染机制
    但我的开发思想，前后端分离，各做各的事，数据以json方式传递前端，与此渲染机制不相符。
    table.Table 实际的作用：1是描述输出项，2是描述输出格式对齐前端所需，3是分页取数，
    应该可以用django 分页类 + 输出描述器 两者完成同类功能，并能扩展到任意控件。 
    输出描述器的开发 预计在此项目之后 暂时分开写。
    '''
    form = RoomQForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest()
    condition = form.get_condition()
    rooms = Room.objects.filter(**condition)
    return render_to_response('room/room_list.html',locals())


def room_input(request,action='add',room_id=None):
    if room_id:
        room = get_object_or_404(Room,pk=room_id)
    else:
        room = Room()
    return render_to_response('room/room_input.html',locals())

def room_detail(request,room_id=None):
    room = get_object_or_404(Room,pk=room_id)
    return render_to_response('room/room.html',locals())

def add_room(request):
    form = RoomForm(request.POST)
    room = form.get_object()
    room.save()
    return HttpResponse('')

def input_room(request,action='add'):
    form = RoomForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpJsonResponse(form.instance.id)
    return HttpResponseBadRequest(form.errors.as_text())

def import_rooms(request):
    csv_file = request.FILES['file']
    reader = csv.reader(csv_file)
    col_name_dict = {
        u'房号': 'sn',
        u'名称': 'name',
        u'说明': 'comment',
        u'类别': 'rtype'
    }
    try:
        result = read_csv(reader,col_name_dict)
    except Exception,e0:
        return HttpResponseBadRequest(e0.message, content_type='application/javascript')
    rooms = []
    rtypeDict = {roomType.name:roomType.id for roomType in RoomType.objects.all()}
    for item in result:
        room = Room()
        room.room_type_id = rtypeDict[item['rtype']]
        room.name = item['name']
        room.sn = item['sn']
        room.comment = item['comment']
        rooms.append(room)
    Room.objects.bulk_create(rooms)
    return HttpJsonResponse('')
    
def delete_rooms(request):
    try:
        Room.objects.filter(id__in = request.POST['ids'].split(',')).delete()
        return HttpJsonResponse('')
    except Exception,e0:
        return HttpResponseBadRequest(u'删除失败:'+e0.message,content_type='application/javascript')
    
