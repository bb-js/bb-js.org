bb-js.org
==================

是从 `Backbonejs入门教程第二版 <https://github.com/the5fire/backbonejs-learning-note>`_ 中最终演化的 `Wechat <https://github.com/the5fire/wechat>`_ 项目fork出来的。打算搞一个Backbonejs的中文社区，开发者除了可以在里面交流技术，还是通过技术共同构建社区——实践技术。


本地运行此项目
-------------------------

::

    git clone https://github.com/bb-js/bb-js.org
    cd bb-js.org && pip install -r requirements.txt
    cd src
    python init_sqlite.py
    python bb_server.py

然后打开浏览器输入http://127.0.0.1:8080，就能看到了。


如何贡献代码
-------------------------

1. fork一份到你的仓库中
2. 从你的仓库clone到本地： ``git clone git@github.com:yourname/bb-js.org``
3. 发现bug时: ``git checkout -b fix-<some>-bug`` ,修改完bug，push到github
4. 然后在你fork的项目上就能看到一个pull-request的按钮，点它，之后安装提示操作。
5. 更新你的仓库和官方一致。创建一个upstream（上游）的源： ``git remote add upstream https://github.com/bb-js/bb-js.org`` ::

    用来更新官方代码到你的fork仓库中，通过该命令：
    git pull upstream master
    git merge upstream/master
