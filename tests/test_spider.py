"""
爬虫测试模块
测试数据清洗和爬虫基础功能
"""
import pytest
import os
import sys

# 添加项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.crawler.data_clean import clean_text, deduplicate_posts, filter_invalid_posts


def test_clean_text():
    """测试文本清洗功能"""
    raw_text = "  Hello!   This is a test...\n\n  "
    cleaned = clean_text(raw_text)
    
    assert cleaned == "Hello! This is a test..."


def test_deduplicate_posts():
    """测试帖子去重功能"""
    posts = [
        {"link": "url1", "content": "content1"},
        {"link": "url1", "content": "content1"},  # 重复
        {"link": "url2", "content": "content2"}
    ]
    
    unique = deduplicate_posts(posts)
    assert len(unique) == 2


def test_filter_invalid_posts():
    """测试无效帖子过滤"""
    posts = [
        {"link": "url1", "content": "content1"},  # 有效
        {"link": "", "content": ""},  # 无效
        {"link": "url2", "content": ""}  # 有效（有链接）
    ]
    
    valid = filter_invalid_posts(posts)
    assert len(valid) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
