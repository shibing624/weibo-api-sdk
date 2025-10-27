#!/usr/bin/env python
"""
Weibopy - 一个免登陆获取新浪微博数据的Python库

使用 setup.py 用于兼容性，推荐使用 pyproject.toml
"""
from setuptools import setup, find_packages
import os


def read_file(filename):
    """读取文件内容"""
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()


# 读取版本号
version = {}
with open("weibopy/__init__.py", encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, version)
            break

setup(
    name='weibopy',
    version=version.get('__version__', '0.1.0'),
    packages=find_packages(exclude=['tests', 'examples', 'docs']),
    include_package_data=True,
    url='https://github.com/shibing624/weibopy',
    project_urls={
        'Documentation': 'https://github.com/shibing624/weibopy#readme',
        'Source': 'https://github.com/shibing624/weibopy',
        'Issues': 'https://github.com/shibing624/weibopy/issues',
    },
    license='MIT',
    author='xuming',
    author_email='xuming624@qq.com',
    description='一个免登陆获取新浪微博数据的Python库，简单易用',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords=['weibo', 'api', 'scraper', 'social-media', '微博', 'sdk'],
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.10.0',
        'python-dotenv>=0.19.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
            'black>=23.0',
            'flake8>=6.0',
            'mypy>=1.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Communications',
    ],
    zip_safe=False,
)
