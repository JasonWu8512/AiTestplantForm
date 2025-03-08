# 项目脚本文件

本文件夹包含了项目的辅助脚本文件，主要用于在Windows环境下提供便捷的命令行操作。

## 脚本文件说明

### Docker相关脚本

- **docker-menu.bat**: Docker操作主菜单，提供了启动、停止、查看日志等功能的菜单界面
- **start-docker.bat**: 启动Docker服务
- **stop-docker.bat**: 停止Docker服务
- **logs-docker.bat**: 查看Docker服务的日志
- **rebuild-docker.bat**: 重新构建Docker服务

### 本地开发脚本

- **run_backend.bat**: 在本地环境中运行后端服务
- **run_frontend.bat**: 在本地环境中运行前端服务
- **start_frontend.bat**: 启动前端服务的简化脚本
- **start-backend-cmd.bat**: 在CMD中启动后端服务
- **start-with-cmd.bat**: 提供了一个菜单来选择启动不同的服务

## 使用说明

1. 这些脚本文件主要用于开发和调试阶段，提供便捷的命令行操作。
2. 在生产环境中，建议直接使用Docker命令或Docker Compose命令。
3. 如果您熟悉Docker命令，可以不使用这些脚本文件。

## 注意事项

1. 这些脚本文件假设您已经安装了Docker和Docker Compose。
2. 部分脚本需要在项目根目录下运行才能正常工作。
3. 如果遇到路径问题，请检查脚本中的相对路径是否正确。 