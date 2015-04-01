#-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from libs.djex.response import HttpJsonResponse, render_to_csv_response
from apps.article.models import Article
from apps.article.forms import ArticleForm, ArticleQForm
from apps.article.admin import ArticleListManager


#@admin_required
def articles(request, contype='html'):
    form = ArticleQForm(request.GET)
    if form.is_valid():
        conditions = form.get_conditions()
    q = Article.objects.select_related('author').filter(**conditions)
    table = ArticleListManager(
        queryset=q,
        paginate_by=form.cleaned_data['iDisplayLength'],
        page=form.cleaned_data['iDisplayStart'] / form.cleaned_data['iDisplayLength'] + 1,
        accessors_out={'action': lambda x: ArticleListManager.get_action(x, request.user.is_superuser)},
    ).to_table()
    if contype == 'html':
        return render_to_response('article/articles.html', RequestContext(request, locals()))
    elif contype == 'table':
        return HttpResponse(table.get_rows(), content_type='application/json; charset=UTF-8')
    elif contype == 'csv':
        return render_to_csv_response(u"文章列表.csv", table.to_csv())


def article_list(request, contype='html'):
    condition = {}
    articles = Article.objects.filter(**condition).order_by('-edit_time')[:20]
    return render_to_response('article/article_list.html', RequestContext(request, locals()))


def article_input(request, article_id=None):
    if article_id:
        action = 'edit'
        article = get_object_or_404(Article, pk=article_id)
    else:
        action = 'add'
        article = Article()
    return render_to_response('article/article_input.html', RequestContext(request, locals()))


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render_to_response('article/article_detail.html', RequestContext(request, locals()))


def input_article(request):
    article_id = request.POST.get('article_id', None)
    article = get_object_or_404(Article, pk=article_id) if article_id else None
    form = ArticleForm(request.POST, instance=article)
    if form.is_valid():
        article = form.instance
        article.author_id = request.user.id
        article.save()
        return HttpJsonResponse('{"status":"ok"}')
    else:
        return HttpResponseBadRequest(form.errors_as_text(), content_type='application/json; charset=UTF-8')


def delete_articles(request):
    try:
        Article.objects.filter(id__in=request.POST['ids'].split(',')).delete()
        return HttpJsonResponse('')
    except Exception, e0:
        return HttpResponseBadRequest(u'删除失败:' + e0.message, content_type='application/javascript')