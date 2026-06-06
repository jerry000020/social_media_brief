"""
智谱API测试模块
测试API连通性和简报生成功能
"""
import pytest
import os
import sys

# 添加项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.ai_client.zhipu_api import test_api_connection, get_content_brief


def test_api_connection():
    """测试API连通性"""
    result = test_api_connection()
    assert result is True, "API连接测试失败"


def test_brief_generation():
    """测试简报生成功能"""
    sample_text = "Check out this amazing AI tool! It can generate videos in seconds. #AI #Tech"
    brief = get_content_brief(sample_text)
    
    assert brief is not None, "简报生成失败"
    assert len(brief) > 0, "简报内容为空"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
