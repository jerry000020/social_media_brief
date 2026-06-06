"""
智谱GLM-4-Flash API统一封装模块
自动读取环境变量，提供get_content_brief()核心函数
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# 配置日志
logger = logging.getLogger(__name__)

# 系统提示词（固定）
SYSTEM_PROMPT = """你是海外短视频&社媒行业分析师，对用户给到的海外INS/FB帖子原文：
1、完整翻译成通顺中文；
2、提炼爆款核心选题；
3、拆解内容脚本结构；
4、分析博主变现方式；
内容精简凝练，分段排版便于生成MD文档。"""

# 接口固定参数
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"
MODEL_NAME = "glm-4-flash"


def load_api_key() -> str:
    """
    加载智谱API密钥
    优先级：系统环境变量（GitHub Actions）> .env文件 > 异常
    """
    # 先尝试从环境变量加载
    api_key = os.getenv("ZHIPU_API_KEY")
    
    if not api_key:
        # 尝试从.env文件加载
        load_dotenv()
        api_key = os.getenv("ZHIPU_API_KEY")
    
    if not api_key:
        raise ValueError("未找到ZHIPU_API_KEY，请在系统环境变量或.env文件中配置")
    
    return api_key


def get_content_brief(raw_text: str) -> Optional[str]:
    """
    调用智谱GLM-4-Flash生成结构化简报
    Args:
        raw_text: 原始英文社媒文案
    Returns:
        AI生成的结构化简报字符串，失败返回None
    """
    try:
        api_key = load_api_key()
        client = ZhipuAI(api_key=api_key)
        
        logger.info(f"正在调用智谱API处理文本，长度: {len(raw_text)}")
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": raw_text}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        logger.info("智谱API调用成功")
        return result
        
    except Exception as e:
        logger.error(f"智谱API调用失败: {str(e)}", exc_info=True)
        return None


def test_api_connection() -> bool:
    """
    测试智谱API连通性
    Returns:
        连接成功返回True，失败返回False
    """
    try:
        api_key = load_api_key()
        client = ZhipuAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "你好"}]
        )
        
        if response.choices[0].message.content:
            logger.info("智谱API连通性测试成功")
            return True
        return False
        
    except Exception as e:
        logger.error(f"智谱API连通性测试失败: {str(e)}", exc_info=True)
        return False
