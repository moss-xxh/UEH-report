# 企业微信项目运行数据统计机器人

## 📋 功能特性

- ✅ 每日定时推送项目运行数据统计报告
- ✅ 实时监控系统性能指标（CPU、内存、磁盘）
- ✅ 支持自定义数据统计指标
- ✅ 智能告警功能（错误率、响应时间、资源使用率）
- ✅ 优雅的Markdown格式报告
- ✅ 灵活的定时任务配置

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/xuexinhai/Desktop/1/wecom_bot
pip3 install -r requirements.txt
```

### 2. 获取企业微信机器人Webhook

1. 在企业微信群中，点击右上角 `···`
2. 选择 `群机器人` -> `添加机器人`
3. 设置机器人名称和头像
4. 复制生成的 **Webhook地址**

### 3. 配置机器人

编辑 `config.py` 文件：

```python
# 替换为你的Webhook地址
WECOM_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY_HERE"

# 配置每日报告时间
STATS_CONFIG = {
    "schedule": {
        "daily_report_time": "09:00",  # 每天早上9点推送
        "timezone": "Asia/Shanghai"
    }
}
```

### 4. 测试运行

```bash
# 测试模式：立即发送一次报告
python3 main.py --test
```

### 5. 正式运行

```bash
# 正常模式：按定时任务运行
python3 main.py
```

## 📊 数据统计配置

### 系统默认指标

机器人默认会采集以下系统指标：

- CPU使用率
- 内存使用率
- 磁盘使用率

### 自定义应用指标

编辑 `data_collector.py` 中的 `collect_application_metrics()` 方法：

#### 示例1：从MySQL数据库统计

```python
def collect_application_metrics(self) -> Dict:
    import pymysql

    metrics = {}

    try:
        connection = pymysql.connect(**self.config['database'])
        with connection.cursor() as cursor:
            # 查询今日请求总量
            cursor.execute("""
                SELECT COUNT(*) FROM requests
                WHERE DATE(created_at) = CURDATE()
            """)
            metrics['total_requests'] = cursor.fetchone()[0]

            # 查询今日活跃用户
            cursor.execute("""
                SELECT COUNT(DISTINCT user_id) FROM users
                WHERE DATE(last_active) = CURDATE()
            """)
            metrics['active_users'] = cursor.fetchone()[0]

        connection.close()

    except Exception as e:
        logger.error(f"数据库查询失败: {e}")

    return metrics
```

#### 示例2：从API接口获取

```python
def collect_application_metrics(self) -> Dict:
    import requests

    try:
        response = requests.get('http://your-api.com/stats')
        data = response.json()

        metrics = {
            'total_requests': data.get('requests', 0),
            'active_users': data.get('users', 0),
            'error_rate': data.get('error_rate', 0.0)
        }

    except Exception as e:
        logger.error(f"API调用失败: {e}")
        metrics = {}

    return metrics
```

#### 示例3：从日志文件分析

```python
def collect_application_metrics(self) -> Dict:
    import re
    from collections import Counter

    metrics = {}

    try:
        # 分析今日日志
        with open('/var/log/app.log', 'r') as f:
            lines = f.readlines()

        # 统计错误数
        errors = [line for line in lines if 'ERROR' in line]
        metrics['error_count'] = len(errors)

        # 统计请求数
        requests = [line for line in lines if 'REQUEST' in line]
        metrics['total_requests'] = len(requests)

    except Exception as e:
        logger.error(f"日志分析失败: {e}")

    return metrics
```

## ⚙️ 告警配置

编辑 `config.py` 中的 `ALERT_THRESHOLDS`：

```python
ALERT_THRESHOLDS = {
    "error_rate": 0.05,        # 错误率超过5%告警
    "response_time": 2000,     # 响应时间超过2秒告警
    "cpu_usage": 80,           # CPU使用率超过80%告警
    "memory_usage": 80         # 内存使用率超过80%告警
}
```

## 🔧 高级配置

### 添加多个定时任务

编辑 `main.py` 中的 `setup_schedules()` 方法：

```python
def setup_schedules(self):
    # 每日早上9点发送报告
    self.scheduler.add_daily_job("09:00", self.send_daily_report)

    # 每日晚上6点也发送一次
    self.scheduler.add_daily_job("18:00", self.send_daily_report)

    # 每小时执行健康检查
    self.scheduler.add_interval_job(1, "hours", self.health_check)

    # 每30分钟执行一次
    self.scheduler.add_interval_job(30, "minutes", self.health_check)
```

### 后台运行

#### 使用nohup（简单方式）

```bash
nohup python3 main.py > bot.log 2>&1 &
```

#### 使用systemd（推荐）

创建服务文件 `/etc/systemd/system/wecom-bot.service`：

```ini
[Unit]
Description=WeComBot Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/Users/xuexinhai/Desktop/1/wecom_bot
ExecStart=/usr/bin/python3 /Users/xuexinhai/Desktop/1/wecom_bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start wecom-bot
sudo systemctl enable wecom-bot  # 开机自启
sudo systemctl status wecom-bot  # 查看状态
```

## 📝 报告示例

```markdown
## 📊 项目运行日报

**统计日期：** 2025-01-18

---

### 📈 核心指标

- **总请求量：** 125,680 次
- **活跃用户：** 3,256 人
- **平均响应时间：** 156 ms
- **错误率：** 0.23%

---

### 🔥 性能指标

- **CPU使用率：** 45.6%
- **内存使用率：** 62.3%
- **磁盘使用率：** 38.9%

---

### 📉 对比数据

- **较昨日请求量：** ↑ 15.3%
- **较昨日用户数：** ↑ 8.7%

---

> 报告生成时间：2025-01-18 09:00:00
```

## 🐛 故障排除

### 1. 消息发送失败

- 检查Webhook地址是否正确
- 确认网络连接正常
- 查看日志文件 `wecom_bot.log`

### 2. 数据采集异常

- 检查数据库连接配置
- 确认数据库权限
- 查看 `data_collector.py` 中的自定义逻辑

### 3. 定时任务不执行

- 确认系统时区设置
- 检查进程是否正常运行
- 查看日志文件

## 📄 项目结构

```
wecom_bot/
├── config.py              # 配置文件
├── wecom_client.py        # 企业微信客户端
├── data_collector.py      # 数据采集模块
├── scheduler.py           # 定时任务调度
├── main.py                # 主程序入口
├── requirements.txt       # 依赖包
├── README.md              # 使用文档
└── wecom_bot.log          # 运行日志
```

## 💡 最佳实践

1. **数据安全**：不要在代码中硬编码敏感信息，使用环境变量
2. **错误处理**：完善异常处理逻辑，避免程序崩溃
3. **日志管理**：定期清理日志文件，避免占用过多磁盘空间
4. **性能优化**：大量数据统计时注意查询性能
5. **监控告警**：合理设置告警阈值，避免告警风暴

## 📞 技术支持

如有问题或建议，请查看项目文档或联系开发团队。
