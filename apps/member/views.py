# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import password_change_done, password_change, logout as ori_logout
from django.contrib.auth import  login as auth_login
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from libs.yhwork.response import HttpJsonResponse


def login(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        res = {'username': form.get_user().username,
               'backend': form.get_user().is_superuser}
        return HttpJsonResponse(res)
    return HttpResponseForbidden(form.errors.as_text())


def login_page(request):
    return render_to_response('user/login.html')


def regist_page(request):
    return render_to_response('user/regist.html')


def logout(request):
    return ori_logout(request, next_page='/')