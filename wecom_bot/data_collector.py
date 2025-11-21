"""
数据采集和统计模块
"""
import psutil
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCollector:
    """数据采集器"""

    def __init__(self, config: Dict):
        """
        初始化数据采集器

        Args:
            config: 配置字典
        """
        self.config = config

    def collect_system_metrics(self) -> Dict:
        """
        采集系统性能指标

        Returns:
            Dict: 系统指标数据
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            metrics = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_total": memory.total / (1024 ** 3),  # GB
                "memory_used": memory.used / (1024 ** 3),    # GB
                "disk_usage": disk.percent,
                "disk_total": disk.total / (1024 ** 3),      # GB
                "disk_used": disk.used / (1024 ** 3)         # GB
            }

            logger.info("✓ 系统指标采集成功")
            return metrics

        except Exception as e:
            logger.error(f"✗ 系统指标采集失败: {e}")
            return {}

    def collect_application_metrics(self) -> Dict:
        """
        采集应用指标（需要根据实际项目实现）

        Returns:
            Dict: 应用指标数据
        """
        # TODO: 根据实际项目实现
        # 示例：从数据库、日志文件或API获取数据

        metrics = {
            "total_requests": 0,
            "active_users": 0,
            "avg_response_time": 0,
            "error_count": 0,
            "error_rate": 0.0
        }

        # 示例：如果使用MySQL数据库
        # try:
        #     import pymysql
        #     connection = pymysql.connect(**self.config['database'])
        #     with connection.cursor() as cursor:
        #         # 查询今日请求总量
        #         cursor.execute("SELECT COUNT(*) FROM requests WHERE DATE(created_at) = CURDATE()")
        #         metrics['total_requests'] = cursor.fetchone()[0]
        #
        #         # 查询今日活跃用户
        #         cursor.execute("SELECT COUNT(DISTINCT user_id) FROM requests WHERE DATE(created_at) = CURDATE()")
        #         metrics['active_users'] = cursor.fetchone()[0]
        #
        #     connection.close()
        # except Exception as e:
        #     logger.error(f"数据库查询失败: {e}")

        logger.info("✓ 应用指标采集成功")
        return metrics

    def collect_daily_stats(self) -> Dict:
        """
        采集每日统计数据

        Returns:
            Dict: 完整的统计数据
        """
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 采集系统指标
        system_metrics = self.collect_system_metrics()

        # 采集应用指标
        app_metrics = self.collect_application_metrics()

        # 计算同比数据（需要历史数据支持）
        changes = self.calculate_changes(app_metrics)

        # 合并所有数据
        stats = {
            "date": today,
            "generated_at": now,
            **system_metrics,
            **app_metrics,
            **changes
        }

        return stats

    def calculate_changes(self, current_metrics: Dict) -> Dict:
        """
        计算数据变化（同比、环比）

        Args:
            current_metrics: 当前指标

        Returns:
            Dict: 变化数据
        """
        # TODO: 实现实际的对比逻辑，需要存储历史数据
        # 示例返回
        changes = {
            "request_change": "N/A",
            "user_change": "N/A"
        }

        # 示例逻辑（需要从数据库或缓存中获取昨日数据）
        # yesterday_requests = get_yesterday_requests()
        # if yesterday_requests > 0:
        #     change_percent = ((current_metrics['total_requests'] - yesterday_requests) / yesterday_requests) * 100
        #     arrow = "↑" if change_percent > 0 else "↓"
        #     changes['request_change'] = f"{arrow} {abs(change_percent):.1f}%"

        return changes

    def check_alerts(self, stats: Dict) -> list:
        """
        检查是否需要告警

        Args:
            stats: 统计数据

        Returns:
            list: 告警列表
        """
        from config import ALERT_THRESHOLDS

        alerts = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 检查错误率
        if stats.get('error_rate', 0) > ALERT_THRESHOLDS['error_rate']:
            alerts.append({
                "type": "错误率告警",
                "level": "error",
                "timestamp": now,
                "message": f"错误率过高: {stats['error_rate']:.2f}%",
                "details": f"当前错误率 {stats['error_rate']:.2f}% 超过阈值 {ALERT_THRESHOLDS['error_rate'] * 100}%"
            })

        # 检查CPU使用率
        if stats.get('cpu_usage', 0) > ALERT_THRESHOLDS['cpu_usage']:
            alerts.append({
                "type": "CPU告警",
                "level": "warning",
                "timestamp": now,
                "message": f"CPU使用率过高: {stats['cpu_usage']:.1f}%",
                "details": f"当前CPU使用率 {stats['cpu_usage']:.1f}% 超过阈值 {ALERT_THRESHOLDS['cpu_usage']}%"
            })

        # 检查内存使用率
        if stats.get('memory_usage', 0) > ALERT_THRESHOLDS['memory_usage']:
            alerts.append({
                "type": "内存告警",
                "level": "warning",
                "timestamp": now,
                "message": f"内存使用率过高: {stats['memory_usage']:.1f}%",
                "details": f"当前内存使用率 {stats['memory_usage']:.1f}% 超过阈值 {ALERT_THRESHOLDS['memory_usage']}%"
            })

        if alerts:
            logger.warning(f"⚠️  检测到 {len(alerts)} 个告警")
        else:
            logger.info("✓ 所有指标正常")

        return alerts


# 使用示例
if __name__ == "__main__":
    from config import STATS_CONFIG

    collector = DataCollector(STATS_CONFIG)

    # 采集数据
    stats = collector.collect_daily_stats()
    print("\n=== 统计数据 ===")
    for key, value in stats.items():
        print(f"{key}: {value}")

    # 检查告警
    print("\n=== 告警检查 ===")
    alerts = collector.check_alerts(stats)
    if alerts:
        for alert in alerts:
            print(f"- {alert['message']}")
    else:
        print("无告警")
