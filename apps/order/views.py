#-*- coding:utf-8 -*-
import json
from datetime import datetime, timedelta
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from libs.yhwork.response import HttpJsonResponse
from apps.order.admin import OrderListManager
from apps.order.form import OrderForm, OrderQForm
from apps.order.models import Order
from apps.room.models import RoomType


def orders(request, contype='html'):
    form = OrderQForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_text())
    condition = form.get_condition()
    q = Order.objects.filter(**condition)
    table = OrderListManager(
         query=q,
         paginate_by=form.cleaned_data['iDisplayLength'],
         page=form.cleaned_data['iDisplayStart'] + 1,
         accessors_out={
            'action': lambda x: OrderListManager.get_action(x, request.user)
            }
    ).to_table()
    if contype == 'html':
        return render_to_response('order/orders.html', locals())
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')


def order_input(request, order_id=None, room_type=None):
    if order_id:
        order = get_object_or_404(Order, pk=order_id)
    else:
        room_type = get_object_or_404(RoomType, pk=room_type)
        order = Order()
        defautlTime = datetime.now() + timedelta(days=1)
        order.use_time = datetime(year=defautlTime.year,
            month=defautlTime.month, day=defautlTime.day, hour=8)
        order.room_type = room_type
        if request.user.pk != None:
            order.set_creater(request.user)
    return render_to_response('order/order_input.html', locals())


def order_detail(request, order_id=None):
    order = get_object_or_404(Order, pk=order_id)
    return render_to_response('order/order_detail.html', locals())


def input_order(request):
    order_id = request.POST.get('order_id', None)
    order = get_object_or_404(Order, pk=order_id) if order_id else None
    form = OrderForm(request.POST, instance=order)
    if form.is_valid():
        order = form.instance
        order.operator = request.user
        order.editdate = datetime.now()
        if not order.room:
            order.room = order.room_type.get_ready_room()
        order.save()
        result = {'status': 'success'}
        return HttpJsonResponse(result)
    else:
        return HttpResponseBadRequest(form.errors_as_text())
