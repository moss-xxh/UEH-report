# ⚡ 快速开始指南

## 第一步：获取企业微信Webhook地址

1. 打开企业微信，进入你想接收通知的群聊
2. 点击右上角 `···` -> `群机器人` -> `添加机器人`
3. 设置机器人名称（如：项目监控机器人）
4. 复制生成的 **Webhook地址**（类似：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx`）

## 第二步：安装依赖

```bash
cd /Users/xuexinhai/Desktop/1/wecom_bot
pip3 install -r requirements.txt
```

或使用安装脚本：

```bash
./setup.sh
```

## 第三步：配置Webhook

编辑 `config.py` 文件，将Webhook地址替换为你的：

```python
WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的key"
```

## 第四步：测试连接

```bash
python3 main.py --test
```

如果配置正确，群里会收到一条测试消息和一份统计报告。

## 第五步：配置数据统计（重要！）

根据你的项目类型，编辑 `data_collector.py`：

### 场景1：统计MySQL数据库数据

1. 安装MySQL驱动：
```bash
pip3 install pymysql
```

2. 配置数据库连接（`config.py`）：
```python
STATS_CONFIG = {
    "database": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "your_password",
        "database": "your_database"
    }
}
```

3. 修改 `data_collector.py` 中的 `collect_application_metrics()` 方法：
```python
def collect_application_metrics(self) -> Dict:
    import pymysql

    try:
        conn = pymysql.connect(**self.config['database'])
        cursor = conn.cursor()

        # 查询今日数据
        cursor.execute("SELECT COUNT(*) FROM orders WHERE DATE(created_at) = CURDATE()")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(amount) FROM orders WHERE DATE(created_at) = CURDATE()")
        total_revenue = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue
        }
    except Exception as e:
        logger.error(f"数据库查询失败: {e}")
        return {}
```

### 场景2：统计API数据

```python
def collect_application_metrics(self) -> Dict:
    import requests

    try:
        response = requests.get('http://your-api.com/stats', timeout=10)
        data = response.json()

        return {
            'total_requests': data.get('requests', 0),
            'active_users': data.get('users', 0)
        }
    except Exception as e:
        logger.error(f"API调用失败: {e}")
        return {}
```

### 场景3：统计日志文件

```python
def collect_application_metrics(self) -> Dict:
    from datetime import datetime

    today = datetime.now().strftime("%Y-%m-%d")

    try:
        with open('/var/log/app.log', 'r') as f:
            lines = f.readlines()

        # 统计今日访问
        today_requests = [l for l in lines if today in l and 'REQUEST' in l]

        # 统计今日错误
        today_errors = [l for l in lines if today in l and 'ERROR' in l]

        return {
            'total_requests': len(today_requests),
            'error_count': len(today_errors),
            'error_rate': (len(today_errors) / len(today_requests) * 100) if today_requests else 0
        }
    except Exception as e:
        logger.error(f"日志分析失败: {e}")
        return {}
```

## 第六步：自定义报告格式

编辑 `wecom_client.py` 中的 `format_daily_report()` 函数，根据你的数据调整报告内容：

```python
def format_daily_report(stats: Dict) -> str:
    report = f"""## 📊 我的项目日报

**日期：** {stats.get('date')}

### 业务数据
- **订单数：** {stats.get('total_orders', 0)} 单
- **营收：** ¥{stats.get('total_revenue', 0):.2f}

### 系统性能
- **CPU：** {stats.get('cpu_usage', 0):.1f}%
- **内存：** {stats.get('memory_usage', 0):.1f}%

> 生成时间：{stats.get('generated_at')}
"""
    return report
```

## 第七步：设置定时推送

编辑 `config.py` 设置推送时间：

```python
STATS_CONFIG = {
    "schedule": {
        "daily_report_time": "09:00",  # 每天早上9点
        "timezone": "Asia/Shanghai"
    }
}
```

## 第八步：正式运行

### 前台运行（测试用）
```bash
python3 main.py
```

### 后台运行（生产环境）
```bash
nohup python3 main.py > bot.log 2>&1 &
```

### 查看日志
```bash
tail -f wecom_bot.log
```

### 停止程序
```bash
# 查找进程
ps aux | grep main.py

# 杀死进程
kill <进程ID>
```

## 常见问题

### Q1: 消息发送失败
- 检查Webhook地址是否正确
- 确认网络连接
- 查看日志：`cat wecom_bot.log`

### Q2: 定时任务不执行
- 确认程序在后台运行：`ps aux | grep main.py`
- 检查系统时间是否正确
- 查看日志

### Q3: 数据统计不准确
- 检查数据库连接配置
- 查看 `data_collector.py` 中的SQL语句
- 检查日志中的错误信息

## 进阶配置

### 添加多个推送时间

编辑 `main.py` 的 `setup_schedules()` 方法：

```python
def setup_schedules(self):
    # 早上9点
    self.scheduler.add_daily_job("09:00", self.send_daily_report)

    # 晚上6点
    self.scheduler.add_daily_job("18:00", self.send_daily_report)

    # 每小时健康检查
    self.scheduler.add_interval_job(1, "hours", self.health_check)
```

### 开机自启动（Linux/Mac）

创建启动脚本 `start.sh`：

```bash
#!/bin/bash
cd /Users/xuexinhai/Desktop/1/wecom_bot
nohup python3 main.py > bot.log 2>&1 &
echo "机器人已启动"
```

添加到系统启动项。

## 下一步

- 📖 阅读完整文档：`README.md`
- 🔧 自定义统计指标：修改 `data_collector.py`
- ⚙️ 调整告警阈值：编辑 `config.py` 中的 `ALERT_THRESHOLDS`
- 🎨 美化报告格式：修改 `wecom_client.py`

祝使用愉快！🎉
