#!/bin/sh

# 等待数据库准备就绪
echo "Waiting for database..."
while ! nc -z db 3306; do
  sleep 1
done
echo "Database is ready!"

# 执行数据库迁移
echo "Applying database migrations..."
python manage.py migrate

# 创建超级用户（如果不存在）
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
"

# 收集静态文件
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 启动应用
echo "Starting application..."
exec "$@" 