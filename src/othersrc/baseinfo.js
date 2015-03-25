$.presenters['/middleman/baseinfo'] = function(){
    // 加载模版
    var $templates = $(new EJS({url: '/static/template/baseinfo.ejs'}).text);
    var baseinfoData = {
        middleman_type: '',
        name: '',
        short_name: '',
        contact: '',
        contact_num : '',
        email: '',
        tel: '',
        address: ''
    };
    var baseinfoInit = function(){
        $.ajax({
            'type': 'get',
            'url': '/middleman/get/baseinfo?middleman_id=' + middleman_id,
            success: function (data) {
                if (data.status == 1) {
                    $.extend(baseinfoData, data.data);
                    baseInfo
                    .value(baseinfoData)
                    .render();
                    // 基础信息用户名及号码
                    $('.J-middleman-name').text(baseinfoData.middleman_name);
                    $('.J-middleman-phone-num').text(baseinfoData.middleman_phone_num);
                } else if (data.msg) {
                    $.alert(data.msg);
                }
            }
        });
    };
    var baseInfo = $('.J-baseinfo-form')
    .wine()
    .setTemplate({ text : $templates.find('.J-baseinfo-template').html() })
    .setValidate([{ 
        name:'name',
        rule: util.regexp.companyName,
        success: util.validateSuccess,
        fail: util.validateFail
    },{ 
        name:'short_name',
        rule: util.regexp.companyShortName,
        success: util.validateSuccess,
        fail: util.validateFail
    },{ 
        name:'email',
        rule: util.regexp.email,
        success: util.validateSuccess,
        fail: util.validateFail
    },{ 
        name:'tel',
        rule: util.regexp.tel,
        success: util.validateSuccess,
        fail: util.validateFail
    },{ 
        name:'address',
        rule: util.regexp.address,
        success: util.validateSuccess,
        fail: util.validateFail
    },{ 
        name:'contact',
        rule: util.regexp.companyShortName,
        success: util.validateSuccess,
        fail: util.validateFail
    },{ 
        name:'contact_num',
        rule: util.regexp.tel,
        success: util.validateSuccess,
        fail: util.validateFail
    }])
    .afterRender(function(){
        var self = this,
        $parent = self.parent,
        data = self.data;
        $parent.find('.input-box').inputBox();
        $parent.find(':radio[wine-bind=middleman_type][value=' + data.middleman_type + ']').trigger('change');
        $parent.find('.J-baseinfo-save').click(function(){
            if( data['middleman_type'] == 1 && !self.validate()){
                return false;
            }
            if (data['middleman_type'] == 2 && ( !self.validate('contact') || !self.validate('contact_num') )) {
                return false;
            }
            data.middleman_id = middleman_id;
            $.ajax({
                'type': 'post',
                'url': '/middleman/modify/baseinfo',
                data: {
                    parameter: JSON.stringify(data)
                },
                success: function (data) {
                    if (data.status == 1) {
                        $.alert('修改成功');
                    } else if (data.msg) {
                        $.alert(data.msg);
                    }
                }
            });
        });
    })
    .binding({
        'middleman_type' : function(data){
            var $parent = this.parent,
                $company = $parent.find('.J-middle-company');
            if (data.value == 2) {
                $company.addClass('hide');
            } else {
                $company.removeClass('hide');
            }
        },
        'name' : function(){
            this.validate('name');
        },
        'short_name' : function(){
            this.validate('short_name');
        },
        'contact' : function(){
            this.validate('contact');
        },
        'contact_num' : function(){
            this.validate('contact_num');
        },
        'tel' : function(){
            this.validate('tel');
        },
        'email' : function(){
            this.validate('email');
        },
        'address' : function(){
            this.validate('address');
        }
    });

    baseinfoInit();

    // 密码修改
    $('<div>').appendTo('body').wine()
    .setTemplate({ text : $templates.find('.J-password-popup').html() })
    .value({
        old_pwd: '',
        new_pwd: '',
        new_pwd_repeat
    })
    .setValidate([{ 
        name:'old_pwd',
        rule: util.regexp.password,
        success: util.validateSuccess,
        fail: util.validateFail
    },{ 
        name:'old_pwd',
        rule: util.regexp.password,
        success: util.validateSuccess,
        fail: util.validateFail
    }])
}