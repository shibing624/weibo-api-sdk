"""
测试 Base 基类
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from weibo_api_sdk.weibo.base import Base
from weibo_api_sdk.utils.exception import GetDataErrorException


class ConcreteBase(Base):
    """用于测试的具体 Base 子类"""
    
    def _build_url(self):
        return f"https://test.com/api?id={self._id}"


class TestBase:
    """测试 Base 基类"""

    def test_base_init(self, client):
        """测试 Base 初始化"""
        obj_id = "test_id"
        cache = {"test": "cache"}
        base = ConcreteBase(obj_id, cache, client._session)
        
        assert base._id == obj_id
        assert base._cache == cache
        assert base._session == client._session
        assert base._data is None
        assert base._refresh_times == 0

    def test_base_init_without_cache(self, client):
        """测试不使用缓存初始化"""
        base = ConcreteBase("test_id", None, client._session)
        assert base._cache is None

    def test_base_id_property(self, client):
        """测试 id 属性"""
        obj_id = "test_id_123"
        base = ConcreteBase(obj_id, None, client._session)
        assert base._id == obj_id

    def test_base_build_url(self, client):
        """测试 _build_url 方法"""
        obj_id = "test_id_456"
        base = ConcreteBase(obj_id, None, client._session)
        url = base._build_url()
        assert "test.com" in url
        assert obj_id in url

    def test_base_method_default(self, client):
        """测试默认 HTTP 方法"""
        base = ConcreteBase("test_id", None, client._session)
        assert base._method() == 'GET'

    def test_base_build_params_default(self, client):
        """测试默认参数为 None"""
        base = ConcreteBase("test_id", None, client._session)
        assert base._build_params() is None

    def test_base_build_data_default(self, client):
        """测试默认数据为 None"""
        base = ConcreteBase("test_id", None, client._session)
        assert base._build_data() is None

    @patch('requests.Session.request')
    def test_base_get_data_success(self, mock_request, client):
        """测试成功获取数据"""
        base = ConcreteBase("test_id", None, client._session)
        
        # 模拟成功的 API 响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "ok": 1,
            "data": {"id": "test_id", "name": "测试"}
        }
        mock_request.return_value = mock_response
        
        # 调用 _get_data
        base._get_data()
        
        # 验证数据被正确提取
        assert base._data is not None
        assert base._data["id"] == "test_id"
        assert base._data["name"] == "测试"

    @patch('requests.Session.request')
    def test_base_get_data_without_data_field(self, mock_request, client):
        """测试响应中没有 data 字段的情况"""
        base = ConcreteBase("test_id", None, client._session)
        
        # 模拟没有 data 字段的响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "test_id",
            "name": "测试"
        }
        mock_request.return_value = mock_response
        
        base._get_data()
        
        # 应该使用整个 JSON 作为 data
        assert base._data is not None
        assert "id" in base._data

    @patch('requests.Session.request')
    def test_base_get_data_json_decode_error(self, mock_request, client):
        """测试 JSON 解析错误"""
        from json import JSONDecodeError
        
        base = ConcreteBase("test_id", None, client._session)
        
        mock_response = Mock()
        mock_response.json.side_effect = JSONDecodeError("msg", "doc", 0)
        mock_response.text = "Invalid JSON"
        mock_request.return_value = mock_response
        
        with pytest.raises(GetDataErrorException):
            base._get_data()

    def test_base_refresh(self, client):
        """测试 refresh 方法"""
        base = ConcreteBase("test_id", None, client._session)
        
        # 设置一些数据
        base._data = {"test": "data"}
        base._cache = {"test": "cache"}
        
        # 刷新
        base.refresh()
        
        # 数据应该被清空
        assert base._data is None
        assert base._cache is None
        assert base._refresh_times == 1
        
        # 再次刷新
        base.refresh()
        assert base._refresh_times == 2

    def test_base_pure_data_with_cache(self, client):
        """测试 pure_data 属性（有缓存）"""
        cache = {"cached": "value"}
        base = ConcreteBase("test_id", cache, client._session)
        
        pure = base.pure_data
        assert "cache" in pure
        assert "data" in pure
        assert pure["cache"] == cache

    @patch.object(ConcreteBase, '_get_data')
    def test_base_pure_data_without_cache(self, mock_get_data, client):
        """测试 pure_data 属性（无缓存）"""
        base = ConcreteBase("test_id", None, client._session)
        
        # 模拟 _get_data 设置数据
        def set_data():
            base._data = {"fetched": "value"}
        mock_get_data.side_effect = set_data
        
        pure = base.pure_data
        
        # 应该调用 _get_data
        mock_get_data.assert_called_once()
        assert pure["data"] == {"fetched": "value"}

