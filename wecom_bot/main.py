#!/usr/bin/env python3
"""
企业微信项目运行数据统计机器人
主程序入口
"""
import logging
from datetime import datetime

from config import WECOM_WEBHOOK, STATS_CONFIG
from wecom_client import WeComBot, format_daily_report, format_alert_message
from data_collector import DataCollector
from scheduler import TaskScheduler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wecom_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProjectMonitorBot:
    """项目监控机器人"""

    def __init__(self):
        self.bot = WeComBot(WECOM_WEBHOOK)
        self.collector = DataCollector(STATS_CONFIG)
        self.scheduler = TaskScheduler()

    def send_daily_report(self):
        """发送每日报告"""
        try:
            logger.info("=" * 60)
            logger.info("📊 开始生成每日报告")

            # 采集数据
            stats = self.collector.collect_daily_stats()

            # 格式化报告
            report = format_daily_report(stats)

            # 发送报告
            success = self.bot.send_markdown(report)

            if success:
                logger.info("✓ 每日报告发送成功")
            else:
                logger.error("✗ 每日报告发送失败")

            # 检查是否有告警
            alerts = self.collector.check_alerts(stats)
            if alerts:
                self.send_alerts(alerts)

            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"✗ 发送每日报告时发生错误: {e}")
            import traceback
            traceback.print_exc()

    def send_alerts(self, alerts: list):
        """发送告警消息"""
        try:
            for alert in alerts:
                message = format_alert_message(alert['type'], alert)
                self.bot.send_markdown(message)
                logger.warning(f"⚠️  告警已发送: {alert['type']}")

        except Exception as e:
            logger.error(f"✗ 发送告警时发生错误: {e}")

    def health_check(self):
        """健康检查（可选）"""
        try:
            logger.info("🔍 执行健康检查")

            # 采集当前数据
            stats = self.collector.collect_daily_stats()

            # 检查告警
            alerts = self.collector.check_alerts(stats)

            # 只有检测到告警时才发送
            if alerts:
                self.send_alerts(alerts)

        except Exception as e:
            logger.error(f"✗ 健康检查时发生错误: {e}")

    def setup_schedules(self):
        """设置定时任务"""
        # 每日报告时间
        daily_time = STATS_CONFIG['schedule']['daily_report_time']

        # 添加每日报告任务
        self.scheduler.add_daily_job(daily_time, self.send_daily_report)

        # 可选：添加健康检查任务（每小时一次）
        # self.scheduler.add_interval_job(1, "hours", self.health_check)

        logger.info(f"✓ 定时任务已配置")
        logger.info(f"  - 每日报告时间: {daily_time}")
        logger.info(f"  - 下次执行时间: {self.scheduler.get_next_run()}")

    def test_connection(self):
        """测试企业微信连接"""
        logger.info("🔧 测试企业微信连接...")

        test_message = f"""## 🤖 机器人测试消息

**测试时间：** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

机器人已成功连接！定时任务将按计划执行。

---

> 这是一条测试消息，如果您看到此消息，说明机器人配置正确。
"""

        success = self.bot.send_markdown(test_message)

        if success:
            logger.info("✓ 企业微信连接测试成功")
            return True
        else:
            logger.error("✗ 企业微信连接测试失败，请检查Webhook配置")
            return False

    def start(self, test_mode: bool = False):
        """
        启动机器人

        Args:
            test_mode: 是否为测试模式（测试模式下立即发送一次报告）
        """
        logger.info("\n" + "=" * 60)
        logger.info("🚀 企业微信项目监控机器人启动")
        logger.info("=" * 60 + "\n")

        # 测试连接
        if not self.test_connection():
            logger.error("⚠️  连接测试失败，请检查配置后重试")
            return

        if test_mode:
            logger.info("📝 测试模式：立即发送一次报告")
            self.send_daily_report()
        else:
            # 设置定时任务
            self.setup_schedules()

            # 启动调度器（阻塞模式）
            self.scheduler.start(blocking=True)


def main():
    """主函数"""
    import sys

    bot = ProjectMonitorBot()

    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 测试模式
        bot.start(test_mode=True)
    else:
        # 正常模式
        bot.start(test_mode=False)


if __name__ == "__main__":
    main()
