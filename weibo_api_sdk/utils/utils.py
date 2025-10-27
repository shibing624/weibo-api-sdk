import importlib

from .exception import UnimplementedException


def get_class_from_name(name, module_filename=None):
    """从类名获取对应的类对象"""
    cls_name = name.capitalize() if name.islower() else name
    file_name = module_filename or cls_name.lower()
    try:
        imported_module = importlib.import_module(
            f'.{file_name}',
            'weibo_api.weibo'
        )
        return getattr(imported_module, cls_name)
    except (ImportError, AttributeError):
        raise UnimplementedException(f'Unknown weibo obj type [{name}]')


def build_weibo_obj_from_dict(data, session, use_cache=True, cls=None):
    """从字典数据构建微博对象"""
    obj_id = data.id
    return cls(obj_id, data if use_cache else None, session)
