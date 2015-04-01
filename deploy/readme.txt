安装python环境：
	1、下载安装python
	从https://www.python.org/downloads/release
	2、配置环境变量
	我的电脑->属性->高级->环境变量->系统变量中的PATH追加c:\python27;c:\python27\scripts
	PATHEXT追加;.PY;.PYM
安装pip：
	3、安装Pip
	#下载https://bootstrap.pypa.io/ez_setup.py
	python ez_setup.py
	easy_install pip
安装依赖库：
	pip install -r requirements.txt