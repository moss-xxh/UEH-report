#!/usr/bin/env python3
"""
用户数据统计机器人 - 主程序
每日定时向企业微信群推送用户数据
"""
import logging
from datetime import datetime

from config import WECOM_WEBHOOK, STATS_CONFIG
from wecom_client import WeComBot, format_user_stats_card
from user_stats import UserStatsCollector
from scheduler import TaskScheduler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('user_stats_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class UserStatsBot:
    """用户数据统计机器人"""

    def __init__(self, webhook_url: str, report_type: str = 'card'):
        """
        初始化机器人

        Args:
            webhook_url: 企业微信Webhook地址
            report_type: 报告类型 'card'(模版卡片) / 'detailed'(详细版) / 'simple'(简洁版)
        """
        self.bot = WeComBot(webhook_url)
        self.collector = UserStatsCollector()
        self.scheduler = TaskScheduler()
        self.report_type = report_type

    def send_daily_report(self):
        """发送每日用户数据报告"""
        try:
            logger.info("=" * 60)
            logger.info("📊 开始生成用户数据报告")

            # 根据类型发送不同格式
            if self.report_type == 'card':
                # 模版卡片格式
                stats_data = self.collector.get_stats_for_card()
                card_data = format_user_stats_card(stats_data)
                success = self.bot.send_template_card(card_data)
            elif self.report_type == 'simple':
                # 简洁版Markdown
                report = self.collector.format_simple_report()
                success = self.bot.send_markdown(report)
            else:
                # 详细版Markdown
                report = self.collector.format_user_report()
                success = self.bot.send_markdown(report)

            if success:
                logger.info("✓ 用户数据报告发送成功")
            else:
                logger.error("✗ 用户数据报告发送失败")

            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"✗ 发送报告时发生错误: {e}")
            import traceback
            traceback.print_exc()

    def setup_schedule(self, time_str: str):
        """
        设置定时任务

        Args:
            time_str: 推送时间，格式 "HH:MM"
        """
        self.scheduler.add_daily_job(time_str, self.send_daily_report)
        logger.info(f"✓ 已设置每日 {time_str} 推送用户数据")
        logger.info(f"  下次执行时间: {self.scheduler.get_next_run()}")

    def test_send(self):
        """测试发送"""
        logger.info("🔧 测试模式：立即发送一次用户数据报告")
        self.send_daily_report()

    def start(self, blocking: bool = True):
        """
        启动机器人

        Args:
            blocking: 是否阻塞运行
        """
        logger.info("\n" + "=" * 60)
        logger.info("🚀 用户数据统计机器人启动")
        logger.info("=" * 60 + "\n")

        if blocking:
            self.scheduler.start(blocking=True)


def main():
    """主函数"""
    import sys

    # 创建机器人（可选择不同报告格式）
    # report_type: 'card' = 模版卡片（推荐） 'detailed' = 详细版Markdown  'simple' = 简洁版Markdown
    bot = UserStatsBot(
        webhook_url=WECOM_WEBHOOK,
        report_type='card'  # 修改这里选择报告类型
    )

    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 测试模式：立即发送一次
        bot.test_send()
    else:
        # 正常模式：设置定时任务
        push_time = STATS_CONFIG['schedule']['daily_report_time']
        bot.setup_schedule(push_time)
        bot.start(blocking=True)


if __name__ == "__main__":
    main()
