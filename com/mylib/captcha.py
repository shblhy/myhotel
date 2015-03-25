# -*- coding: utf-8 -*-
"""
###########################################
#  Created on 2013-07-09
#  @author: Tim.Wang
#  Description: 生成验证码
Usage:
    1. views.py 生成验证码

    @bpAuth.route( '/get_captcha' )
    def get_captcha():
        captcha = Captcha(session=session, img_width=100, img_height=29)
        return captcha.get_image()

    2. templates html页面

    <input type="text" name="captcha" id="captcha" />
    <img src="/auths/get_captcha" title="看不清？点击刷新图片" onclick="this.src='/auths/get_captcha';" />

    3. views.py 验证用户输入

    @bpAuth.route( '/login', methods = ['GET', 'POST'] )
    @templated( "login.html" )
    def login():
        captcha_input = _g('captcha')
        captcha = Captcha(session=session)
        if not captcha_input or not captcha.validate(captcha_input):
            return u'验证失败'
        else
            return u'验证成功'

###########################################
"""


import random
import StringIO
import os
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse


class Captcha(object):

    def __init__(self, session, img_width=120, img_height=30, type='_random_number', length=4):
        """
        Args:
            session: Flask session对象
            img_width: 验证码图片宽度
            img_heigth: 验证码图片高度
            type: 验证码类型：’_random_char_number'(字母数字混合), '_random_char'(字母), '_random_number'(数字)
            length: 验证码字符的个数
        """
        self.session = session
        self.img_width = img_width
        self.img_height = img_height
        self.type = type
        self.length = length

    def get_image(self):
        """
        生成验证码图片
        """

        captcha = self.get_captcha(self.type, self.length)
        self.session['captcha'] = captcha

        font_color = ['Green'] # 验证码字体颜色
        background = (random.randrange(230, 255),random.randrange(230, 255),random.randrange(230, 255)) # 随机背景颜色
        #font_path = os.path.join(os.path.abspath(__file__), '..', 'arial.ttf')   # 字体文件路径
        font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'arial.ttf')   # 字体文件路径

        img = Image.new('RGB',(self.img_width, self.img_height), background)
        draw = ImageDraw.Draw(img)

        # 干扰点
        for w in xrange(self.img_width):
            for h in xrange(self.img_height):
                tmp = random.randint(0, 50)
                if tmp > 47:
                    draw.point((w, h), fill=(0, 0, 0))

        # 干扰线
        for i in range(random.randrange(3,8)):
            line_color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
            xy = (
                random.randrange(0,int(self.img_width*0.2)),
                random.randrange(0,self.img_height),
                random.randrange(3*self.img_width/4,self.img_width),
                random.randrange(0,self.img_height),
                )
            draw.line(xy,fill=line_color,width=int(12*0.1))

        # 写验证码
        font_size = min(self.img_height, int(self.img_width / len(captcha)))  # 字体大小为图片高度的80%
        x = random.randrange(int(font_size*0.3), int(font_size*0.5)) #起始位置
        for i in captcha:
            m = random.randrange(4, int(font_size*0.2)) # 字体大小浮动
            font = ImageFont.truetype(font_path.replace('\\','/'), font_size + m)
            y = random.randrange(0, (self.img_height - font_size - m)*2)    # 上下浮动
            draw.text((x,y), i, font=font, fill=random.choice(font_color))
            x += font_size*random.uniform(0.8,1.1)  # 左右浮动

        buf = StringIO.StringIO()
        img.save(buf,'gif')
        buf.closed
        # response = make_response(buf.getvalue())
        response = HttpResponse(buf.getvalue(), 'image/gif')
        return response

    def validate(self, captcha_input):
        """
        验证用户输入的验证码是否正确
        """
        captcha = self.session.get('captcha')
        if not captcha:
            return False
        self.session.pop('captcha')
        return captcha.lower() == captcha_input.lower()

    def get_captcha(self, type='_random_char_number', length=4):
        """
        获取验证码字符
        """
        if hasattr(self, type):
            method = getattr(self, type)
            if callable(method): return method(length)
        return self._random_char_number(length)

    def _random_number(self, length):
        """
        生成随机数字
        """
        return ''.join([str(i) for i in random.sample(range(10), length)])

    def _random_char(self, length):
        """
        生成随机字符
        """
        lowercase_list = [chr(i) for i in range(ord('a'), ord('z')+1)]
        uppercase_list = [chr(i) for i in range(ord('A'), ord('Z')+1)]
        return ''.join(random.sample(lowercase_list+uppercase_list, length))

    def _random_char_number(self, length):
        """
        生成随机字符或数字
        """
        lowercase_list = [chr(i) for i in range(ord('a'), ord('z')+1)]
        uppercase_list = [chr(i) for i in range(ord('A'), ord('Z')+1)]
        number_list = [str(i) for i in range(0, 10)]
        return ''.join(random.sample(lowercase_list+uppercase_list+number_list, length))