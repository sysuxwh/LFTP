使用手册：

0. Server和Client确保可以相互ping通（关掉防火墙）

1. 客户端需要先安装progressbar库，显示进度条
	pip install progressbar

2. Server需要修改FTP_server.py中的HOST为ip地址（可以为localhost）,默认的链接端口FTPPORT为3154，也可更改为其他可用端口

3. Server可以修改FTP_server.py中的PATH，PATH为存放文件的地方，供client下载/上传

3. Client可以修改FTP_client.py中的DOWNLOADPATH，即是下载后文件的存放路径