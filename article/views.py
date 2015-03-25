#-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404,render_to_response
from article.models import Article
from admin import ArticleListManager
#from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseBadRequest
from libs.yhwork.response import HttpJsonResponse,render_to_csv_response
from django.template import RequestContext
from article.forms import ArticleForm
import json

def articles(request,contype='html'):
    condition = {}
    q = Article.objects.filter(**condition)
    table = ArticleListManager(
        queryset = q,
        paginate_by = 30,
        page = 1,
        accessors_out = {'action':lambda x:ArticleListManager.get_action(x,request.user)
                         },
    ).to_table()
    print table.get_columns()
    print table.get_rows()
    if contype == 'html':
        return render_to_response('article/articles.html',RequestContext(request,locals()))
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')
    elif contype == 'csv':
        return render_to_csv_response(u"店面列表.csv",table.to_csv())

def article_list(request,contype='html'):
    condition = {}
    q = Article.objects.filter(**condition)
    table = ArticleListManager(
        queryset = q,
        paginate_by = 30,
        page = 1,
        accessors_out = {'action':lambda x:ArticleListManager.get_action(x,request.user)
                         },
    ).to_table()
    print table.get_columns()
    print table.get_rows()
    if contype == 'html':
        return render_to_response('article/article_list.html',RequestContext(request,locals()))
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')
    elif contype == 'csv':
        return render_to_csv_response(u"店面列表.csv",table.to_csv())

def article_input(request,article_id=None):
    if article_id:
        article = get_object_or_404(Article,pk=article_id)
    else:
        article = Article()
    return render_to_response('article/article_input.html',RequestContext(request,locals()))

def article_detail(request,article_id):
    article = get_object_or_404(Article,pk=article_id)
    return render_to_response('article/article_detail.html',RequestContext(request,locals()))

def input_article(request):
    article_id = request.POST.get('article_id',None)
    article = get_object_or_404(Article,pk=article_id) if article_id else None
    form = ArticleForm(request.POST,instance = article)
    if form.is_valid():
        article = form.instance
        article.author_id = request.user.id
        article.save()
        return HttpResponse('{"status":"ok"}', content_type='text/json; charset=UTF-8')
    else:
        return HttpResponseBadRequest(form.errors_as_text(), content_type='text/json; charset=UTF-8')    

def delete_articles(request):
    return

'''
    table = ArticleTable(
        query=q,
        limit=form.cleaned_data['iDisplayLength'],
        offset=form.cleaned_data['iDisplayStart'],
        order_by=form.cleaned_data['orderBy']
    )
    return render_to_response('room/rooms.html',locals())
'''