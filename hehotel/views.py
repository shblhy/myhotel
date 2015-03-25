from django.shortcuts import render_to_response

#from django.contrib.auth.decorators import login_required
from member.models import User
from room.models import Room
from order.models import Order
from article.models import Article
from common import render_to_basehtml_response
def index(request):
    return render_to_response('index.html',locals())

def hotel(request):
    return render_to_basehtml_response('main/hotel.html',locals())

def order(request):
    return render_to_basehtml_response('main/order.html',locals())

def rooms(request):
    return render_to_basehtml_response('main/rooms.html',locals())

def pictures(request):
    return render_to_basehtml_response('main/pictures.html',locals())

def special_offers(request):
    return render_to_basehtml_response('main/special_offers.html',locals())

def about(request):
    return render_to_basehtml_response('main/about.html',locals())

#@login_required
def admin(request):
    user_cnt = {
                'all':User.objects.all().count(),
                }
    room_cnt = {
                'all':Room.objects.all().count(),
                'empty':Room.objects.filter(status=0).count(),
                'order':Room.objects.filter(status=1).count()
                }
    article_cnt = Article.objects.all().count()
    order_cnt = {
                 'all':Order.objects.count(),
                 'pay':Order.objects.filter(status=1).count()
                 }
    return render_to_response('admin/admin.html',locals())

def sitemap(request):
    return render_to_response('sitemap.html',locals())

def easy_page(request,template):
    return render_to_response(template,locals())