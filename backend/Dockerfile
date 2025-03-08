FROM python:3.8-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings_prod

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev pkg-config netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 创建日志目录和日志文件
RUN mkdir -p /app/logs && touch /app/logs/django.log && chmod -R 777 /app/logs

# 创建静态文件目录
RUN mkdir -p /app/static && chmod -R 755 /app/static
RUN mkdir -p /app/media && chmod -R 755 /app/media

# 安装Python依赖
COPY requirements_en.txt .
RUN pip install --no-cache-dir -r requirements_en.txt

# 复制项目文件
COPY . .

# 确保logs目录存在并有正确的权限
RUN mkdir -p /app/logs && touch /app/logs/django.log && chmod -R 777 /app/logs

# 设置启动脚本权限
RUN chmod +x docker-entrypoint.sh

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 设置启动脚本
ENTRYPOINT ["./docker-entrypoint.sh"]

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "config.wsgi:application"] 