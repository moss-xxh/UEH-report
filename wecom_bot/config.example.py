"""
企业微信机器人配置文件（示例）
使用说明：
1. 复制此文件为 config.py
2. 填写你的企业微信webhook地址和其他配置
"""

# 企业微信机器人Webhook地址
# 获取方式：企业微信群 -> 群设置 -> 群机器人 -> 添加机器人 -> 复制Webhook地址
WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY_HERE"

# 数据统计配置
STATS_CONFIG = {
    # 数据库配置（示例）
    "database": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "your_password",
        "database": "your_database"
    },

    # 统计时间配置
    "schedule": {
        "daily_report_time": "09:00",  # 每日报告推送时间
        "timezone": "Asia/Shanghai"
    },

    # 统计指标配置
    "metrics": {
        "api_requests": True,      # 是否统计API请求
        "user_activity": True,     # 是否统计用户活跃度
        "error_logs": True,        # 是否统计错误日志
        "performance": True        # 是否统计性能指标
    }
}

# 告警阈值配置
ALERT_THRESHOLDS = {
    "error_rate": 0.05,        # 错误率超过5%告警
    "response_time": 2000,     # 响应时间超过2秒告警
    "cpu_usage": 80,           # CPU使用率超过80%告警
    "memory_usage": 80         # 内存使用率超过80%告警
}
