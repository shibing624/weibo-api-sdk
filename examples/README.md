# Weibo API SDK 使用示例

这个目录包含了 weibo-api-sdk 的使用示例，帮助您快速上手。

## 示例列表

### 1. basic_usage.py - 基本使用示例

演示了 Weibo API SDK 的核心功能：

- **获取用户信息**: 包括昵称、简介、性别、粉丝数等
- **获取用户微博**: 获取用户发布的微博列表
- **获取用户文章**: 获取用户的文章列表
- **获取粉丝列表**: 查看用户的粉丝
- **获取关注列表**: 查看用户关注的人
- **获取微博详情**: 获取单条微博的详细信息

#### 安装依赖

```bash
# 方法1：从 PyPI 安装
pip install weibo-api-sdk

# 方法2：从源码安装
cd weibo-api-sdk
pip install -e .
```

#### 配置 Cookie

**方法1：使用 .env 文件（推荐）**

1. 复制配置文件模板：
```bash
cp .env.example .env
```

2. 获取微博 Cookie：
   - 访问 [https://m.weibo.cn](https://m.weibo.cn) 并登录（可选但推荐）
   - 按 `F12` 打开开发者工具 → `Network` 标签页
   - 刷新页面，找到任意请求
   - 在请求头中找到 `Cookie`，复制完整值

3. 编辑 `.env` 文件，将 Cookie 填入：
```bash
WEIBO_COOKIE=your_actual_cookie_string_here
```

4. 运行示例：
```bash
python examples/basic_usage.py
```

**方法2：使用环境变量**

```bash
# Linux / macOS
export WEIBO_COOKIE="your_cookie_here"
python examples/basic_usage.py

# Windows PowerShell
$env:WEIBO_COOKIE="your_cookie_here"
python examples/basic_usage.py
```

#### 修改示例参数

在运行示例之前，可以修改用户ID：

```python
# 在 basic_usage.py 中修改
uid = "1815418641"  # 替换为你想查询的微博用户ID
```

## ⚠️ 重要：关于 Cookie

由于微博的反爬虫机制，直接访问 API 会返回 432 状态码。**必须配置 Cookie** 才能正常使用。

### 为什么需要 Cookie？

- 微博使用反爬虫机制保护其 API
- 没有 Cookie 会返回空响应（432 状态码）
- Cookie 可以让请求看起来像来自真实浏览器

### Cookie 安全提示

⚠️ **重要安全提醒**：
- `.env` 文件已添加到 `.gitignore`，不会被提交到 Git
- 不要将 Cookie 分享给他人
- Cookie 包含登录凭证，泄露可能导致账号被盗
- 定期更新 Cookie（通常几天到几周过期一次）

详细说明请参见：[HOW_TO_GET_COOKIE.md](../HOW_TO_GET_COOKIE.md)

## 获取用户ID

要使用这些示例，您需要知道微博用户的 ID。以下是几种获取方法：

1. **通过微博主页URL**: 
   - 访问用户主页，URL 通常为 `https://weibo.com/u/[USER_ID]`
   - USER_ID 即为所需的用户ID

2. **通过移动端URL**:
   - 移动端主页 URL 格式：`https://m.weibo.cn/u/[USER_ID]`

## API 功能概览

### WeiboClient 主要方法

```python
from weibo_api_sdk import WeiboClient

client = WeiboClient()

# 用户相关
people = client.people(uid)              # 获取用户信息
followers = client.followers(uid)        # 获取粉丝列表
follows = client.follow(uid)             # 获取关注列表

# 微博相关
status = client.status(status_id)        # 获取微博详情
statuses = client.statuses(uid)          # 获取用户全部微博
origin_statuses = client.origin_statuses(uid)  # 获取用户原创微博

# 文章相关
article = client.article(article_id)     # 获取文章详情
articles = client.articles(uid)          # 获取用户文章列表
```

### People 对象属性

```python
people = client.people(uid)

people.id                # 用户ID
people.name              # 昵称
people.description       # 简介
people.gender            # 性别
people.avatar            # 头像URL
people.followers_count   # 粉丝数
people.follow_count      # 关注数
people.statuses          # 用户的微博
people.articles          # 用户的文章
people.followers         # 用户的粉丝
people.follows           # 用户关注的人
```

### Status 对象属性

```python
status = client.status(status_id)

status.id                  # 微博ID
status.longTextContent     # 长文本内容
status.attitudes_count     # 点赞数
status.comments_count      # 评论数
status.reposts_count       # 转发数
```

### Statuses 对象方法

```python
statuses = client.statuses(uid)

statuses.total                      # 微博总数
statuses.page(page_num)            # 获取指定页
statuses.page_from_to(from_page, to_page)  # 获取指定范围页
statuses.all()                      # 获取全部微博
```

## 注意事项

1. **请求频率**: 请合理控制请求频率，避免对微博服务器造成过大压力
2. **错误处理**: 示例中包含了基本的错误处理，实际使用时请根据需要完善
3. **数据变化**: 微博的 API 可能会发生变化，如遇到问题请查看项目主页
4. **隐私保护**: 使用时请遵守相关法律法规，尊重用户隐私

## 更多示例

如果您有其他使用场景的示例需求，欢迎提交 Issue 或 Pull Request！

## 问题反馈

如果在使用过程中遇到问题，请在 GitHub 上提交 Issue：
https://github.com/shibing624/weibo-api-sdk/issues

