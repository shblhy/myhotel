from django.shortcuts import render_to_response
from libs.yhwork.response import render_to_tmpl_response as render_to_tmpl_response


def render_to_basehtml_response(*args, **kwargs):
    return render_to_response(*args, **kwargs)
    head = '''{% extends "base.html" %}
    {% block content %}
    '''
    end = '''{% block content %}
    '''
    return render_to_tmpl_response((head,end),*args, **kwargs)

def render_to_baseadminhtml_response(*args, **kwargs):
    return render_to_response(*args, **kwargs)
    head = '''{% extends "baseadmin.html" %}
    {% block content %}
    '''
    end = '''{% block content %}
    '''
    return render_to_tmpl_response((head,end),*args, **kwargs)