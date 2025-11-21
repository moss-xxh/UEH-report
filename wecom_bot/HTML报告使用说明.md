# VPP HTML报告系统使用说明

## 📋 系统概述

VPP HTML报告系统提供了现代化的数据可视化界面，支持浏览器直接预览和导出为PDF。

## 🚀 快速开始

### 1. 启动报告服务

```bash
# 在项目目录下启动Flask服务
python3 pdf_server.py
```

服务启动后，访问地址：
- **主页**: http://127.0.0.1:8080
- **HTML报告**: http://127.0.0.1:8080/report/html
- **PDF报告**: http://127.0.0.1:8080/report/pdf（旧版，不推荐）
- **统计数据API**: http://127.0.0.1:8080/api/stats
- **健康检查**: http://127.0.0.1:8080/health

### 2. 发送企业微信通知

```bash
# 测试模式：立即发送一次
python3 send_user_stats.py --test

# 正常模式：定时每日推送
python3 send_user_stats.py
```

## 📊 功能特性

### HTML报告特性

✅ **现代设计风格**
- 渐变色卡片设计（Material Design风格）
- 响应式布局，支持移动端访问
- 平滑动画和交互效果

✅ **核心数据展示**
- **Total Users**: 总用户数，对比昨日变化
- **New Users**: 今日新增用户
- **Exit Users**: 今日退出用户

✅ **导出功能**
- 点击"📥 导出为 PDF"按钮
- 使用浏览器打印功能导出
- 支持Chrome、Safari、Edge等主流浏览器

### 企业微信卡片集成

企业微信卡片中点击"**查看详细数据**"按钮，将直接打开HTML报告页面。

卡片显示内容：
- 📊 VPP运行报告标题
- 💰 今日获利（重点展示）
- ⚡ 累计馈网量
- 🔄 调度次数、充电次数、放电次数
- 👥 用户数据（总用户、新增、退出）
- 📋 地区调度详情表格

## 🎨 设计规范

### 配色方案

| 卡片类型 | 渐变色 | 用途 |
|---------|--------|------|
| Total Users | `#667eea → #764ba2` (紫色) | 总用户数 |
| New Users | `#06beb6 → #48b1bf` (青色) | 新增用户 |
| Exit Users | `#fc4a1a → #f7b733` (橙色) | 退出用户 |

### 趋势指示器

- ▲ 绿色 (`#4CAF50`): 上升趋势
- ▼ 红色 (`#F44336`): 下降趋势
- ● 灰色 (`#9E9E9E`): 无变化

## 🔧 技术架构

### 后端 (Flask)

```python
# pdf_server.py
@app.route('/report/html')
def generate_html_report():
    """生成并返回HTML报告"""
    # 1. 收集数据
    collector = UserStatsCollector()
    stats_data = collector.get_stats_for_card()

    # 2. 读取HTML模板
    with open('report_template.html', 'r', encoding='utf-8') as f:
        html_template = f.read()

    # 3. 注入实时数据
    html_content = html_template.replace(
        'const data = {',
        f'''const data = {{
            date: '{stats_data.get("date", "N/A")}',
            total_users: {stats_data.get("today", {}).get("total_users", 0)},
            ...
        }}'''
    )

    # 4. 返回HTML
    return Response(html_content, mimetype='text/html')
```

### 前端 (HTML + CSS + JavaScript)

**核心技术栈：**
- HTML5 语义化标签
- CSS3 渐变、阴影、动画
- Flexbox 响应式布局
- JavaScript 数据动态渲染
- Print Media Query 打印样式

**文件结构：**
```
report_template.html
├── <head>
│   ├── Meta 信息
│   └── <style> CSS样式
└── <body>
    ├── Header (标题、日期)
    ├── Export Button (导出按钮)
    ├── Section: 用户数据概览
    │   └── Cards Row (3个指标卡片)
    ├── Footer (生成时间)
    └── <script> JavaScript逻辑
```

## 📱 导出PDF

### 方法1：浏览器打印（推荐）

1. 点击页面上的"📥 导出为 PDF"按钮
2. 浏览器将打开打印对话框
3. 选择"另存为PDF"
4. 调整页面设置（建议取消页眉页脚）
5. 保存PDF文件

### 方法2：浏览器菜单

1. 在HTML报告页面，按 `Cmd+P` (Mac) 或 `Ctrl+P` (Windows)
2. 目标打印机选择"另存为PDF"
3. 保存文件

### 打印设置建议

- ✅ 取消勾选"页眉和页脚"
- ✅ 勾选"背景图形"（显示渐变色）
- ✅ 页边距：默认或最小
- ✅ 缩放：100%

