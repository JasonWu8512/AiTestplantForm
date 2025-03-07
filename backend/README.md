# AiTestPlantForm 后端

AiTestPlantForm是一个基于AI的测试平台，旨在提高测试效率和质量。

## 项目结构

```
backend/
├── apps/                  # 应用模块
│   ├── users/             # 用户管理
│   ├── projects/          # 项目管理
│   ├── testcases/         # 测试用例
│   ├── testplans/         # 测试计划
│   └── executions/        # 测试执行
├── config/                # 配置文件
├── utils/                 # 工具模块
│   ├── constants.py       # 常量定义
│   ├── exceptions.py      # 异常处理
│   ├── helpers.py         # 辅助函数
│   ├── middleware.py      # 中间件
│   ├── pagination.py      # 分页
│   ├── permissions.py     # 权限
│   └── validators.py      # 验证器
├── manage.py              # Django管理脚本
└── requirements.txt       # 依赖包列表
```

## 技术栈

- Python 3.8+
- Django 3.2
- Django REST Framework 3.12
- MySQL 5.7+
- Redis 6.0+
- Celery 5.1

## 安装与运行

### 环境准备

1. 安装Python 3.8+
2. 安装MySQL 5.7+
3. 安装Redis 6.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 数据库配置

1. 创建MySQL数据库
```sql
CREATE DATABASE aitestplantform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改`config/settings.py`中的数据库配置

### 运行迁移

```bash
python manage.py migrate
```

### 创建超级用户

```bash
python manage.py createsuperuser
```

### 运行开发服务器

```bash
python manage.py runserver
```

## API文档

启动服务器后，访问以下URL查看API文档：

- Swagger UI: http://localhost:8000/api/swagger/
- ReDoc: http://localhost:8000/api/redoc/

## 测试

运行单元测试：

```bash
python manage.py test
```

## 部署

### 使用Docker部署

1. 构建Docker镜像
```bash
docker build -t aitestplantform-backend .
```

2. 运行容器
```bash
docker run -d -p 8000:8000 aitestplantform-backend
```

### 使用Docker Compose部署

```bash
docker-compose up -d
```

## 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅 [LICENSE](LICENSE) 文件 