# -*- coding: utf-8 -*-
import os
import subprocess
import logging
from datetime import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.member.models import User
from apps.room.models import Room
from apps.order.models import Order
from apps.article.models import Article
from common import render_to_basehtml_response


def index(request):
    return render_to_response('index.html',locals())


def hotel(request):
    return render_to_basehtml_response('main/hotel.html',locals())


def order(request):
    return render_to_basehtml_response('main/order.html', RequestContext(request, locals()))


def rooms(request):
    return render_to_basehtml_response('main/rooms.html', RequestContext(request, locals()))


def pictures(request):
    return render_to_basehtml_response('main/pictures.html', RequestContext(request, locals()))


def special_offers(request):
    return render_to_basehtml_response('main/special_offers.html', RequestContext(request, locals()))


def about(request):
    return render_to_basehtml_response('main/about.html', RequestContext(request, locals()))


def admin(request):
    user_cnt = {
                'all':User.objects.all().count(),
                }
    room_cnt = {
                'all': Room.objects.all().count(),
                'empty': Room.objects.filter(status=0).count(),
                'order': Room.objects.filter(status=1).count()
                }
    article_cnt = Article.objects.all().count()
    order_cnt = {
                 'all': Order.objects.count(),
                 'pay': Order.objects.filter(status=1).count()
                 }
    return render_to_response('admin/admin.html', RequestContext(request, locals()))


def sitemap(request):
    return render_to_response('sitemap.html', RequestContext(request, locals()))


def easy_page(request, template):
    return render_to_response(template, RequestContext(request, locals()))


def site_update(request):
    command = '/tor.sh > /tor.log'
    log = logging.getLogger('log')
    timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.info('run command4:' + timestr)
    #os.system(command)
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return render_to_response('main/site_update.html', RequestContext(request, locals()))
