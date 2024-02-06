基本信息： 收集商家出售产品名录，用于分析商品程序

1、 collection 是项目的执行程序， 包含商家名称、产品、发布、直播店等信息程序

2、CollectionNum是操作界面初始定位元素

3、collectionException 是自定义的异常

4、common 是环境相关，包含日志和环境

5、config是配置文件：config是环境配置， elements是商家分类, log.conf 是日志文件配置

6、log是日志存储

7、pgDataBase是postgresql存储相关函数、类

8、celery_config.py 是celery配置文件

9、start_app_multitasking是celery并发

10、start_app_single是单个设备环境

启动条件：

1、安装adb环境

2、pip install -r requirement.txt

3、python -m uiautomator2 init() 在设备上安装atx uiautomator

4、celery --app=celery_worker worker -l info

5、运行start_app_multitasking.py {单设备直接运行start_app_single.py}


启动步骤：

1、在启动条件部分安装完adb之后， 进入adb目录下，adb start-server; adb devices -l列出所有的devices

2、启动条件中第四步会启动celery工作， 之后使用celery --app=celery_worker flower --port=***就可以启动flower进行web查看

3、 在终端启动start_app_multitasking.py {python start_app_multitasking.py}即可启动运行