## 🛠️ 自定义扩展

### 添加新的数据模块

编辑 `report_template.html`，在用户数据模块后添加：

```html
<!-- 新模块：VPP运行数据 -->
<h2 class="section-title">VPP运行数据</h2>
<div class="cards-row">
    <!-- 调度次数卡片 -->
    <div class="metric-card">
        <div class="card-header gradient-purple">
            Dispatch Count
        </div>
        <div class="card-body">
            <div class="card-value" id="dispatch-count">328</div>
            <div class="card-subtitle">
                <span>今日调度次数</span>
            </div>
        </div>
    </div>

    <!-- 更多卡片... -->
</div>
```

### 修改配色方案

编辑 `report_template.html` 中的 CSS：

```css
.card-header.gradient-purple {
    background: linear-gradient(135deg, #新颜色1 0%, #新颜色2 100%);
}
```

### 注入新数据字段

编辑 `pdf_server.py` 的 `generate_html_report()` 函数：

```python
html_content = html_template.replace(
    'const data = {',
    f'''const data = {{
        date: '{stats_data.get("date", "N/A")}',
        total_users: {stats_data.get("today", {}).get("total_users", 0)},
        新字段: {新数据值},  # 添加新字段
        ...
    }}'''
)
```

## 📊 数据来源

### UserStatsCollector

数据收集器位于 `user_stats.py`，提供以下数据：

```python
{
    "date": "2025年11月18日",
    "today": {
        "total_users": 19,      # 总用户数
        "new_users": 156,          # 新增用户
        "exit_users": 42,          # 退出用户
        "dispatch_count": 328,     # 调度次数
        "charge_count": 185,       # 充电次数
        "discharge_count": 143,    # 放电次数
        "grid_power": 2856.5,      # 累计馈网量(kWh)
        "profit": 4285.75          # 获利(元)
    },
    "yesterday": { ... },          # 昨日数据
    "regional_details": [ ... ]    # 地区调度详情
}
```

## 🐛 常见问题

### Q1: 为什么HTML显示正常但导出PDF后渐变色消失？

**A:** 在打印设置中勾选"背景图形"选项。

### Q2: 中文字体在PDF中显示异常？

**A:** HTML版本使用浏览器字体渲染，不会出现字体问题。如果使用旧版PDF生成（reportlab），需要注册中文字体。

### Q3: 如何修改报告生成时间？

**A:** 编辑 `config.py` 中的配置：

```python
STATS_CONFIG = {
    'schedule': {
        'daily_report_time': '09:00'  # 修改为你想要的时间
    }
}
```

### Q4: Flask服务端口被占用怎么办？

**A:** 修改 `pdf_server.py` 中的端口号：

```python
app.run(
    host='0.0.0.0',
    port=8080,  # 改为其他端口，如 8081
    debug=True
)
```

同时更新 `wecom_client.py` 中的URL地址。

## 📝 版本历史

### v2.0 (当前版本) - HTML版本

- ✅ 使用HTML+CSS替代PDF生成
- ✅ 支持浏览器打印导出PDF
- ✅ 现代化渐变卡片设计
- ✅ 完美支持中文和emoji
- ✅ 响应式移动端适配

### v1.0 - PDF版本（已弃用）

- ❌ 使用reportlab生成PDF
- ❌ emoji显示为白色方块
- ❌ 中文字体需要特殊处理
- ❌ 布局对齐问题

## 🔗 相关文件

| 文件 | 说明 |
|-----|------|
| `pdf_server.py` | Flask Web服务器 |
| `report_template.html` | HTML报告模板 |
| `wecom_client.py` | 企业微信客户端 |
| `user_stats.py` | 数据收集器 |
| `send_user_stats.py` | 消息发送主程序 |
| `config.py` | 配置文件 |

## 💡 最佳实践

1. **定期备份配置**: `config.py` 包含webhook密钥，请妥善保管
2. **监控服务状态**: 使用 `/health` 接口监控Flask服务
3. **日志查看**: 查看 `pdf_server.log` 排查问题
4. **测试先行**: 使用 `--test` 参数测试消息发送
5. **浏览器兼容**: 推荐使用Chrome或Edge浏览器导出PDF

## 🎯 下一步计划

- [ ] 添加更多VPP运行数据模块
- [ ] 地区调度详情表格可视化
- [ ] 历史数据趋势图表
- [ ] 数据导出Excel功能
- [ ] 移动端App适配

---

**更新时间**: 2025-11-18
**文档版本**: v2.0
**维护者**: VPP开发团队
