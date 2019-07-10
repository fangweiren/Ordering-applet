# Ordering-applet
慕课网：Python Flask 构建基于微信小程序的订餐系统
==============================================
## 启动
* export ops_config=local | production && python manage.py runserver


## ERROR
点击登录提示：
```python
Do not have loginClick handler in current page: pages/login/login. Please make sure that loginClick \
handler has been defined in pages/login/login, or pages/login/login has been added into app.json
```

解决：[Do not have XXX handler in current page: pages/login/login](https://blog.csdn.net/qq_37568942/article/details/87937690)