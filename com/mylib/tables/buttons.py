#!/usr/bin/env python
#-*- coding:utf-8 -*-


class Button(object):
    """ Table Button

    Attributes:
        text: 按钮名称
        btn_class: 按钮css样式
        icon: 按钮图标
        has_js: 是否有额外的js脚本

    """

    def __init__(self, text='Button', btn_class='pull-left small-margin-right', icon=''):
        self.text = text
        self.btn_class = btn_class
        self.icon = icon
        self.has_js = False

    def __attrs__(self):
        result = [
            '"text": "%s"' % self.text,
            '"btnClass": "%s"' % self.btn_class
        ]
        if self.icon:
            result.append('"ico": "%s"' % self.icon)
        return result

    def render_js(self):
        pass


class LinkButton(Button):
    """链接按钮"""

    def __init__(self, url, **kwargs):
        super(LinkButton, self).__init__(**kwargs)
        self.url = url

    def __attrs__(self):
        result = super(LinkButton, self).__attrs__()
        result.append("'fn': {'click': function(oSettings){functions.load_page('%s');}}" % self.url)
        return result


class DeleteButton(Button):
    """删除按钮"""

    def __init__(self, url):
        super(DeleteButton, self).__init__(
            text=u'删除',
            icon='icon-delete icon-white',
            btn_class='pull-left small-margin-right btn-danger',
        )
        self.url = url

    def __attrs__(self):
        result = super(DeleteButton, self).__attrs__()
        result.append(''''fn': {'click': function(oSettings){
            var values = oSettings.oInstance.fnGetSelected();
            if(values.length == 0) return false;
            var params = [];
            $.each(values, function(n, value) {
                params.push('id='+value);
            });
            $.ajax({
                url:"%s?" + params.join('&') ,
            }).done(
                function(data){$('#iframe').html(data);}
            );
        }}''' % self.url)
        return result


class ExportButton(Button):
    """导出按钮"""

    def __init__(self, url):
        super(ExportButton, self).__init__(
            text=u'导出',
            btn_class='pull-right btn-info export'
        )
        self.url = url

    def __attrs__(self):
        result = super(ExportButton, self).__attrs__()
        result.append(u''''fn': {
        'mousedown': function(oSettings){
            var param_list = [];
            var params = get_params()
            for(param in params) param_list.push(param + '=' + params[param]);
            var url = '%s';
            if(param_list.length > 0) url += '?' + param_list.join('&');
            $(this).attr({"href": url});
        },
        'click': function(oSettings){
            if (window.confirm('可能需要较长时间，您需要导出吗?')) window.location.href = $(this).attr("href");
            return false;
        }}''' % self.url)
        return result


class ImportButton(Button):
    """导入按钮"""

    def __init__(self, url):
        super(ImportButton, self).__init__(
            text=u'导入',
            icon='icon-add',
            btn_class='pull-left small-margin-right fileinput-button'
        )
        self.url = url
        self.has_js = True

    def render_js(self):
        return u'''
        $('.fileinput-button').append('<input id="fileupload" type="file" name="files[]" multiple>');
        $('#fileupload').fileupload({
            url: '%s',
            dataType: 'json',
            autoUpload: true,
            //不需要UI支持
            add: function(e, data) {
                var uploadErrors = [];
                var acceptFileTypes = /(\.)(csv)$/i;
                if(!acceptFileTypes.test(data.originalFiles[0]['name'])) {
                    uploadErrors.push('上传文件类型不支持');
                }
                if(data.originalFiles[0]['size'] > 512000) { //5120 / 1024 kb/m = 5m
                    uploadErrors.push('上传文件大于5M');
                }
                if(uploadErrors.length > 0) {
                    var info = '';
                    for(var index in uploadErrors){
                        if(uploadErrors[index])
                            info += '<span style="color:red;font-weight:bold;">'+uploadErrors[index]+'</span><br>';
                    }
                    Tipped.create('#fileupload', info, {
                        skin : 'white',
                        hideOnClickOutside:true,
                        showOn : false,
                        hideOn : false,
                        closeButton : true,
                        hook : 'topmiddle',
                        maxWidth : 190,
                        stem:false,
                        offset:{x:0}
                    }).show();
                } else {
                    data.submit();
                }
            },
            done: function (e, data) {

            }
        });
        ''' % self.url


def action_caller(route, *actions):
    """表格操作列的caller(返回的是一个回调方法)"""

    def caller(obj):
        ret = []
        for action in actions:
            if action == 'edit':
                ret.append(u'<a href="%s/%s/edit">编辑</a>' % (route, obj.pk))
            elif action == 'delete':
                # ret.append(u'<a href="%s/delete/" data-id="%s" class="delete">删除</a>' % (route, obj.id))
                ret.append(u'<a href="%s/delete?id=%s">删除</a>' % (route, obj.pk))
        return '&nbsp;&nbsp;&nbsp;&nbsp;'.join(ret)
    return caller