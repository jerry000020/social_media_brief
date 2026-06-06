"""
全局配置文件
定义爬虫延时、AI参数、存储路径、目标链接等
"""
import os

# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志配置
LOG_LEVEL = "INFO"
LOG_DIR = os.path.join(BASE_DIR, "logs")

# 数据存储路径
DATA_DIR = os.path.join(BASE_DIR, "data")

# 爬虫配置
CRAWLER_DELAY_MIN = 2  # 最小请求延时（秒）
CRAWLER_DELAY_MAX = 6  # 最大请求延时（秒）

# AI参数
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 2000

# 目标抓取链接列表（示例）
TARGET_URLS = {
    "instagram": [
        "https://www.instagram.com/p/example1/",
        "https://www.instagram.com/p/example2/"
    ],
    "facebook": [
        "https://www.facebook.com/example1/posts/123456",
        "https://www.facebook.com/example2/posts/789012"
    ]
}
