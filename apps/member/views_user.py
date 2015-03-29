# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from libs.yhwork.response import render_to_csv_response, HttpJsonResponse
from apps.member.models import User
from apps.member.admin import UserListManager
from apps.member.form import UserForm, UserQForm
from apps.order.admin import OrderListManager


def users(request, contype='html'):
    form = UserQForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_text())
    condition = form.get_conditions()
    q = User.objects.filter(**condition)
    table = UserListManager(
        queryset=q,
        paginate_by=form.cleaned_data['iDisplayLength'],
        page=form.cleaned_data['iDisplayStart'] + 1,
        accessors_out={'action': lambda x: UserListManager.get_action(x, request.user)}
    ).to_table()
    #print table.get_columns()
    #print table.get_rows()
    if contype == 'html':
        return render_to_response('member/users.html', RequestContext(request, locals()))
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')
    elif contype == 'csv':
        return render_to_csv_response(u"用户列表.csv", table.to_csv())


def user_input(request, action='add', user_id=None):
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    else:
        user = User()
    return render_to_response('member/user_input.html', RequestContext(request, locals()))


def user_detail(request, user_id=None):
    user = get_object_or_404(User, pk=user_id)
    return render_to_response('member/user.html', RequestContext(request, locals()))


def user_center(request):
    user = request.user
    orders = user.order_set.all()
    table = OrderListManager(
        queryset=orders,
        paginate_by=30,
        page=1,
        accessors_out={'action': lambda x: OrderListManager.get_action(x, request.user)},
    ).to_table()
    print table.get_columns()
    print table.get_rows()
    return render_to_response('member/center.html', RequestContext(request, locals()))


def input_user(request):
    user_id = request.POST.get('user_id', None)
    user = get_object_or_404(User, pk=user_id) if user_id else None
    form = UserForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        return HttpJsonResponse({'status': 'success'})
    return HttpResponseBadRequest(form.errors.as_text())


def regist(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.instance
        user.set_password(user.password)
        user.save()
        return HttpJsonResponse({'status': 'success'})
    return HttpResponseBadRequest(form.errors.as_text())


def import_users(request):
    return HttpResponse(u'开发中')


def delete_users(request):
    try:
        User.objects.filter(id__in=request.POST['ids'].split(',')).delete()
        return HttpJsonResponse('')
    except Exception,e0:
        return HttpResponseBadRequest(u'删除失败:' + e0.message, content_type='application/javascript')
