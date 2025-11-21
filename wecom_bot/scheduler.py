"""
定时任务调度模块
"""
import schedule
import time
import logging
from datetime import datetime
from typing import Callable

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskScheduler:
    """定时任务调度器"""

    def __init__(self):
        self.jobs = []

    def add_daily_job(self, time_str: str, func: Callable, *args, **kwargs):
        """
        添加每日定时任务

        Args:
            time_str: 时间字符串，格式 "HH:MM"
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
        """
        job = schedule.every().day.at(time_str).do(func, *args, **kwargs)
        self.jobs.append(job)
        logger.info(f"✓ 已添加每日任务: {func.__name__} at {time_str}")

    def add_interval_job(self, interval: int, unit: str, func: Callable, *args, **kwargs):
        """
        添加间隔执行任务

        Args:
            interval: 间隔时间
            unit: 时间单位 (seconds, minutes, hours)
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
        """
        if unit == "seconds":
            job = schedule.every(interval).seconds.do(func, *args, **kwargs)
        elif unit == "minutes":
            job = schedule.every(interval).minutes.do(func, *args, **kwargs)
        elif unit == "hours":
            job = schedule.every(interval).hours.do(func, *args, **kwargs)
        else:
            raise ValueError(f"不支持的时间单位: {unit}")

        self.jobs.append(job)
        logger.info(f"✓ 已添加间隔任务: {func.__name__} every {interval} {unit}")

    def run_pending(self):
        """执行所有待执行的任务"""
        schedule.run_pending()

    def start(self, blocking: bool = True):
        """
        启动调度器

        Args:
            blocking: 是否阻塞运行
        """
        logger.info("=" * 60)
        logger.info("🚀 定时任务调度器已启动")
        logger.info(f"📋 当前共有 {len(self.jobs)} 个任务")
        logger.info("=" * 60)

        if blocking:
            try:
                while True:
                    self.run_pending()
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\n⏹️  调度器已停止")
        else:
            # 非阻塞模式，需要在主程序中调用 run_pending()
            pass

    def clear_jobs(self):
        """清空所有任务"""
        schedule.clear()
        self.jobs = []
        logger.info("✓ 所有任务已清空")

    def get_next_run(self) -> str:
        """获取下次执行时间"""
        if self.jobs:
            next_job = min(self.jobs, key=lambda j: j.next_run)
            return next_job.next_run.strftime("%Y-%m-%d %H:%M:%S")
        return "无计划任务"


# 使用示例
if __name__ == "__main__":
    scheduler = TaskScheduler()

    # 测试任务
    def test_job(name):
        print(f"[{datetime.now()}] 执行任务: {name}")

    # 添加每日9点执行的任务
    scheduler.add_daily_job("09:00", test_job, "每日报告")

    # 添加每5分钟执行一次的任务
    scheduler.add_interval_job(5, "minutes", test_job, "健康检查")

    print(f"下次执行时间: {scheduler.get_next_run()}")

    # 启动调度器（阻塞模式）
    # scheduler.start()
