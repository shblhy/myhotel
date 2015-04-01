#-*- coding:utf-8 -*-
import os, json, csv
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from libs.djex.response import HttpJsonResponse, render_to_csv_response
from libs.utils.mytime import datetime_to_timestamp
from settings import STATIC_ROOT_PATH
from apps.room.admin import RoomListManager, RoomTypeListManager
from apps.room.forms import RoomTypeForm
from apps.room.models import RoomType


def room_types(request, contype='html'):
    condition = {}
    q = RoomType.objects.filter(**condition)
    table = RoomTypeListManager(
        queryset=q,
        paginate_by=30,
        page=1,
        accessors_out={'action': lambda x:
                       RoomListManager.get_action(x, request.user)
                         },
    ).to_table()
    if contype == 'html':
        return render_to_response('room/room_types.html', RequestContext(request, locals()))
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')
    elif contype == 'csv':
        return render_to_csv_response(u"房型列表.csv", table.to_csv())


def room_type_list(request, contype='html'):
    condition = {}
    room_types = RoomType.objects.filter(**condition)
    return render_to_response('room/room_type_list.html', RequestContext(request, locals()))


def room_type_input(request, room_type_id=None):
    if room_type_id:
        action = 'edit'
        room_type = get_object_or_404(RoomType, pk=room_type_id)
    else:
        action = 'add'
        room_type = RoomType()
    return render_to_response('room/room_type_input.html', RequestContext(request, locals()))


def room_type_detail(request, room_type_id=None):
    room_type = get_object_or_404(RoomType, pk=room_type_id)
    return render_to_response('room/room_type.html', RequestContext(request, locals()))


def add_room_type(request):
    form = RoomTypeForm(request.POST)
    room = form.get_object()
    room.save()
    return HttpResponse('')


def input_room_type(request, action='add'):
    room_type_id = request.POST.get('room_type_id', None)
    room_type = get_object_or_404(RoomType, pk=room_type_id) if room_type_id else None
    form = RoomTypeForm(request.POST, instance=room_type)
    if form.is_valid():
        form.save()
        return HttpJsonResponse(form.instance.id)
    return HttpResponseBadRequest(form.errors_as_text())


def delete_room_types(request):
    try:
        RoomType.objects.filter(id__in=request.POST['ids'].split(',')).delete()
        return HttpJsonResponse('')
    except Exception, e0:
        return HttpResponseBadRequest(u'删除失败:' + e0.message, content_type='application/javascript')


def upload_photo(request):
    from PIL import Image
    photoFile = request.FILES.get('photo', None)
    filename = os.path.basename(photoFile.name)
    suffix = filename.split('.')[-1:][0]
    if not suffix in ('jpg', 'png', 'bmp'):
        return HttpResponseBadRequest('上传文件扩展名错误，只能为jpg/png/bmp', content_type='application/javascript; charset=UTF-8')
    if photoFile.size > 2 * 1024 * 1024:
        return HttpResponseBadRequest('上传文件过大，必须小于2M', content_type='application/javascript; charset=UTF-8')
    img = Image.open(photoFile)
    phigh, pwidth = img.size
    if not  (200 < phigh < 600 and 200 < pwidth < 600):
        return HttpResponseBadRequest(u'上传图片长必须在200~600间，宽必须在200~600间', content_type='application/javascript; charset=UTF-8')
    #文件大小检查
    #文件长宽检查
    timeStamp = datetime_to_timestamp(datetime.now())
    newFileName = timeStamp + '.' + suffix
    dirPath = os.path.join(os.path.join(STATIC_ROOT_PATH, 'upload'), 'room_type')
    tarpath = os.path.join(dirPath, newFileName)
    f = open(tarpath, "wb+")
    for chunk in photoFile.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse(json.dumps(newFileName), content_type='application/json; charset=UTF-8')
