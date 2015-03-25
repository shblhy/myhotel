#!/usr/bin/env python
#-*- coding:utf-8 -*-


class FieldRender(object):
    def __init__(self, field):
        self.id = field.id_for_label
        self.value = field.data
        self.label = field.label

    def render(self):
        return ''


class SelectRender(FieldRender):
    def render(self):
        return u'''
        $('#%s').prepend('<option%s></option>');
        $('#%s').select2({
            placeholder : "选择%s...",
            minimumResultsForSearch: 18,
            allowClear : true
        }); ''' % (self.id, ' selected' if self.value in [None, ''] else '', self.id, self.label)


class InputRender(FieldRender):
    pass


class TreeRender(FieldRender):
    def __init__(self, field):
        self.default = field.field.default
        self.url = field.field.url
        super(TreeRender, self).__init__(field)

    def render(self):
        return u'''
            var tree_select = Tipped.create('#%(id)s_select', '%(id)s_container', {
                inline : true,
                showOn : 'click',
                hideOn : [{element:'self',event:'click'}],
                hideOnClickOutside:true,
                skin : 'white',
                hook : 'rightmiddle',
                radius:4,
                shadow: { blur: 5 },
                onShow:function(content,element){ $(element).addClass('select2-dropdown-open'); },
                onHide:function(content,element){$(element).removeClass('select2-dropdown-open');}
            });
            $('#%(id)s_container').on('click', 'a', function(){
                if($(this).hasClass('btn-primary')){
                  var values = $('#%(id)s').tree('getValues');
                    console.log(values);
                  if( $('#%(id)s_input').val() != values){
                      var text = $('#%(id)s').tree('getTexts');
                        $('#%(id)s_select').find('span').text(text);
                        $('#%(id)s_select').attr('title',text);
                        $('#%(id)s_input').val(values);
                  }
                  if(!values){
                      $('#%(id)s_select').find('span').html('中国');
                      $('#%(id)s_input').val('0');
                      tree_select.hide();
                  }else{
                      tree_select.hide();
                  }
                }else{
                    tree_select.hide();
                }
            });
            //地区树初始化
            $('#%(id)s').tree({
                data: %(default)s,
                checkbox:true,
                onBeforeExpand:function(node) {
                    $('#%(id)s').tree("options").url = "%(url)s"+node.id;
                },
                onExpand: function(node){
                }
            });
            //设置初始值
            var selected_names = $('#%(id)s').tree('getTexts');
            $('#%(id)s_select').find('span').text(selected_names == null? '中国' : selected_names);
            var selected_values = $('#%(id)s').tree('getValues');
            $('#%(id)s_input').val(selected_names == null? '0' : selected_values);
        ''' % {
            'id': self.id,
            'url': self.url,
            'default': self.default
        }


class FieldParam(object):
    def __init__(self, field):
        self.id = field.id_for_label
        self.name = field.name


class SelectParam(FieldParam):
    def param(self):
        return 'params["%s"] = $("#%s").select2("val");' % (self.name, self.id)


class InputParam(FieldParam):
    def param(self):
        return 'params["%s"] = $("#%s").val();' % (self.name, self.id)


class RenderFactory(object):
    render_dict = {
        'ModelChoiceField': SelectRender,
        'ChoiceField': SelectRender,
        'IPAddressField': InputRender,
        'CharField': InputRender,
        'TreeField': TreeRender,
    }

    param_dict = {
        'ModelChoiceField': SelectParam,
        'ChoiceField': SelectParam,
        'IPAddressField': InputParam,
        'CharField': InputParam,
    }

    @classmethod
    def init_render(cls, field):
        render_class = cls.render_dict.get(field.field.__class__.__name__)
        if render_class:
            return render_class(field)

    @classmethod
    def init_param(cls, field):
        param_class = cls.param_dict.get(field.field.__class__.__name__)
        if param_class:
            return param_class(field)