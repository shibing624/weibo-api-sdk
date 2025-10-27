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

### 2. follow_network.py - 关注网络爬取示例

递归爬取用户的关注网络，构建社交关系图谱：

- **多层级爬取**: 从起始用户开始，递归获取3层关注关系
- **数据去重**: 自动去除重复用户，避免重复爬取
- **进度显示**: 实时显示爬取进度和统计信息
- **JSONL 输出**: 将用户信息保存为标准 JSONL 格式
- **错误处理**: 自动处理异常，中断后可恢复部分数据
- **频率控制**: 自动添加延迟，避免请求过快被限制

**输出字段**：`id`, `name`, `description`, `gender`, `avatar`, `followers_count`, `follow_count`

**⚠️ 注意**：此操作可能需要 10-30 分钟，请耐心等待

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

#### 运行示例

```bash
# 基本使用示例
python examples/basic_usage.py

# 关注网络爬取示例（需要较长时间）
python examples/follow_network.py
```

#### 修改示例参数

在运行示例之前，可以修改用户ID：

```python
# 在 basic_usage.py 中修改
uid = "1815418641"  # 替换为你想查询的微博用户ID

# 在 follow_network.py 中修改
start_uid = "1815418641"  # 起始用户ID
max_depth = 3  # 爬取深度（层数）
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

## 数据格式说明

### JSONL 格式

`follow_network.py` 输出的 JSONL 文件格式：

```jsonl
{"id": "1815418641", "name": "杨洋", "description": "演员", "gender": "m", "avatar": "https://...", "followers_count": 55924000, "follow_count": 356}
{"id": "1234567890", "name": "用户名", "description": "简介", "gender": "f", "avatar": "https://...", "followers_count": 1000, "follow_count": 500}
```

每行一个 JSON 对象，可以使用以下方式读取：

```python
import json

# 读取 JSONL 文件
with open('follow_network.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        user = json.loads(line)
        print(f"{user['name']}: {user['description']}")
```

### 数据分析示例

```python
import json
import pandas as pd

# 转换为 DataFrame
users = []
with open('follow_network.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        users.append(json.loads(line))

df = pd.DataFrame(users)

# 统计分析
print(f"总用户数: {len(df)}")
print(f"平均粉丝数: {df['followers_count'].mean():.0f}")
print(f"平均关注数: {df['follow_count'].mean():.0f}")

# 找出粉丝数最多的前10个用户
top_users = df.nlargest(10, 'followers_count')[['name', 'followers_count']]
print("\n粉丝数 TOP 10:")
print(top_users)
```

## 性能和限制

### 请求频率

- **基本示例**: 快速执行，约 10-30 秒
- **关注网络爬取**: 较慢执行，约 10-30 分钟
  - 自动添加 0.5-1 秒延迟
  - 避免触发微博反爬虫限制

### 数据量预估

以 `follow_network.py` 为例（3层深度）：

- **层级 0**: 1 个用户（起始用户）
- **层级 1**: ~200 个用户（关注列表，10页×20）
- **层级 2**: ~1,200 个用户（第1层的关注，3页×20×20）
- **层级 3**: ~400 个用户（第2层的关注，1页×20×20）

**预计总数**: 约 1,800+ 个用户（去重后可能更少）

### 注意事项

1. **Cookie 有效期**: Cookie 通常几天到几周过期，需要定期更新
2. **请求限制**: 微博可能限制请求频率，遇到错误会自动跳过
3. **数据准确性**: 部分用户可能设置隐私，无法获取完整信息
4. **中断恢复**: 使用 Ctrl+C 中断时会保存已获取的数据

## 更多示例

如果您有其他使用场景的示例需求，欢迎提交 Issue 或 Pull Request！

## 问题反馈

如果在使用过程中遇到问题，请在 GitHub 上提交 Issue：
https://github.com/shibing624/weibo-api-sdk/issues

