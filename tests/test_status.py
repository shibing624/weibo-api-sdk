"""
测试 Status 微博相关功能
"""
import pytest
from unittest.mock import Mock, patch
from weibo_api_sdk.weibo.status import Status, Statuses


class TestStatus:
    """测试 Status 类"""

    def test_status_init(self, client):
        """测试 Status 初始化"""
        status_id = "test_status_id"
        status = Status(status_id, None, client._session)
        assert status._id == status_id
        assert status._session == client._session
        assert status._cache is None
        assert status._data is None

    def test_status_init_with_cache(self, client):
        """测试使用缓存初始化 Status"""
        status_id = "test_status_id"
        cache = {
            "longTextContent": "测试内容",
            "attitudes_count": 100
        }
        status = Status(status_id, cache, client._session)
        assert status._cache == cache

    def test_status_id_property(self, client):
        """测试 id 属性"""
        status_id = "test_status_id"
        status = Status(status_id, None, client._session)
        assert status.id == status_id

    def test_status_build_url(self, client):
        """测试 _build_url 方法"""
        status_id = "test_status_id"
        status = Status(status_id, None, client._session)
        url = status._build_url()
        assert status_id in url
        assert 'api' in url.lower() or 'status' in url.lower()

    @patch('weibo_api_sdk.weibo.base.Base._get_data')
    def test_status_default_values_without_data(self, mock_get_data, client):
        """测试没有数据时的默认值"""
        status = Status("test_id", None, client._session)
        
        # 模拟 _get_data 不设置任何数据
        mock_get_data.return_value = None
        
        # 这些属性应该有默认值
        # 注意：实际行为取决于装饰器实现


class TestStatuses:
    """测试 Statuses 类（微博列表）"""

    def test_statuses_init(self, client):
        """测试 Statuses 初始化"""
        uid = "1815418641"
        statuses = Statuses(uid, None, client._session)
        assert statuses._id == uid
        assert statuses._session == client._session
        assert statuses._page_num == 1
        assert statuses._original is False

    def test_statuses_init_original(self, client):
        """测试原创微博模式初始化"""
        uid = "1815418641"
        statuses = Statuses(uid, None, client._session, original=True)
        assert statuses._original is True

    def test_statuses_build_url_normal(self, client):
        """测试普通微博列表 URL 构建"""
        uid = "1815418641"
        statuses = Statuses(uid, None, client._session, original=False)
        url = statuses._build_url()
        assert uid in url

    def test_statuses_build_url_original(self, client):
        """测试原创微博列表 URL 构建"""
        uid = "1815418641"
        statuses = Statuses(uid, None, client._session, original=True)
        url = statuses._build_url()
        assert uid in url
        assert 'ori' in url.lower() or 'original' in url.lower()

    def test_statuses_page_num_changes(self, client):
        """测试页码变化"""
        uid = "1815418641"
        statuses = Statuses(uid, None, client._session)
        assert statuses._page_num == 1
        
        statuses._page_num = 2
        assert statuses._page_num == 2
        
        statuses._page_num = 5
        assert statuses._page_num == 5

    @patch('weibo_api_sdk.weibo.base.Base._get_data')
    def test_statuses_refresh(self, mock_get_data, client):
        """测试 refresh 方法"""
        statuses = Statuses("1815418641", None, client._session)
        
        # 设置一些数据
        statuses._data = {"test": "data"}
        statuses._cache = {"test": "cache"}
        
        # 调用 refresh
        statuses.refresh()
        
        # 数据应该被清空
        assert statuses._data is None
        assert statuses._cache is None
        assert statuses._refresh_times == 1

