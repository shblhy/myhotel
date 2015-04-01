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
初始化数据库：
	在根目录下建立data目录，并放置db.sqlite3文件即可。
	db.sqlite3从mysql产生：
		python manage.py dumpdata > data.json --settings=settings_dev （数据导出）
		python manage.py sysncdb
		删除所有表的数据，再重新导入
		python manage.py loaddata data.json --settings=settings_light （数据导入）
sqlite数据库查看管理：
	SQLiteSpy 1.2M绿色软件（http://www.yunqa.de/delphi/doku.php/products/sqlitespy/index）