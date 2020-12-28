### 数据模型
**student**
见 django/app/models
### 需要实现的接口

直接在 django/app/plugin.py 中实现这些接口即可

existById
getStudentByName
getStudentById
createStudent
deleteById


### 图片
规格 300*450

占位图生成器：https://oktools.net/placeholder

### 依赖安装
根目录 pip install -r requirements.txt

### 混合版
server端运行`socket version/multi-socket-all.py`，client端运行`django/manage.py`。
即可在网页进行交互。

### Socket Version
分为两个部分，server和client。其中server.py与client.py为基于单线程实现；multi开头的为多线程实现。

#### Server的运行方法
直接`python server.py`,或者在ide中打开。

#### Client的运行方法
直接`python client.py`,或者在ide中打开。
在多线程调试时，可以开两个窗口同时运行`python multi-client.py`和`python multi-client2.py`。

#### TODO
1. （单client）极端情形下（如命令错误）server端与client端的error detection。
2. （多client）Read after Write情形下的文件锁与同步问题。
3. （可视化）Django可以做Socket Programming吗...
4. Payload与用户交互的进一步优化。
