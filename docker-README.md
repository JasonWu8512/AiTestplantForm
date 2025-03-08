# Docker部署指南

本文档提供了使用Docker部署测试平台的详细说明。

## 前提条件

- 安装Docker：[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- 安装Docker Compose：[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## 快速开始

1. 克隆项目仓库：

```bash
git clone <repository-url>
cd AiTestPlantForm
```

2. 配置环境变量：

编辑`.env`文件，根据需要修改环境变量。

3. 构建并启动服务：

```bash
docker-compose up -d
```

4. 访问应用：

- 前端：http://localhost
- 后端API：http://localhost/api/
- API文档：http://localhost/api/swagger/

5. 默认超级用户：

- 用户名：admin
- 密码：admin123

## 服务说明

本项目包含以下Docker服务：

- **backend**：Django后端服务
- **frontend**：Vue前端服务
- **db**：MySQL数据库服务
- **redis**：Redis缓存服务
- **celery-worker**：Celery Worker服务
- **celery-beat**：Celery Beat服务

## 常用命令

### 启动所有服务

```bash
docker-compose up -d
```

### 查看服务日志

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除卷（慎用，会删除数据）
docker-compose down -v
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec db mysql -u testuser -p
```

## 数据备份与恢复

### 备份数据库

```bash
docker-compose exec db mysqldump -u root -p testplatform > backup.sql
```

### 恢复数据库

```bash
cat backup.sql | docker-compose exec -T db mysql -u root -p testplatform
```

## 生产环境部署注意事项

1. 修改`.env`文件中的敏感信息，特别是密码和密钥。
2. 设置`DEBUG=False`以禁用调试模式。
3. 更新`ALLOWED_HOSTS`以包含您的域名。
4. 配置HTTPS以确保安全通信。
5. 定期备份数据库。

## 故障排除

### 服务无法启动

检查日志以获取详细错误信息：

```bash
docker-compose logs <service-name>
```

### 数据库连接问题

确保数据库服务已启动，并且环境变量配置正确：

```bash
docker-compose ps
```

### 权限问题

如果遇到权限问题，可以尝试以下命令：

```bash
# 修复媒体目录权限
docker-compose exec backend chmod -R 777 /app/media
```

## 更新应用

1. 拉取最新代码：

```bash
git pull
```

2. 重新构建并启动服务：

```bash
docker-compose up -d --build
```

## 联系与支持

如有问题或需要支持，请联系项目维护者。 