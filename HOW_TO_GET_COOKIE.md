# 如何获取微博 Cookie

由于微博的反爬虫机制，API 请求可能返回 432 状态码。为了正常使用，您需要提供浏览器的 Cookie。

## 方法一：从浏览器获取（推荐）

### Chrome / Edge 浏览器

1. 打开 [https://m.weibo.cn](https://m.weibo.cn)
2. 按 `F12` 打开开发者工具
3. 切换到 `Network` (网络) 标签页
4. 刷新页面 (`F5`)
5. 在网络请求列表中找到任意一个请求（通常是 API 请求）
6. 在右侧的 `Headers` (请求头) 中找到 `Cookie` 字段
7. 复制完整的 Cookie 值

### Firefox 浏览器

1. 打开 [https://m.weibo.cn](https://m.weibo.cn)
2. 按 `F12` 打开开发者工具
3. 切换到 `网络` 标签页
4. 刷新页面 (`F5`)
5. 在网络请求列表中选择任意一个请求
6. 在右侧的 `请求头` 中找到 `Cookie`
7. 复制完整的 Cookie 值

### Safari 浏览器

1. 打开 Safari -> 偏好设置 -> 高级
2. 勾选"在菜单栏中显示开发菜单"
3. 打开 [https://m.weibo.cn](https://m.weibo.cn)
4. 点击菜单栏 `开发` -> `显示网页检查器`
5. 切换到 `网络` 标签页
6. 刷新页面
7. 选择任意请求，在右侧找到 Cookie

## 方法二：使用浏览器扩展

可以使用 Cookie 管理扩展来导出 Cookie：

- **EditThisCookie** (Chrome/Edge)
- **Cookie-Editor** (Firefox)

## 使用 Cookie

获取到 Cookie 后，在代码中这样使用：

```python
from weibo_api import WeiboClient

# 方式1：在初始化时提供 Cookie
cookie = "your_cookie_string_here"
client = WeiboClient(cookie=cookie)

# 方式2：使用环境变量（推荐）
import os
cookie = os.getenv('WEIBO_COOKIE')
client = WeiboClient(cookie=cookie)

# 然后正常使用
user = client.people('1815418641')
print(user.name)
```

## 注意事项

1. **Cookie 安全**
   - 不要将 Cookie 提交到 Git 仓库
   - 不要在公共场合分享 Cookie
   - Cookie 包含您的登录凭证，泄露可能导致账号安全问题

2. **Cookie 有效期**
   - Cookie 会过期，通常几天到几周不等
   - 如果出现 401/403 错误，需要重新获取 Cookie

3. **使用建议**
   - 使用环境变量存储 Cookie
   - 定期更新 Cookie
   - 为脚本创建专门的小号账户

## 使用环境变量存储 Cookie

### Linux / macOS

```bash
# 临时设置（当前终端会话）
export WEIBO_COOKIE="your_cookie_here"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export WEIBO_COOKIE="your_cookie_here"' >> ~/.zshrc
source ~/.zshrc
```

### Windows (PowerShell)

```powershell
# 临时设置
$env:WEIBO_COOKIE="your_cookie_here"

# 永久设置
[Environment]::SetEnvironmentVariable("WEIBO_COOKIE", "your_cookie_here", "User")
```

### Windows (CMD)

```cmd
# 临时设置
set WEIBO_COOKIE=your_cookie_here

# 永久设置
setx WEIBO_COOKIE "your_cookie_here"
```

## 使用 .env 文件（推荐）

1. 安装 python-dotenv：
```bash
pip install python-dotenv
```

2. 创建 `.env` 文件：
```
WEIBO_COOKIE=your_cookie_here
```

3. 在代码中使用：
```python
from dotenv import load_dotenv
import os
from weibo_api import WeiboClient

load_dotenv()
cookie = os.getenv('WEIBO_COOKIE')
client = WeiboClient(cookie=cookie)
```

4. 将 `.env` 添加到 `.gitignore`：
```bash
echo ".env" >> .gitignore
```

## 常见问题

### Q: 还是返回 432 错误？
A: 
1. 确认 Cookie 是最新的
2. 检查 Cookie 格式是否完整
3. 尝试在浏览器中访问 API URL，确认可以正常访问
4. Cookie 可能包含特殊字符，确保正确转义

### Q: 获取的数据不完整？
A: 可能是 Cookie 权限不足，尝试：
1. 在微博网站登录
2. 获取新的 Cookie
3. 确认账号没有被限制

### Q: 需要登录吗？
A: 对于公开信息，理论上不需要登录。但实际上，微博的反爬虫机制可能需要Cookie验证。建议使用登录后的 Cookie。

