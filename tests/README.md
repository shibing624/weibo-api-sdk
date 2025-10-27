# 测试说明

本目录包含 Weibo API SDK 的单元测试。

## 测试结构

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

## 运行测试

### 安装依赖

```bash
# 安装开发依赖（包含 pytest）
pip install -e ".[dev]"
```

### 运行所有测试

```bash
# 基本运行
pytest

# 详细输出
pytest -v

# 显示测试覆盖率
pytest --cov=weibo_api_sdk --cov-report=term

# 生成 HTML 覆盖率报告
pytest --cov=weibo_api_sdk --cov-report=html
# 然后打开 htmlcov/index.html 查看
```

### 运行特定测试

```bash
# 运行特定文件
pytest tests/test_client.py

# 运行特定测试类
pytest tests/test_client.py::TestWeiboClient

# 运行特定测试方法
pytest tests/test_client.py::TestWeiboClient::test_client_init_with_cookie

# 运行匹配模式的测试
pytest -k "client"
```

### 其他有用选项

```bash
# 显示打印输出
pytest -s

# 在第一个失败时停止
pytest -x

# 显示最慢的 10 个测试
pytest --durations=10

# 并行运行测试（需要 pytest-xdist）
pytest -n auto
```

## 测试覆盖

### test_client.py

测试客户端初始化和基本功能：
- ✅ Cookie 设置和处理
- ✅ 默认请求头配置
- ✅ 各种对象创建方法
- ✅ 会话持久性

### test_people.py

测试用户相关功能：
- ✅ People 对象初始化
- ✅ 缓存机制
- ✅ URL 构建
- ✅ Peoples（粉丝/关注列表）功能

### test_status.py

测试微博相关功能：
- ✅ Status 对象初始化
- ✅ Statuses 列表功能
- ✅ 原创微博模式
- ✅ 分页功能

### test_utils.py

测试工具函数：
- ✅ 异常类（WeiboException 及子类）
- ✅ get_class_from_name 函数
- ✅ StreamingJSON 类（属性访问、迭代、长度等）

### test_base.py

测试 Base 基类：
- ✅ 初始化和属性
- ✅ 数据获取流程
- ✅ JSON 解析和错误处理
- ✅ 刷新机制
- ✅ pure_data 属性

## Fixtures

`conftest.py` 提供了以下共享 fixtures：

- `mock_cookie` - 模拟 Cookie 字符串
- `client` - 带 Cookie 的测试客户端
- `client_no_cookie` - 无 Cookie 的测试客户端
- `mock_session` - 模拟的 requests.Session
- `sample_user_response` - 示例用户 API 响应
- `sample_status_response` - 示例微博 API 响应
- `sample_statuses_response` - 示例微博列表响应
- `env_cookie` - 环境变量中的 Cookie

## 测试最佳实践

### 使用 Mock

测试中使用 `unittest.mock` 来模拟网络请求：

```python
from unittest.mock import Mock, patch

@patch('requests.Session.request')
def test_something(mock_request):
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_request.return_value = mock_response
    # 测试代码...
```

### 使用 Fixtures

利用 fixtures 减少重复代码：

```python
def test_client_init(client):
    # client 由 conftest.py 提供
    assert client._session is not None
```

### 测试异常

使用 `pytest.raises` 测试异常：

```python
import pytest

def test_invalid_input():
    with pytest.raises(ValueError):
        # 触发异常的代码
        pass
```

## 添加新测试

当添加新功能时，请：

1. 在相应的测试文件中添加测试方法
2. 如果需要，在 `conftest.py` 中添加新的 fixtures
3. 确保测试覆盖：
   - 正常情况
   - 边界情况
   - 错误处理

示例：

```python
def test_new_feature(client):
    """测试新功能"""
    # Arrange（准备）
    expected = "expected_value"
    
    # Act（执行）
    result = client.new_feature()
    
    # Assert（断言）
    assert result == expected
```

## 持续集成

项目使用 GitHub Actions 进行持续集成，每次提交都会自动运行测试。

配置文件：`.github/workflows/tests.yml`

## 常见问题

### Q: 测试需要真实的 Cookie 吗？
A: 不需要。单元测试使用 mock 模拟 API 响应，不会发送真实请求。

### Q: 如何调试失败的测试？
A: 使用 `pytest -v -s` 查看详细输出，或在测试中添加 `import pdb; pdb.set_trace()` 设置断点。

### Q: 测试运行很慢怎么办？
A: 
- 使用 `pytest -n auto` 并行运行（需要安装 pytest-xdist）
- 只运行相关的测试文件
- 检查是否有真实的网络请求（应该都是 mock）

## 参考资料

- [pytest 官方文档](https://docs.pytest.org/)
- [unittest.mock 文档](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov 文档](https://pytest-cov.readthedocs.io/)

