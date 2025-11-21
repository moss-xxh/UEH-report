"""
企业微信机器人客户端
用于向企业微信群发送消息
"""
import requests
import json
from typing import Dict, List, Optional


class WeComBot:
    """企业微信机器人客户端"""

    def __init__(self, webhook_url: str):
        """
        初始化企业微信机器人

        Args:
            webhook_url: 企业微信机器人Webhook地址
        """
        self.webhook_url = webhook_url

    def send_text(self, content: str, mentioned_list: Optional[List[str]] = None) -> bool:
        """
        发送文本消息

        Args:
            content: 消息内容
            mentioned_list: @的用户列表，如 ["@all"] 或 ["userid1", "userid2"]

        Returns:
            bool: 发送是否成功
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }

        if mentioned_list:
            data["text"]["mentioned_list"] = mentioned_list

        return self._send(data)

    def send_markdown(self, content: str) -> bool:
        """
        发送Markdown消息

        Args:
            content: Markdown格式的消息内容

        Returns:
            bool: 发送是否成功
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }

        return self._send(data)

    def send_news(self, articles: List[Dict]) -> bool:
        """
        发送图文消息

        Args:
            articles: 图文列表，每个元素包含 title, description, url, picurl

        Returns:
            bool: 发送是否成功
        """
        data = {
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }

        return self._send(data)

    def send_template_card(self, card_data: Dict) -> bool:
        """
        发送模版卡片消息

        Args:
            card_data: 卡片数据

        Returns:
            bool: 发送是否成功
        """
        data = {
            "msgtype": "template_card",
            "template_card": card_data
        }

        return self._send(data)

    def _send(self, data: Dict) -> bool:
        """
        发送消息到企业微信

        Args:
            data: 消息数据

        Returns:
            bool: 发送是否成功
        """
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self.webhook_url,
                headers=headers,
                data=json.dumps(data),
                timeout=10
            )

            result = response.json()

            if result.get("errcode") == 0:
                print("✓ 消息发送成功")
                return True
            else:
                print(f"✗ 消息发送失败: {result.get('errmsg')}")
                return False

        except Exception as e:
            print(f"✗ 发送消息时发生错误: {e}")
            return False


def format_daily_report(stats: Dict) -> str:
    """
    格式化每日统计报告（Markdown格式）

    Args:
        stats: 统计数据字典

    Returns:
        str: 格式化后的Markdown消息
    """
    report = f"""## 📊 项目运行日报

**统计日期：** {stats.get('date', 'N/A')}

---

### 📈 核心指标

- **总请求量：** <font color="info">{stats.get('total_requests', 0):,}</font> 次
- **活跃用户：** <font color="info">{stats.get('active_users', 0):,}</font> 人
- **平均响应时间：** <font color="warning">{stats.get('avg_response_time', 0)}</font> ms
- **错误率：** <font color="warning">{stats.get('error_rate', 0):.2f}%</font>

---

### 🔥 性能指标

- **CPU使用率：** {stats.get('cpu_usage', 0):.1f}%
- **内存使用率：** {stats.get('memory_usage', 0):.1f}%
- **磁盘使用率：** {stats.get('disk_usage', 0):.1f}%

---

### 📉 对比数据

- **较昨日请求量：** {stats.get('request_change', 'N/A')}
- **较昨日用户数：** {stats.get('user_change', 'N/A')}

---

> 报告生成时间：{stats.get('generated_at', 'N/A')}
"""
    return report


