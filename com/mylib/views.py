#-*- coding:utf-8 -*-
from fault.models import File
from InternetQOEmonitorSystemFront.common import get_request_params,login_on
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
from InternetQOEmonitorSystemFront.mytime import datetime_to_timestamp
from datetime import datetime
from InternetQOEmonitorSystemFront.settings import RESOURCE_ROOT_PATH,EXPORT_ENGINE_PATH,EXPORT_OUTFILE_PATH,WEBSITE_PORT
import os,json
from django.views.decorators.cache import never_cache
import subprocess

@login_on
def up_file(request):
    optional_params={'note':'','dir':('','',None,'ori')}
    params=get_request_params(request,None,optional_params)
    if not params.__class__==dict :
        return HttpResponseBadRequest(params, mimetype='application/javascript')
    if not request.FILES['file']:
        return HttpResponseBadRequest('必须提供文件', mimetype='application/javascript')
    res=[]
    for oriFile in request.FILES.getlist('file'):
        f = File()
        filename = os.path.basename(oriFile.name)
        timeStamp = datetime_to_timestamp(datetime.now())
        f.name = filename
        f.file = params['dir']+'/'+ timeStamp+'_'+str(request.FILES.getlist('file').index(oriFile))
        f.note=params['note']
        f.save()
        dirPath = os.path.join(os.path.join(RESOURCE_ROOT_PATH,'file'),params['dir'])
        if not os.path.isdir(dirPath):os.makedirs(dirPath)
        targetFile = os.path.join(dirPath,timeStamp+'_'+str(request.FILES.getlist('file').index(oriFile)))
        handler_file(targetFile,oriFile)
        res.append({'id':f.id,'name':filename})
    return HttpResponse(json.dumps(res), mimetype='application/javascript')

def handler_file(tarpath,orifile):
    open(tarpath, "wb").write(orifile.read())

@login_on
def download_file(request):
    necessary_params={'id':('',File,'file')}
    params = get_request_params(request, necessary_params, None)
    if not params.__class__ == dict:
        return HttpResponseBadRequest(params, mimetype='application/javascript')    
    return HttpResponseRedirect('/static_file/'+str(params['file'].file))

@login_on
@never_cache
def page_export(request,export_type="jpg"):
    '''将页面转化为图片导出'''
    #E:\soft\tool\phantomjs\phantomjs-1.9.7-windows\phantomjs.exe E:\soft\tool\phantomjs\phantomjs-1.9.7-windows\myex\myrender.js http://www.baidu.com E:\soft\tool\phantomjs\phantomjs-1.9.7-windows\baidu3.jpg
    #url = "http://www.baidu.com"
    url = request.get_full_path().replace("/export","http://127.0.0.1:"+str(WEBSITE_PORT),1)
    filename = datetime_to_timestamp(datetime.now()) + ".jpg"
    command = EXPORT_ENGINE_PATH + "\phantomjs.exe " + EXPORT_ENGINE_PATH + "\myex\myrender.js \"" + url +"\" "+ EXPORT_OUTFILE_PATH +"\\" + filename
    print command
    data=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    data.wait()
    picturePath = EXPORT_OUTFILE_PATH +"\\" + filename
    return HttpResponseRedirect(picturePath)