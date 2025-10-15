FROM        rockylinux:9.3.20231119
USER        root
RUN         /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

# 安装依赖
RUN         yum install -y python3.12 python3.12-devel python3.12-pip gcc net-tools

# 创建应用目录
RUN         mkdir /qytangfastapi
WORKDIR     /qytangfastapi

# 安装Python依赖
COPY        requirements.txt .
RUN         pip3.12 install -r requirements.txt --proxy http://192.168.20.100:7890

# 复制应用文件和证书
COPY        main.py .
COPY        fastapi.key .
COPY        fastapi.crt .

# HTTP模式，使用gunicorn+uvicorn
# Gunicorn 是一个成熟的 WSGI HTTP 服务器，主要用于管理多个进程（worker），
# 以提高应用在生产环境下的稳定性和并发处理能力；而 Uvicorn 则是一个专门针对 ASGI 协议的服务器，
# 适用于像 FastAPI 这样支持异步的现代 Python Web 框架。

# 在生产部署中，常见的做法是利用 Gunicorn 来作为进程管理器，
# 并通过指定 Uvicorn 作为 worker（例如使用命令 gunicorn -k uvicorn.workers.UvicornWorker app:app），
# 从而将 Gunicorn 的多进程管理优势与 Uvicorn 的异步处理能力结合起来，
# 这样既能提高应用的性能，也能更好地利用多核 CPU 的资源。
CMD         gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 旧配置，已被替换
#CMD         gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:443 --keyfile=fastapi-key.pem --certfile=fastapi.pem
#CMD         uvicorn main:app --host 0.0.0.0 --port=443 --ssl-keyfile=fastapi-key.pem --ssl-certfile=fastapi.pem --workers 10
#CMD         uvicorn main:app --host 0.0.0.0 --port=443 --ssl-keyfile=apifox.key --ssl-certfile=apifox.crt --workers 10