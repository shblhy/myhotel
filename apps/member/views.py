# -*- coding: utf-8 -*-
import json
from datetime import timedelta

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.views import password_change,password_change_done,logout as ori_logout
from django.contrib.auth import  login as auth_login
from django.http import HttpResponse,HttpResponseForbidden,HttpResponseBadRequest
from django.shortcuts import render_to_response,get_object_or_404
from member.models import User
from member.table import UserTable
from member.form import UserForm,UserQForm


def login(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        #auth_login(request, form.instance)
        #request.session.set_expiry(timedelta(days=7))
        res = {'username': form.get_user().username,
               'backend': form.get_user().is_superuser}
        return HttpResponse(json.dumps(res))
    return HttpResponseForbidden(form.errors.as_text())


def login_page(request):
    return render_to_response('user/login.html')


def regist_page(request):
    return render_to_response('user/regist.html')


def logout(request):
    return ori_logout(request,next_page='/')