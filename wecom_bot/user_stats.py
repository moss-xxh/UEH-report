#!/usr/bin/env python3
"""
用户数据统计模块
"""
from datetime import datetime, timedelta
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserStatsCollector:
    """用户数据统计采集器"""

    def __init__(self, db_config: Dict = None):
        """
        初始化用户统计采集器

        Args:
            db_config: 数据库配置
        """
        self.db_config = db_config

    def get_today_stats(self) -> Dict:
        """
        获取今日VPP运行统计数据

        Returns:
            Dict: 今日统计数据
        """
        # TODO: 从数据库获取真实数据
        # 示例SQL查询逻辑：

        # import pymysql
        # conn = pymysql.connect(**self.db_config)
        # cursor = conn.cursor()
        #
        # # 今日调度次数
        # cursor.execute("""
        #     SELECT COUNT(*) FROM dispatch_records
        #     WHERE DATE(created_at) = CURDATE()
        # """)
        # dispatch_count = cursor.fetchone()[0]
        #
        # # 今日充电次数
        # cursor.execute("""
        #     SELECT COUNT(*) FROM dispatch_records
        #     WHERE DATE(created_at) = CURDATE() AND type = 'charge'
        # """)
        # charge_count = cursor.fetchone()[0]
        #
        # # 今日放电次数
        # cursor.execute("""
        #     SELECT COUNT(*) FROM dispatch_records
        #     WHERE DATE(created_at) = CURDATE() AND type = 'discharge'
        # """)
        # discharge_count = cursor.fetchone()[0]
        #
        # # 今日累计馈网量(kWh)
        # cursor.execute("""
        #     SELECT SUM(power_kwh) FROM grid_feedback
        #     WHERE DATE(created_at) = CURDATE()
        # """)
        # grid_power = cursor.fetchone()[0] or 0
        #
        # # 今日获利金额
        # cursor.execute("""
        #     SELECT SUM(profit) FROM profit_records
        #     WHERE DATE(created_at) = CURDATE()
        # """)
        # profit = cursor.fetchone()[0] or 0
        #
        # conn.close()

        # 模拟数据（请替换为真实数据库查询）
        today_stats = {
            'new_users': 4,
            'exit_users': 0,
            'total_users': 19,
            'dispatch_count': 3,      # 今日调度次数
            'charge_count': 185,         # 今日充电次数
            'discharge_count': 143,      # 今日放电次数
            'grid_power': 318,           # 今日累计馈网量(kWh)
            'profit': 26,                # 今日获利(元)
            'success_rate': 99.8,        # 调度成功率(%)

            # 设备地区分布（澳洲）
            'device_by_region': {
                'NSW': 13,    # 新南威尔士州
                'QLD': 0,     # 昆士兰州
                'VIC': 6,     # 维多利亚州
                'SA': 0,      # 南澳大利亚州
                'TAS': 0      # 塔斯马尼亚州
            },

            # 设备品牌分布
            'device_by_brand': {
                'ipotisedge': 4,
                'FOX ESS': 6,
                'Alpha': 9
            }
        }

        logger.info(f"✓ 今日数据采集成功: 调度{today_stats['dispatch_count']}次, 充电{today_stats['charge_count']}次, 放电{today_stats['discharge_count']}次")
        return today_stats

    def get_yesterday_stats(self) -> Dict:
        """
        获取昨日VPP运行统计数据

        Returns:
            Dict: 昨日统计数据
        """
        # TODO: 从数据库获取昨日数据

        # 模拟数据
        yesterday_stats = {
            'new_users': 134,
            'exit_users': 38,
            'total_users': 18,
            'dispatch_count': 2,
            'charge_count': 165,
            'discharge_count': 133,
            'grid_power': 294.5,
            'profit': 24.5,
            'success_rate': 99.6
        }

        logger.info(f"✓ 昨日数据采集成功: 调度{yesterday_stats['dispatch_count']}次, 充电{yesterday_stats['charge_count']}次, 放电{yesterday_stats['discharge_count']}次")
        return yesterday_stats

    def get_regional_dispatch_details(self) -> list:
        """
        获取地区调度详情

        Returns:
            list: 地区调度详情列表
        """
        # TODO: 从数据库获取真实数据
        # 示例SQL:
        # SELECT
        #     DATE_FORMAT(dispatch_time, '%H:%M') as time,
        #     region,
        #     type as action,
        #     COUNT(*) as device_count
        # FROM dispatch_records
        # WHERE DATE(dispatch_time) = CURDATE()
        # GROUP BY time, region, type
        # ORDER BY dispatch_time DESC
        # LIMIT 10

        # 模拟数据
        details = [
            {'time': '14:30', 'region': '深圳南山', 'action': '放电', 'device_count': 45},
            {'time': '13:15', 'region': '广州天河', 'action': '充电', 'device_count': 38},
            {'time': '12:00', 'region': '深圳福田', 'action': '放电', 'device_count': 52},
            {'time': '10:45', 'region': '东莞松山湖', 'action': '充电', 'device_count': 31},
            {'time': '09:20', 'region': '佛山顺德', 'action': '放电', 'device_count': 28},
        ]

        logger.info(f"✓ 地区调度详情采集成功: {len(details)}条记录")
        return details

    def get_regional_operation_stats(self) -> list:
        """
        获取各地区运行统计数据

        Returns:
            list: 地区运行数据列表
        """
        # TODO: 从数据库获取真实数据
        # 模拟数据
        regional_stats = [
            {
                'region': 'NSW',
                'dispatch_count': 125,      # 调度次数
                'device_count': 1245,       # 调度设备数
                'grid_power': 1125.5,       # 馈网量(kWh)
                'profit': 1687.25           # 获利(元)
            },
            {
                'region': 'QLD',
                'dispatch_count': 98,
                'device_count': 987,
                'grid_power': 892.3,
                'profit': 1338.45
            },
            {
                'region': 'VIC',
                'dispatch_count': 67,
                'device_count': 856,
                'grid_power': 652.8,
                'profit': 979.20
            },
            {
                'region': 'SA',
                'dispatch_count': 28,
                'device_count': 432,
                'grid_power': 135.6,
                'profit': 203.40
            },
            {
                'region': 'TAS',
                'dispatch_count': 10,
                'device_count': 178,
                'grid_power': 50.3,
                'profit': 77.45
            },
            {
                'region': 'NSW',
                'dispatch_count': 115,
                'device_count': 1198,
                'grid_power': 1087.2,
                'profit': 1630.80
            },
            {
                'region': 'QLD',
                'dispatch_count': 89,
                'device_count': 945,
                'grid_power': 856.4,
                'profit': 1284.60
            },
            {
                'region': 'VIC',
                'dispatch_count': 72,
                'device_count': 823,
                'grid_power': 745.6,
                'profit': 1118.40
            },
            {
                'region': 'SA',
                'dispatch_count': 31,
                'device_count': 412,
                'grid_power': 167.8,
                'profit': 251.70
            },
            {
                'region': 'TAS',
                'dispatch_count': 14,
                'device_count': 165,
                'grid_power': 63.2,
                'profit': 94.80
            },
            {
                'region': 'NSW',
                'dispatch_count': 108,
                'device_count': 1156,
                'grid_power': 1042.3,
                'profit': 1563.45
            },
            {
                'region': 'QLD',
                'dispatch_count': 92,
                'device_count': 912,
                'grid_power': 823.7,
                'profit': 1235.55
            },
            {
                'region': 'VIC',
                'dispatch_count': 58,
                'device_count': 795,
                'grid_power': 698.4,
                'profit': 1047.60
            },
            {
                'region': 'SA',
                'dispatch_count': 25,
                'device_count': 398,
                'grid_power': 152.3,
                'profit': 228.45
            },
            {
                'region': 'TAS',
                'dispatch_count': 12,
                'device_count': 152,
                'grid_power': 57.8,
                'profit': 86.70
            },
            {
                'region': 'NSW',
                'dispatch_count': 132,
                'device_count': 1287,
                'grid_power': 1198.6,
                'profit': 1797.90
            },
            {
                'region': 'QLD',
                'dispatch_count': 103,
                'device_count': 1024,
                'grid_power': 945.8,
                'profit': 1418.70
            },
            {
                'region': 'VIC',
                'dispatch_count': 81,
                'device_count': 892,
                'grid_power': 812.4,
                'profit': 1218.60
            },
            {
                'region': 'SA',
                'dispatch_count': 35,
                'device_count': 456,
                'grid_power': 189.5,
                'profit': 284.25
            },
            {
                'region': 'TAS',
                'dispatch_count': 16,
                'device_count': 187,
                'grid_power': 72.3,
                'profit': 108.45
            }
        ]

        logger.info(f"✓ 地区运行数据采集成功: {len(regional_stats)}个地区")
        return regional_stats

    def get_dispatch_records(self) -> list:
        """
        获取调度记录

        Returns:
            list: 调度记录列表
        """
        # TODO: 从数据库获取真实数据
        # 模拟数据
        records = [
            {
                'time': '14:30',
                'region': 'NSW',
                'command': '放电',
                'device_count': 328,
                'start_devices': 312,       # 下发设备数
                'start_success_rate': 95.1, # 下发成功率
                'stop_devices': 298,        # 停止设备数
                'stop_success_rate': 90.9   # 停止成功率
            },
            {
                'time': '13:15',
                'region': 'QLD',
                'command': '充电',
                'device_count': 298,
                'start_devices': 285,
                'start_success_rate': 95.6,
                'stop_devices': 272,
                'stop_success_rate': 91.3
            },
            {
                'time': '12:00',
                'region': 'VIC',
                'command': '放电',
                'device_count': 315,
                'start_devices': 302,
                'start_success_rate': 95.9,
                'stop_devices': 289,
                'stop_success_rate': 91.7
            },
            {
                'time': '10:45',
                'region': 'NSW',
                'command': '充电',
                'device_count': 287,
                'start_devices': 275,
                'start_success_rate': 95.8,
                'stop_devices': 264,
                'stop_success_rate': 92.0
            },
            {
                'time': '09:20',
                'region': 'SA',
                'command': '放电',
                'device_count': 302,
                'start_devices': 289,
                'start_success_rate': 95.7,
                'stop_devices': 276,
                'stop_success_rate': 91.4
            }
        ]

        logger.info(f"✓ 调度记录采集成功: {len(records)}条记录")
        return records

    def calculate_compare(self, today: int, yesterday: int) -> Dict:
        """
        计算对比数据

        Args:
            today: 今日数值
            yesterday: 昨日数值

        Returns:
            Dict: 对比结果
        """
        if yesterday == 0:
            return {
                'change': today,
                'percent': 0,
                'trend': '─'
            }

        change = today - yesterday
        percent = round((change / yesterday) * 100, 1)

        return {
            'change': change,
            'percent': abs(percent),
            'trend': '↑' if change > 0 else '↓' if change < 0 else '─',
            'is_increase': change > 0
        }

    def format_user_report(self) -> str:
        """
        生成用户数据Markdown报告

        Returns:
            str: Markdown格式的报告
        """
        today = self.get_today_stats()
        yesterday = self.get_yesterday_stats()

        # 计算对比
        new_compare = self.calculate_compare(today['new_users'], yesterday['new_users'])
        exit_compare = self.calculate_compare(today['exit_users'], yesterday['exit_users'])
        total_compare = self.calculate_compare(today['total_users'], yesterday['total_users'])

        # 当前日期
        current_date = datetime.now().strftime('%Y年%m月%d日')
        current_time = datetime.now().strftime('%H:%M')

        # 生成报告
        report = f"""## 📊 VPP运行报告

**统计日期：** {current_date}

---

### 👥 今日新增用户

<font color="info">**{today['new_users']:,}** 人</font>

对比昨日：<font color="{'comment' if new_compare['is_increase'] else 'warning'}">{new_compare['trend']} {new_compare['change']:+,} 人 ({new_compare['trend']} {new_compare['percent']}%)</font>

---

### 👋 今日退出用户

<font color="warning">**{today['exit_users']:,}** 人</font>

对比昨日：<font color="{'warning' if exit_compare['is_increase'] else 'info'}">{exit_compare['trend']} {exit_compare['change']:+,} 人 ({exit_compare['trend']} {exit_compare['percent']}%)</font>

---

### 📈 目前总用户

<font color="info">**{today['total_users']:,}** 人</font>

对比昨日：<font color="{'info' if total_compare['is_increase'] else 'warning'}">{total_compare['trend']} {total_compare['change']:+,} 人 ({total_compare['trend']} {total_compare['percent']}%)</font>

---

### 📊 数据概览

| 指标 | 今日 | 昨日 | 变化 |
|------|------|------|------|
| 新增用户 | {today['new_users']:,} | {yesterday['new_users']:,} | {new_compare['trend']} {new_compare['change']:+,} |
| 退出用户 | {today['exit_users']:,} | {yesterday['exit_users']:,} | {exit_compare['trend']} {exit_compare['change']:+,} |
| 总用户数 | {today['total_users']:,} | {yesterday['total_users']:,} | {total_compare['trend']} {total_compare['change']:+,} |
| 净增长 | {today['new_users'] - today['exit_users']:+,} | {yesterday['new_users'] - yesterday['exit_users']:+,} | - |

---

> 📅 报告生成时间：{current_date} {current_time}
"""

        return report

    def get_exceptions(self) -> list:
        """
        获取异常情况

        Returns:
            list: 异常情况列表
        """
        # TODO: 从数据库获取真实数据
        # 模拟数据（按时间、地区、指令分组排序以便合并单元格）
        exceptions = [
            # 19:11:28 - NSW1 - 停止调度 (3条)
            {'time': '2025-11-07 19:11:28', 'region': 'NSW1', 'command': '停止调度', 'sn': '2448-36640026PH', 'brand': 'FOX ESS', 'nmi': '6305522614', 'retry_count': 3, 'error_reason': '等待回调通知超时'},
            {'time': '2025-11-07 19:11:28', 'region': 'NSW1', 'command': '停止调度', 'sn': '4921-58372946PH', 'brand': 'Alpha', 'nmi': '6305522615', 'retry_count': 3, 'error_reason': '网络连接超时'},
            {'time': '2025-11-07 19:11:28', 'region': 'NSW1', 'command': '停止调度', 'sn': '3728-91847263PH', 'brand': 'ipotisedge', 'nmi': '6305522616', 'retry_count': 3, 'error_reason': '等待回调通知超时'},

            # 18:45:12 - VIC - 充电 (2条)
            {'time': '2025-11-07 18:45:12', 'region': 'VIC', 'command': '充电', 'sn': '3512-44729018PH', 'brand': 'FOX ESS', 'nmi': '6305522617', 'retry_count': 3, 'error_reason': '网络连接超时'},
            {'time': '2025-11-07 18:45:12', 'region': 'VIC', 'command': '充电', 'sn': '2837-61829475PH', 'brand': 'ipotisedge', 'nmi': '6305522618', 'retry_count': 3, 'error_reason': '等待回调通知超时'},

            # 17:32:45 - QLD - 放电 (2条)
            {'time': '2025-11-07 17:32:45', 'region': 'QLD', 'command': '放电', 'sn': '1856-29384765PH', 'brand': 'Alpha', 'nmi': '6305522619', 'retry_count': 3, 'error_reason': '网络连接超时'},
            {'time': '2025-11-07 17:32:45', 'region': 'QLD', 'command': '放电', 'sn': '5194-73628491PH', 'brand': 'FOX ESS', 'nmi': '6305522620', 'retry_count': 3, 'error_reason': '等待回调通知超时'},

            # 14:38:29 - NSW1 - 充电 (1条)
            {'time': '2025-11-07 14:38:29', 'region': 'NSW1', 'command': '充电', 'sn': '6482-38291756PH', 'brand': 'ipotisedge', 'nmi': '6305522621', 'retry_count': 3, 'error_reason': '网络连接超时'}
        ]

        logger.info(f"✓ 异常情况采集成功: {len(exceptions)}条记录")
        return exceptions

    def get_stats_for_card(self) -> Dict:
        """
        获取用于模版卡片的统计数据

        Returns:
            Dict: 卡片数据结构
        """
        today = self.get_today_stats()
        yesterday = self.get_yesterday_stats()
        regional_details = self.get_regional_dispatch_details()
        regional_operation = self.get_regional_operation_stats()
        dispatch_records = self.get_dispatch_records()
        exceptions = self.get_exceptions()
        current_date = datetime.now().strftime('%Y年%m月%d日')

        return {
            'date': current_date,
            'today': today,
            'yesterday': yesterday,
            'regional_details': regional_details,
            'regional_operation': regional_operation,
            'dispatch_records': dispatch_records,
            'exceptions': exceptions
        }

    def format_simple_report(self) -> str:
        """
        生成简洁版用户数据报告

        Returns:
            str: 简洁版Markdown报告
        """
        today = self.get_today_stats()
        yesterday = self.get_yesterday_stats()

        new_compare = self.calculate_compare(today['new_users'], yesterday['new_users'])
        exit_compare = self.calculate_compare(today['exit_users'], yesterday['exit_users'])
        total_compare = self.calculate_compare(today['total_users'], yesterday['total_users'])

        current_date = datetime.now().strftime('%m月%d日')

        report = f"""**📊 VPP运行报告 - {current_date}**

👥 新增：**{today['new_users']}** 人 ({new_compare['trend']}{new_compare['percent']}%)
👋 退出：**{today['exit_users']}** 人 ({exit_compare['trend']}{exit_compare['percent']}%)
📈 总计：**{today['total_users']:,}** 人 ({total_compare['trend']}{abs(total_compare['change'])}人)

净增长：**{today['new_users'] - today['exit_users']:+}** 人
"""

        return report


# 使用示例
if __name__ == "__main__":
    # 创建采集器
    collector = UserStatsCollector()

    # 生成完整报告
    print("=" * 60)
    print("完整版报告：")
    print("=" * 60)
    report = collector.format_user_report()
    print(report)

    print("\n" + "=" * 60)
    print("简洁版报告：")
    print("=" * 60)
    simple_report = collector.format_simple_report()
    print(simple_report)
