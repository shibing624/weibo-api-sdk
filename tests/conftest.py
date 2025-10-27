"""
Pytest 配置和共享 fixtures
"""
import pytest
import os
from unittest.mock import Mock, MagicMock
from weibo_api_sdk import WeiboClient


@pytest.fixture
def mock_cookie():
    """模拟 Cookie"""
    return "SUB=test_sub; SUBP=test_subp"


@pytest.fixture
def client(mock_cookie):
    """创建测试客户端"""
    return WeiboClient(cookie=mock_cookie)


@pytest.fixture
def client_no_cookie():
    """创建无 Cookie 的测试客户端"""
    return WeiboClient()


@pytest.fixture
def mock_session():
    """模拟 requests.Session"""
    session = MagicMock()
    session.headers = {}
    return session


@pytest.fixture
def sample_user_response():
    """示例用户 API 响应"""
    return {
        "ok": 1,
        "data": {
            "userInfo": {
                "id": 1815418641,
                "screen_name": "测试用户",
                "description": "这是一个测试用户",
                "gender": "m",
                "avatar_hd": "https://example.com/avatar.jpg",
                "followers_count": 1000,
                "follow_count": 500,
            }
        }
    }


@pytest.fixture
def sample_status_response():
    """示例微博 API 响应"""
    return {
        "ok": 1,
        "data": {
            "longTextContent": "这是一条测试微博的长文本内容",
            "attitudes_count": 100,
            "comments_count": 50,
            "reposts_count": 25,
        }
    }


@pytest.fixture
def sample_statuses_response():
    """示例微博列表 API 响应"""
    return {
        "ok": 1,
        "data": {
            "cards": [
                {
                    "mblog": {
                        "id": "test_id_1",
                        "text": "测试微博1",
                        "created_at": "2024-01-01 12:00:00",
                        "user": {
                            "id": 1815418641,
                            "screen_name": "测试用户"
                        }
                    }
                },
                {
                    "mblog": {
                        "id": "test_id_2",
                        "text": "测试微博2",
                        "created_at": "2024-01-02 12:00:00",
                        "user": {
                            "id": 1815418641,
                            "screen_name": "测试用户"
                        }
                    }
                }
            ],
            "cardlistInfo": {
                "total": 100
            }
        }
    }


@pytest.fixture
def env_cookie(monkeypatch):
    """设置环境变量中的 Cookie"""
    test_cookie = "ENV_SUB=test; ENV_SUBP=test"
    monkeypatch.setenv("WEIBO_COOKIE", test_cookie)
    return test_cookie

