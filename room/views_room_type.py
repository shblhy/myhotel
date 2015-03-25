#-*- coding:utf-8 -*-
import os
import json,csv
from datetime import datetime
from com.mylib.mytime import datetime_to_timestamp
from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render_to_response,get_object_or_404
#from django.contrib.auth.decorators import login_required
#from room.table import RoomTypeTable
from room.admin import RoomListManager,RoomTypeListManager
from room.forms import RoomTypeForm
from room.models import Room,RoomType
from settings import STATIC_ROOT_PATH
from PIL import Image
from libs.yhwork.response import HttpJsonResponse,render_to_csv_response
from django.template import RequestContext

def room_types(request,contype='html'):
    condition = {}
    q = RoomType.objects.filter(**condition)
    table = RoomTypeListManager(
        queryset = q,
        paginate_by = 30,
        page = 1,
        accessors_out = {'action':lambda x:
                         RoomListManager.get_action(x,request.user)
                         },
    ).to_table()
    print table.get_columns()
    print table.get_rows()
    if contype == 'html':
        return render_to_response('room/room_types.html',RequestContext(request,locals()))
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')
    elif contype == 'csv':
        return render_to_csv_response(u"店面列表.csv",table.to_csv())
    
def room_type_list(request,contype='html'):
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
    condition = {}
    room_types = RoomType.objects.filter(**condition)
    return render_to_response('room/room_type_list.html',locals())

def room_type_input(request,action='add',room_type_id=None):
    if room_type_id:
        room_type = get_object_or_404(RoomType,pk=room_type_id)
    else:
        room_type = RoomType()
    return render_to_response('room/room_type_input.html',locals())

def room_type_detail(request,room_type_id=None):
    room_type = get_object_or_404(RoomType,pk=room_type_id)
    return render_to_response('room/room_type.html',locals())

def add_room_type(request):
    form = RoomTypeForm(request.POST)
    room = form.get_object()
    room.save()
    return HttpResponse('')

def input_room_type(request,action='add'):
    form = RoomTypeForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpJsonResponse(form.instance.id)
    return HttpResponseBadRequest(form.errors.as_text())

def delete_room_types(request):
    try:
        RoomType.objects.filter(id__in = request.POST['ids'].split(',')).delete()
        return HttpJsonResponse('')

    except Exception,e0:
        return HttpResponseBadRequest(u'删除失败:'+e0.message,content_type='application/javascript')

def upload_photo(request):
    photoFile = request.FILES.get('photo',None)
    filename = os.path.basename(photoFile.name)#上传文件名
    suffix = filename.split('.')[-1:][0]
    if not suffix in ('jpg','png','bmp'):
        return HttpResponseBadRequest('上传文件扩展名错误，只能为jpg/png/bmp',content_type='application/javascript; charset=UTF-8')
    if photoFile.size > 2*1024*1024:
        return HttpResponseBadRequest('上传文件过大，必须小于2M',content_type='application/javascript; charset=UTF-8')
    img = Image.open(photoFile)
    phigh,pwidth=img.size
    if not  (200 < phigh< 600 and 200 < pwidth < 600):
        return HttpResponseBadRequest(u'上传图片长必须在200~600间，宽必须在200~600间',content_type='application/javascript; charset=UTF-8')
    #文件大小检查
    #文件长宽检查
    timeStamp = datetime_to_timestamp(datetime.now())
    newFileName = timeStamp+'.'+suffix
    dirPath = os.path.join(os.path.join(STATIC_ROOT_PATH,'upload'),'room_type')    
    tarpath = os.path.join(dirPath,newFileName)
    f=open(tarpath, "wb+")
    for chunk in photoFile.chunks(): 
        f.write(chunk)
    f.close()
    return HttpResponse(json.dumps(newFileName),content_type='application/json; charset=UTF-8')