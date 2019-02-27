# pyMongoLab
Flask+Pymongo+apscheduler构建的一个Restful示例应用。在操作MongoDB数据库时，必须指定id内容，不可使用MongoDB默认的oid，否则会导致JSON解析失败。

## 使用组件

- Flask 应用服务器
- Flask_CORS 跨域访问 
- Pymongo 操作MongoDB数据库
- apscheduler 定时任务，启动其它进程


## 使用方法

```python

python setup.py build

python setup.py install

python api.py
