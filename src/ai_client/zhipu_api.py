"""
智谱AI客户端 - 使用requests直接调用API（最小依赖！
"""
import os
import logging
from typing import Optional
import requests

logger = logging.getLogger(__name__)

# 固定配置
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL_NAME = "glm-4-flash"

# 系统提示词
SYSTEM_PROMPT = """你是海外短视频&社媒行业分析师，对用户给到的海外INS/FB帖子原文：
1、完整翻译成通顺中文；
2、提炼爆款核心选题；
3、拆解内容脚本结构；
4、分析博主变现方式；
内容精简凝练，分段排版便于生成MD文档。"""


def load_api_key() -> str:
    """加载API密钥"""
    api_key = os.getenv("ZHIPU_API_KEY", "")
    if not api_key:
        raise ValueError("未找到 ZHIPU_API_KEY 环境变量")
    return api_key.strip()


def call_zhipu_api(text: str) -> Optional[str]:
    """调用智谱API"""
    try:
        api_key = load_api_key()
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        logger.info("📤 调用智谱API...")
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            logger.error(f"❌ API错误 {response.status_code}: {response.text}")
            return None
        
        data = response.json()
        
        result = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if not result:
            logger.error("❌ API返回内容为空")
            return None
        
        logger.info("✅ 智谱API调用成功")
        return result
        
    except requests.exceptions.Timeout:
        logger.error("❌ API调用超时")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 网络请求失败: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ 调用异常: {e}", exc_info=True)
        return None


def get_content_brief(raw_text: str) -> Optional[str]:
    """对外部暴露的主函数"""
    return call_zhipu_api(raw_text)
