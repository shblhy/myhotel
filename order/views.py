#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseBadRequest,HttpResponse
#from django.contrib.auth.decorators import login_required
#from order.table import OrderTable
from order.admin import OrderListManager
from order.form import OrderForm,OrderQForm
from order.models import Order
from room.models import RoomType
from datetime import datetime,timedelta
import json
def orders(request):
    form = OrderQForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_text())
    condition = form.get_condition()
    q = Order.objects.filter(**condition)
    table = OrderListManager(
         query=q,
         paginate_by = form.cleaned_data['iDisplayLength'],
         page = form.cleaned_data['iDisplayStart']+1,
         accessors_out = {
            'action':lambda x:OrderListManager.get_action(x,request.user)
            }
    ).to_table()
    return render_to_response('order/orders.html',locals())

def order_input(request,order_id=None,room_type=None):
    if order_id:
        order = get_object_or_404(Order,pk=order_id)
    else:
        room_type = get_object_or_404(RoomType,pk=room_type)
        order = Order()
        defautlTime = datetime.now()+timedelta(days=1)
        order.use_time = datetime(year=defautlTime.year,month=defautlTime.month,day=defautlTime.day,hour=8)
        order.room_type = room_type
        order.set_creater(request.user)
    return render_to_response('order/order_input.html',locals())

def order_detail(request,order_id=None):
    order = get_object_or_404(Order,pk=order_id)
    return render_to_response('order/order_detail.html',locals())

def input_order(request):
    order_id = request.POST.get('order_id',None)
    order = get_object_or_404(Order,pk=order_id) if order_id else None
    form = OrderForm(request.POST,instance = order)
    if form.is_valid():
        order = form.instance
        order.operator = request.user
        order.editdate = datetime.now()
        if not order.room:
            order.room = order.room_type.get_ready_room()
        order.save()
        result = {'status':0,'message':'success'}
    else:
        result = {'status':1,'message':form.errors_as_text()}
    return HttpResponse(json.dumps(result), content_type='text/html; charset=UTF-8')