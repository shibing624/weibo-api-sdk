"""
测试工具函数
"""
import pytest
from weibo_api_sdk.utils.exception import (
    WeiboException,
    UnexpectedResponseException,
    GetDataErrorException,
    NeedLoginException,
    IdMustBeIntException,
)
from weibo_api_sdk.utils.utils import get_class_from_name
from weibo_api_sdk.utils.streaming import StreamingJSON


class TestExceptions:
    """测试异常类"""

    def test_weibo_exception(self):
        """测试基础异常"""
        exc = WeiboException("测试错误")
        assert str(exc) == "测试错误"

    def test_unexpected_response_exception(self):
        """测试意外响应异常"""
        from unittest.mock import Mock
        
        mock_response = Mock()
        mock_response.text = "错误的响应内容"
        
        exc = UnexpectedResponseException(
            url="https://test.com",
            res=mock_response,
            expect="JSON 数据"
        )
        
        assert "https://test.com" in str(exc)
        assert "JSON 数据" in str(exc)

    def test_get_data_error_exception_with_json_error(self):
        """测试数据获取错误异常（包含 JSON 错误信息）"""
        from unittest.mock import Mock
        
        mock_response = Mock()
        mock_response.text = '{"error": {"message": "测试错误消息"}}'
        mock_response.json.return_value = {
            "error": {"message": "测试错误消息"}
        }
        
        exc = GetDataErrorException(
            url="https://test.com",
            res=mock_response,
            expect="数据"
        )
        
        assert "测试错误消息" in str(exc)

    def test_get_data_error_exception_without_json_error(self):
        """测试数据获取错误异常（无 JSON 错误信息）"""
        from unittest.mock import Mock
        from json import JSONDecodeError
        
        mock_response = Mock()
        mock_response.text = "非 JSON 响应"
        mock_response.json.side_effect = JSONDecodeError("msg", "doc", 0)
        
        exc = GetDataErrorException(
            url="https://test.com",
            res=mock_response,
            expect="数据"
        )
        
        assert "Unknown error" in str(exc)

    def test_need_login_exception(self):
        """测试需要登录异常"""
        exc = NeedLoginException("test_method")
        assert "test_method" in str(exc)
        assert "login" in str(exc).lower()

    def test_id_must_be_int_exception(self):
        """测试 ID 必须是整数异常"""
        def test_func():
            pass
        
        exc = IdMustBeIntException(test_func)
        assert "test_func" in str(exc)
        assert "integer" in str(exc).lower()


class TestUtils:
    """测试工具函数"""

    def test_get_class_from_name_people(self):
        """测试获取 People 类"""
        from weibo_api_sdk.weibo.people import People
        cls = get_class_from_name('people')
        assert cls == People

    def test_get_class_from_name_status(self):
        """测试获取 Status 类"""
        from weibo_api_sdk.weibo.status import Status
        cls = get_class_from_name('status')
        assert cls == Status

    def test_get_class_from_name_article(self):
        """测试获取 Article 类"""
        from weibo_api_sdk.weibo.article import Article
        cls = get_class_from_name('article')
        assert cls == Article

    def test_get_class_from_name_case_insensitive(self):
        """测试类名大小写不敏感"""
        from weibo_api_sdk.weibo.people import People
        cls1 = get_class_from_name('people')
        cls2 = get_class_from_name('People')
        cls3 = get_class_from_name('PEOPLE')
        assert cls1 == cls2 == cls3 == People


class TestStreamingJSON:
    """测试 StreamingJSON 类"""

    def test_streaming_json_init_with_dict(self):
        """测试使用字典初始化"""
        data = {"name": "测试", "value": 123}
        sj = StreamingJSON(data)
        assert sj._json == data

    def test_streaming_json_init_with_list(self):
        """测试使用列表初始化"""
        data = [1, 2, 3, 4, 5]
        sj = StreamingJSON(data)
        assert sj._json == data

    def test_streaming_json_init_with_invalid_type(self):
        """测试使用无效类型初始化"""
        with pytest.raises(ValueError):
            StreamingJSON("invalid string")
        
        with pytest.raises(ValueError):
            StreamingJSON(123)

    def test_streaming_json_getattr_dict(self):
        """测试字典的属性访问"""
        data = {"name": "测试", "age": 18}
        sj = StreamingJSON(data)
        assert sj.name == "测试"
        assert sj.age == 18

    def test_streaming_json_getattr_nested_dict(self):
        """测试嵌套字典的属性访问"""
        data = {"user": {"name": "测试", "id": 123}}
        sj = StreamingJSON(data)
        assert isinstance(sj.user, StreamingJSON)
        assert sj.user.name == "测试"
        assert sj.user.id == 123

    def test_streaming_json_getitem_list(self):
        """测试列表的索引访问"""
        data = [10, 20, 30]
        sj = StreamingJSON(data)
        assert sj[0] == 10
        assert sj[1] == 20
        assert sj[2] == 30

    def test_streaming_json_getitem_list_with_dict(self):
        """测试包含字典的列表"""
        data = [{"name": "A"}, {"name": "B"}]
        sj = StreamingJSON(data)
        assert isinstance(sj[0], StreamingJSON)
        assert sj[0].name == "A"
        assert sj[1].name == "B"

    def test_streaming_json_iter_list(self):
        """测试列表迭代"""
        data = [1, 2, 3]
        sj = StreamingJSON(data)
        result = list(sj)
        assert result == [1, 2, 3]

    def test_streaming_json_iter_dict_list(self):
        """测试字典列表迭代"""
        data = [{"id": 1}, {"id": 2}]
        sj = StreamingJSON(data)
        result = list(sj)
        assert len(result) == 2
        assert all(isinstance(item, StreamingJSON) for item in result)

    def test_streaming_json_len(self):
        """测试长度"""
        data = [1, 2, 3, 4, 5]
        sj = StreamingJSON(data)
        assert len(sj) == 5
        
        data2 = {"a": 1, "b": 2}
        sj2 = StreamingJSON(data2)
        assert len(sj2) == 2

    def test_streaming_json_contains(self):
        """测试包含检查"""
        data = {"name": "测试", "age": 18}
        sj = StreamingJSON(data)
        assert "name" in sj
        assert "age" in sj
        assert "email" not in sj

    def test_streaming_json_bool(self):
        """测试布尔值"""
        sj_true = StreamingJSON([1, 2, 3])
        assert bool(sj_true) is True
        
        sj_false = StreamingJSON([])
        assert bool(sj_false) is False

    def test_streaming_json_raw_data(self):
        """测试 raw_data 方法"""
        data = {"name": "测试", "nested": {"value": 123}}
        sj = StreamingJSON(data)
        raw = sj.raw_data()
        
        # 应该返回副本
        assert raw == data
        assert raw is not data  # 不是同一个对象
        
        # 修改副本不应影响原对象
        raw["new_key"] = "new_value"
        assert "new_key" not in sj._json

    def test_streaming_json_keyword_conflict(self):
        """测试与 Python 关键字冲突的处理"""
        data = {"from": "sender", "import": "module"}
        sj = StreamingJSON(data)
        # 使用下划线后缀访问
        assert sj.from_ == "sender"
        assert sj.import_ == "module"

