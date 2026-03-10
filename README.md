# OA系统后端

## 项目介绍

这是一个基于Django的企业级OA系统后端，提供用户认证、请假管理、通知管理、员工管理等核心功能。系统采用模块化设计，支持RESTful API接口，可与前端框架无缝集成。

## 技术栈

- **后端框架**：Django 5.2.8
- **API框架**：Django REST Framework 3.15.1
- **数据库**：MySQL
- **缓存**：Redis
- **异步任务**：Celery 5.6.2
- **认证**：JWT
- **加密**：AES
- **部署**：uWSGI

## 项目结构

```
oaback/
├── apps/                # 功能模块
│   ├── oauth/           # 用户认证模块
│   ├── absent/          # 请假管理模块
│   ├── inform/          # 通知管理模块
│   ├── staff/           # 员工管理模块
│   ├── image/           # 图片管理模块
│   └── home/            # 首页模块
├── oaback/              # 项目配置
├── media/               # 媒体文件
├── static/              # 静态文件
├── templates/           # 模板文件
├── utils/               # 工具类
├── manage.py            # 管理脚本
├── requirements.txt     # 依赖文件
└── uwsgi.ini            # uWSGI配置
```

## 核心功能

### 1. 用户认证系统
- 自定义用户模型（OAUser）
- JWT token认证
- 邮箱激活
- 密码重置
- 用户状态管理（激活、未激活、锁定）

### 2. 请假管理系统
- 多种请假类型
- 完整的审批流程
- 请假状态跟踪（审批中、通过、拒绝）
- 请假记录管理

### 3. 通知管理系统
- 部门通知
- 全员通知
- 通知阅读状态跟踪
- 按时间排序

### 4. 员工管理系统
- 部门管理
- 员工信息管理
- 批量导入/导出员工数据
- 权限控制

### 5. 图片管理系统
- 图片上传
- 媒体文件存储

## 安装与部署

### 1. 环境要求
- Python 3.10+
- MySQL 5.7+
- Redis 6.0+

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库配置

在项目根目录创建 `.env` 文件，配置数据库连接信息：

```
DB_NAME=oa
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
CACHE_URL=redis://localhost:6379/3
```

### 4. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 初始化数据

```bash
# 初始化部门
python manage.py initdepartments

# 初始化用户
python manage.py inituser

# 初始化请假类型
python manage.py initabsenttype
```

### 6. 启动服务

#### 开发环境

```bash
python manage.py runserver
```

#### 生产环境

```bash
uwsgi --ini uwsgi.ini
```

## API文档

### 认证接口
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/reset_pwd/` - 密码重置

### 请假接口
- `GET /api/absent/` - 获取请假列表
- `POST /api/absent/` - 提交请假申请
- `PUT /api/absent/{id}/` - 更新请假状态（审批）

### 通知接口
- `GET /api/inform/` - 获取通知列表
- `POST /api/inform/` - 创建通知
- `POST /api/inform/{id}/read/` - 标记通知已读

### 员工接口
- `GET /api/staff/` - 获取员工列表
- `POST /api/staff/` - 新增员工
- `PUT /api/staff/{id}/` - 更新员工信息
- `GET /api/staff/download/` - 下载员工数据
- `POST /api/staff/upload/` - 上传员工数据

### 图片接口
- `POST /api/image/upload/` - 上传图片

## 安全特性

- JWT token认证
- AES加密激活链接
- 权限控制（基于用户角色）
- CORS跨域配置
- 密码加密存储

## 性能优化

- Redis缓存热点数据
- Celery异步处理邮件发送
- 数据库查询优化（select_related、prefetch_related）
- 分页查询

## 测试

```bash
python manage.py test
```

## 贡献指南

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

## 许可证

MIT License
