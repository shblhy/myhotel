文档更新：
	make html 即可。
	后续会将rst文件散布到各模块内，编写py脚本收集再生成文档，更方便文档处理。
	认同 文档也是源码。
	
sphinx文档初始化（团队有一人处理即可）：
	pip install Sphinx==1.2.3
	执行sphinx-quickstart（参考sphinx.txt）
	sphinx-apidoc -o ./docs/source ./
	修改conf.py文件，正确设置django环境变量。