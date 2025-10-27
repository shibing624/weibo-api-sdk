"""
测试 People 用户相关功能
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from weibo_api_sdk.weibo.people import People, Peoples


class TestPeople:
    """测试 People 类"""

    def test_people_init(self, client):
        """测试 People 初始化"""
        uid = "1815418641"
        people = People(uid, None, client._session)
        assert people._id == uid
        assert people._session == client._session
        assert people._cache is None
        assert people._data is None

    def test_people_init_with_cache(self, client):
        """测试使用缓存初始化 People"""
        uid = "1815418641"
        cache = {"userInfo": {"id": uid, "screen_name": "测试用户"}}
        people = People(uid, cache, client._session)
        assert people._cache == cache

    def test_people_id_property(self, client):
        """测试 id 属性"""
        uid = "1815418641"
        people = People(uid, None, client._session)
        # id 属性应该返回传入的 uid
        assert people._id == uid

    @patch('weibo_api_sdk.weibo.base.Base._get_data')
    def test_people_get_data_called_when_no_cache(self, mock_get_data, client, sample_user_response):
        """测试没有缓存时会调用 _get_data"""
        uid = "1815418641"
        people = People(uid, None, client._session)
        
        # 模拟 _get_data 设置 _data
        def set_data():
            people._data = sample_user_response['data']
        mock_get_data.side_effect = set_data
        
        # 访问 userInfo 属性应该触发 _get_data
        _ = people.userInfo
        mock_get_data.assert_called_once()

    def test_people_build_url(self, client):
        """测试 _build_url 方法"""
        uid = "1815418641"
        people = People(uid, None, client._session)
        url = people._build_url()
        assert uid in url
        assert 'api' in url.lower() or 'container' in url.lower()

    def test_people_with_complete_cache(self, client):
        """测试使用完整缓存的 People"""
        cache = {
            "userInfo": {
                "id": 1815418641,
                "screen_name": "测试用户",
                "description": "测试简介",
                "gender": "m",
                "avatar_hd": "https://example.com/avatar.jpg",
                "followers_count": 1000,
                "follow_count": 500,
            }
        }
        people = People("1815418641", cache, client._session)
        assert people._cache == cache


class TestPeoples:
    """测试 Peoples 类（粉丝/关注列表）"""

    def test_peoples_init_follower(self, client):
        """测试 Peoples 初始化（粉丝模式）"""
        uid = "1815418641"
        peoples = Peoples(uid, None, client._session, utype='follower')
        assert peoples._id == uid
        assert peoples._utype == 'follower'
        assert peoples._page_num == 1

    def test_peoples_init_follow(self, client):
        """测试 Peoples 初始化（关注模式）"""
        uid = "1815418641"
        peoples = Peoples(uid, None, client._session, utype='follow')
        assert peoples._utype == 'follow'

    def test_peoples_build_url_follower(self, client):
        """测试粉丝列表 URL 构建"""
        uid = "1815418641"
        peoples = Peoples(uid, None, client._session, utype='follower')
        url = peoples._build_url()
        assert uid in url
        assert 'follower' in url.lower() or 'fans' in url.lower()

    def test_peoples_build_url_follow(self, client):
        """测试关注列表 URL 构建"""
        uid = "1815418641"
        peoples = Peoples(uid, None, client._session, utype='follow')
        url = peoples._build_url()
        assert uid in url
        assert 'follow' in url.lower()

    def test_peoples_page_num_changes(self, client):
        """测试页码变化"""
        uid = "1815418641"
        peoples = Peoples(uid, None, client._session)
        assert peoples._page_num == 1
        
        peoples._page_num = 2
        assert peoples._page_num == 2

