# Weibo API SDK

一个免登陆获取新浪微博数据的Python库，简单易用

[![PyPI version](https://img.shields.io/pypi/v/weibo-api-sdk.svg)](https://pypi.org/project/weibo-api-sdk/)
[![Python Version](https://img.shields.io/pypi/pyversions/weibo-api-sdk.svg)](https://pypi.org/project/weibo-api-sdk/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/weibo-api-sdk.svg)](https://pypi.org/project/weibo-api-sdk/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/shibing624/weibo-api-sdk)

## 特性

- 🚀 简单易用的 API 接口
- 📦 免登陆获取微博数据
- 🎯 支持获取用户信息、微博列表、文章、粉丝、关注等
- 🐍 纯 Python 3.8+ 实现
- 📝 完整的代码示例
- ✅ 完善的单元测试

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install weibo-api-sdk
```

### 从源码安装

```bash
git clone https://github.com/shibing624/weibo-api-sdk.git
cd weibo-api-sdk
pip install -e .
```

### 开发模式安装

```bash
pip install -e ".[dev]"  # 包含开发工具
```

## 快速开始

### ⚠️ 重要提示

由于微博的反爬虫机制，**必须提供 Cookie** 才能正常访问 API。

### 配置步骤

1. **复制配置文件**
```bash
cp .env.example .env
```

2. **获取 Cookie**
   - 访问 [https://m.weibo.cn](https://m.weibo.cn) 并登录
   - 按 `F12` 打开开发者工具
   - 切换到 `Network` 标签，刷新页面
   - 找到任意请求，复制 `Cookie` 值

3. **编辑 .env 文件**
```bash
WEIBO_COOKIE=your_actual_cookie_string_here
```

详细教程请参见：[HOW_TO_GET_COOKIE.md](HOW_TO_GET_COOKIE.md)

### 代码示例

```python
from weibopy import WeiboClient  # 注意：导入用 weibopy，安装用 weibo-api-sdk
from dotenv import load_dotenv
import os

# 加载 .env 文件中的配置
load_dotenv()

# 创建客户端（会自动读取 WEIBO_COOKIE 环境变量）
cookie = os.getenv('WEIBO_COOKIE')
client = WeiboClient(cookie=cookie)

# 获取用户信息
user = client.people('5623741644')  # 用户ID
print(f"用户名: {user.name}")
print(f"用户简介: {user.description}")
print(f"关注数: {user.follow_count}")
print(f"粉丝数: {user.followers_count}")

# 获取用户最新微博
print("\n最近发布的微博：")
for status in user.statuses.page(1):
    print(f"微博ID: {status.id}")
    print(f"发布时间: {status.created_at}")
    print(f"内容: {status.text}")
    print(f"点赞数: {status.attitudes_count}")
    print(f"评论数: {status.comments_count}")
    print(f"转发数: {status.reposts_count}")
    print("-" * 50)

# 获取粉丝列表
print("\n粉丝列表：")
for follower in user.followers.page(1):
    print(f"- {follower.name}")

# 获取关注列表
print("\n关注列表：")
for follow in user.follows.page(1):
    print(f"- {follow.name}")

# 获取文章列表
print("\n文章列表：")
for article in user.articles.page(1):
    print(f"- {article.text}")
```

## 示例代码

更多详细示例请查看 [examples](examples/) 目录：

- [basic_usage.py](examples/basic_usage.py) - 基本使用示例，包含所有核心功能

### 运行示例

1. 配置 Cookie（参见上方配置步骤）
2. 运行示例：

```bash
python examples/basic_usage.py
```

output:

<img src="https://github.com/shibing624/weibo-api-sdk/blob/master/docs/basic_demo_snap.png" width="500" />
**注意**：示例代码会自动从 `.env` 文件读取 Cookie 配置。

## API 文档

### WeiboClient

主要的客户端类，用于创建各种微博对象。

#### 方法

- `people(uid)` - 获取用户信息
- `status(status_id)` - 获取微博详情
- `statuses(uid)` - 获取用户全部微博列表
- `origin_statuses(uid)` - 获取用户原创微博列表
- `article(article_id)` - 获取文章详情
- `articles(uid)` - 获取用户文章列表
- `followers(uid)` - 获取粉丝列表
- `follow(uid)` - 获取关注列表

### People 对象

用户对象，包含用户的基本信息和相关数据。

#### 属性

- `id` - 用户ID
- `name` - 昵称
- `description` - 简介
- `gender` - 性别
- `avatar` - 头像URL
- `followers_count` - 粉丝数
- `follow_count` - 关注数
- `statuses` - 微博列表
- `articles` - 文章列表
- `followers` - 粉丝列表
- `follows` - 关注列表

### Status 对象

微博对象，包含微博的详细信息。

#### 属性

- `id` - 微博ID
- `text` - 微博内容
- `created_at` - 发布时间
- `source` - 发布来源
- `attitudes_count` - 点赞数
- `comments_count` - 评论数
- `reposts_count` - 转发数
- `user` - 发布用户
- `pic_urls` - 图片URL列表

## 注意事项

- 请合理控制请求频率，避免对微博服务器造成过大压力
- `page(n)` 方法用于获取指定页的数据
- `all()` 方法会获取所有数据，对于数据量大的用户请谨慎使用
- 所有 API 都是免登陆的，但受微博反爬虫机制限制

## 开发

### 环境要求

- Python 3.8+
- requests >= 2.10.0
- python-dotenv >= 0.19.0

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/shibing624/weibo-api-sdk.git
cd weibo-api-sdk

# 安装开发依赖
pip install -e ".[dev]"

# 或使用 requirements.txt
pip install -r requirements.txt
```

### 运行测试

项目包含完整的单元测试套件，使用 pytest 进行测试。

```bash
# 运行所有测试
pytest

# 运行测试并显示详细信息
pytest -v

# 运行测试并生成覆盖率报告
pytest --cov=weibo_api_sdk --cov-report=html --cov-report=term

# 运行特定测试文件
pytest tests/test_client.py

# 运行特定测试类
pytest tests/test_client.py::TestWeiboClient

# 运行特定测试方法
pytest tests/test_client.py::TestWeiboClient::test_client_init_with_cookie
```

### 测试结构

```
tests/
├── __init__.py           # 测试包初始化
├── conftest.py           # pytest 配置和共享 fixtures
├── test_base.py          # 测试 Base 基类
├── test_client.py        # 测试 WeiboClient 客户端
├── test_people.py        # 测试用户相关功能
├── test_status.py        # 测试微博相关功能
└── test_utils.py         # 测试工具函数和异常
```

### 测试覆盖率

测试覆盖了以下主要功能：

- ✅ 客户端初始化和配置
- ✅ Cookie 处理和请求头设置
- ✅ 用户信息获取和属性访问
- ✅ 微博列表获取和分页
- ✅ 粉丝和关注列表
- ✅ 数据缓存机制
- ✅ 异常处理
- ✅ 工具函数和 StreamingJSON

### 代码格式化

```bash
# 使用 black 格式化代码
black weibo_api_sdk/

# 检查代码风格
flake8 weibo_api_sdk/

# 类型检查
mypy weibo_api_sdk/
```

## 贡献指南

欢迎贡献代码！请确保：

1. 添加适当的测试用例
2. 运行所有测试并确保通过：`pytest`
3. 使用 black 格式化代码：`black .`
4. 更新相关文档

## TODO

- [ ] 搜索接口
- [ ] 根据用户昵称创建用户
- [ ] 头条文章获取优化
- [ ] 文章评论功能
- [ ] 完善文档
- [x] 添加单元测试 ✅
- [ ] 添加更多示例
- [ ] 增加测试覆盖率到 90%+
- [ ] 添加 GitHub Actions CI/CD

## 联系方式

- **GitHub Issues**: [报告问题或功能请求](https://github.com/shibing624/weibo-api-sdk/issues)
- **邮箱**: xuming624@qq.com
- **微信**: xuming624（备注：姓名-公司-Weibo）

<p align="center">
  <img src="https://github.com/shibing624/weibo-api-sdk/blob/master/docs/wechat.jpeg" width="200" />
</p>
## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
