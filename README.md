# 1. LFTP
一个基于UDP实现的大文件可靠传输协议，使用python实现。

# 2. 架构设计
将LFTP分解为两个板块。

## 2.1 TCP
TCP板块使用UDP模拟实现可靠传输、流控制和拥塞控制。提供可靠传输的接口供FTP调用。
- 发送方——sender。
- 接收方——receiver。

## 2.2 FTP
FTP板块负责调用TCP板块提供的可靠传输接口，进行文件传输。需要实现文件分片、重组以及多客户端支持、用户交互等。
- 客户端——client。
- 服务端——server。

---

**注：server和每个client都既是sender也是receiver。**

---

## 2.3 接口设计
TCP板块提供以下接口供FTP调用：

- 用于绑定和连接接收方的ip地址和端口。连接成功返回true，失败返回false。
```python
sender.connect(remoteIP, remotePort) -> bool
```

- 用于发送方发送数据，message必须是bytes。发送成功返回true，失败返回false。
```python
sender.send(message) -> bool
```

- 用于接收方绑定本地端口。绑定成功返回true，端口被占用返回false。
```python
receiver.bind(localPort) -> bool
```

- 用于接收方接收数据。该方法阻塞，直到接收到数据包，返回一个处理好的数据包。
```python
receiver.receive() -> bytes
```

## 2.4 分工
- 谢涛：TCP
- 谢玮鸿：FTP

# 3. 测试

## 3.1 上传文件
## 3.2 下载文件
## 3.3 流控制
## 3.4 拥塞控制
## 3.5 多客户端