def format_user_stats_card(stats: Dict) -> Dict:
    """
    格式化VPP运行数据为文本通知模版卡片

    Args:
        stats: 统计数据字典

    Returns:
        Dict: 模版卡片数据
    """
    # 计算对比数据
    def format_compare(current, previous):
        if previous == 0:
            return "─ 0%"
        change = current - previous
        percent = (change / previous) * 100
        arrow = "↑" if change > 0 else "↓" if change < 0 else "─"
        return f"{arrow} {abs(percent):.1f}%"

    today_data = stats.get('today', {})
    yesterday_data = stats.get('yesterday', {})

    # 构建表格数据
    regional_details = stats.get('regional_details', [])
    table_rows = []
    for detail in regional_details[:5]:  # 最多显示5条
        table_rows.append([
            detail.get('time', '-'),
            detail.get('region', '-'),
            detail.get('action', '-'),
            f"{detail.get('device_count', 0)} 台"
        ])

    card = {
        "card_type": "text_notice",
        "source": {
            "desc": "VPP Data Statistics System"
        },
        "main_title": {
            "title": "📊 VPP Operations Report",
            "desc": stats.get('date', 'N/A')
        },
        "emphasis_content": {
            "title": f"${int(today_data.get('profit', 0))}",
            "desc": f"Today's Profit ({'+' if today_data.get('profit', 0) - yesterday_data.get('profit', 0) >= 0 else ''}${today_data.get('profit', 0) - yesterday_data.get('profit', 0):,.1f})"
        },
        "horizontal_content_list": [
            {
                "keyname": "👥 Users",
                "value": f"{today_data.get('total_users', 0)} (+{today_data.get('new_users', 0)})"
            },
            {
                "keyname": "🔄 Dispatches",
                "value": f"{today_data.get('dispatch_count', 0)} ({'+' if today_data.get('dispatch_count', 0) - yesterday_data.get('dispatch_count', 0) >= 0 else ''}{today_data.get('dispatch_count', 0) - yesterday_data.get('dispatch_count', 0)})"
            },
            {
                "keyname": "✓ Success Rate",
                "value": f"{today_data.get('success_rate', 0)}% ({'+' if today_data.get('success_rate', 0) - yesterday_data.get('success_rate', 0) >= 0 else ''}{today_data.get('success_rate', 0) - yesterday_data.get('success_rate', 0):.1f}%)"
            },
            {
                "keyname": "⚡ Grid Power",
                "value": f"{today_data.get('grid_power', 0):,.1f} kWh ({'+' if today_data.get('grid_power', 0) - yesterday_data.get('grid_power', 0) >= 0 else ''}{today_data.get('grid_power', 0) - yesterday_data.get('grid_power', 0):,.1f})"
            }
        ],
        "jump_list": [
            {
                "type": 1,
                "title": "View Details",
                "url": "https://moss-xxh.github.io/UEH-report/"
            }
        ],
        "card_action": {
            "type": 1,
            "url": "https://moss-xxh.github.io/UEH-report/"
        }
    }

    # Add table if regional details available
    if table_rows:
        card["table"] = {
            "table_title": "📋 Regional Dispatch Details",
            "table_header": ["Time", "Region", "Charge/Discharge", "Devices"],
            "table_content": table_rows
        }

    return card


def format_alert_message(alert_type: str, alert_data: Dict) -> str:
    """
    格式化告警消息

    Args:
        alert_type: 告警类型
        alert_data: 告警数据

    Returns:
        str: 格式化后的告警消息
    """
    alert_emoji = {
        "error": "🚨",
        "warning": "⚠️",
        "info": "ℹ️"
    }

    emoji = alert_emoji.get(alert_data.get('level', 'info'), "📢")

    message = f"""{emoji} **系统告警 - {alert_type}**

**告警级别：** {alert_data.get('level', 'unknown').upper()}
**告警时间：** {alert_data.get('timestamp', 'N/A')}
**告警内容：** {alert_data.get('message', 'N/A')}

---

**详细信息：**
{alert_data.get('details', '暂无详细信息')}
"""

    return message


# 使用示例
if __name__ == "__main__":
    # 测试代码
    from config import WECOM_WEBHOOK

    bot = WeComBot(WECOM_WEBHOOK)

    # 测试发送文本消息
    # bot.send_text("这是一条测试消息", mentioned_list=["@all"])

    # 测试发送Markdown消息
    test_stats = {
        "date": "2025-01-18",
        "total_requests": 125680,
        "active_users": 3256,
        "avg_response_time": 156,
        "error_rate": 0.23,
        "cpu_usage": 45.6,
        "memory_usage": 62.3,
        "disk_usage": 38.9,
        "request_change": "↑ 15.3%",
        "user_change": "↑ 8.7%",
        "generated_at": "2025-01-18 09:00:00"
    }

    # report = format_daily_report(test_stats)
    # bot.send_markdown(report)

    print("企业微信机器人客户端已就绪")
    print("请在config.py中配置正确的Webhook地址后使用")
