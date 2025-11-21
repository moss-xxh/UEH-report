#!/usr/bin/env python3
"""
直接生成PDF报告文件
不需要浏览器,直接从数据生成PDF
"""
from weasyprint import HTML, CSS
from user_stats import UserStatsCollector
from datetime import datetime
import os


def generate_pdf_report():
    """生成PDF报告"""

    print("=" * 60)
    print("🚀 开始生成PDF报告...")
    print("=" * 60)

    # 1. 收集数据
    print("📊 正在收集数据...")
    collector = UserStatsCollector()
    stats_data = collector.get_stats_for_card()

    today = stats_data.get('today', {})
    yesterday = stats_data.get('yesterday', {})

    # 2. 生成HTML内容(嵌入所有数据,不使用JavaScript)
    print("📝 正在生成HTML内容...")
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>VPP运维报告 - {stats_data.get('date', 'N/A')}</title>
    <style>
        @page {{
            size: A4;
            margin: 15mm;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            color: #000;
            line-height: 1.6;
        }}

        .header {{
            border-bottom: 2px solid #000;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .header .date {{
            font-size: 14px;
            color: #666;
        }}

        .section {{
            margin-bottom: 40px;
            page-break-inside: avoid;
        }}

        .section-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 20px;
            border-bottom: 1px solid #000;
            padding-bottom: 8px;
        }}

        .section-subtitle {{
            font-size: 16px;
            font-weight: 600;
            margin: 20px 0 15px 0;
        }}

        .cards-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }}

        .metric-card {{
            background: #f5f5f5;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}

        .card-label {{
            font-size: 12px;
            color: #666;
            margin-bottom: 8px;
        }}

        .card-value {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 6px;
        }}

        .card-subtitle {{
            font-size: 11px;
            color: #888;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 12px;
        }}

        table th {{
            background: #333;
            color: #fff;
            padding: 10px 8px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #000;
        }}

        table td {{
            padding: 8px;
            border: 1px solid #ddd;
        }}

        table tbody tr:nth-child(even) {{
            background: #f9f9f9;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 11px;
            color: #666;
        }}
    </style>
</head>
<body>
    <!-- 页眉 -->
    <div class="header">
        <h1>VPP 运维数据报告</h1>
        <p class="date">{stats_data.get('date', 'N/A')}</p>
    </div>

    <!-- 1. 用户统计 -->
    <div class="section">
        <h2 class="section-title">1. 用户统计</h2>

        <div class="cards-grid">
            <div class="metric-card">
                <div class="card-label">总用户数</div>
                <div class="card-value">{today.get('total_users', 0):,}</div>
                <div class="card-subtitle">较昨日 {'+' if (today.get('total_users', 0) - yesterday.get('total_users', 0)) >= 0 else ''}{today.get('total_users', 0) - yesterday.get('total_users', 0)}</div>
            </div>

            <div class="metric-card">
                <div class="card-label">新增用户</div>
                <div class="card-value">+{today.get('new_users', 0):,}</div>
                <div class="card-subtitle">今日新增</div>
            </div>

            <div class="metric-card">
                <div class="card-label">退出用户</div>
                <div class="card-value">{today.get('exit_users', 0):,}</div>
                <div class="card-subtitle">今日退出</div>
            </div>
        </div>

        <h3 class="section-subtitle">地区分布</h3>
        <table>
            <thead>
                <tr>
                    <th>地区</th>
                    <th>设备数量</th>
                    <th>占比</th>
                </tr>
            </thead>
            <tbody>
"""

    # 添加地区分布数据
    device_by_region = today.get('device_by_region', {})
    total_devices = sum(device_by_region.values()) if device_by_region else 1

    for region, count in sorted(device_by_region.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_devices * 100) if total_devices > 0 else 0
        html_content += f"""
                <tr>
                    <td>{region}</td>
                    <td>{count:,}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
"""

    html_content += """
            </tbody>
        </table>

        <h3 class="section-subtitle">品牌分布</h3>
        <table>
            <thead>
                <tr>
                    <th>品牌</th>
                    <th>设备数量</th>
                    <th>占比</th>
                </tr>
            </thead>
            <tbody>
"""

    # 添加品牌分布数据
    device_by_brand = today.get('device_by_brand', {})
    total_brand_devices = sum(device_by_brand.values()) if device_by_brand else 1

    for brand, count in sorted(device_by_brand.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_brand_devices * 100) if total_brand_devices > 0 else 0
        html_content += f"""
                <tr>
                    <td>{brand}</td>
                    <td>{count:,}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
"""

    html_content += """
            </tbody>
        </table>
    </div>

    <!-- 2. 调度统计 -->
    <div class="section">
        <h2 class="section-title">2. 调度统计</h2>

        <div class="cards-grid">
            <div class="metric-card">
                <div class="card-label">调度次数</div>
                <div class="card-value">{:,}</div>
                <div class="card-subtitle">今日调度</div>
            </div>

            <div class="metric-card">
                <div class="card-label">充电次数</div>
                <div class="card-value">{:,}</div>
                <div class="card-subtitle">今日充电</div>
            </div>

            <div class="metric-card">
                <div class="card-label">放电次数</div>
                <div class="card-value">{:,}</div>
                <div class="card-subtitle">今日放电</div>
            </div>
        </div>

        <h3 class="section-subtitle">地区调度详情</h3>
        <table>
            <thead>
                <tr>
                    <th>地区</th>
                    <th>调度次数</th>
                    <th>设备数量</th>
                    <th>馈网量(kWh)</th>
                    <th>获利($)</th>
                </tr>
            </thead>
            <tbody>
""".format(
        today.get('dispatch_count', 0),
        today.get('charge_count', 0),
        today.get('discharge_count', 0)
    )

    # 添加地区运行数据
    regional_operation = stats_data.get('regional_operation', [])[:5]  # 只取前5个地区
    for region_data in regional_operation:
        html_content += f"""
                <tr>
                    <td>{region_data.get('region', 'N/A')}</td>
                    <td>{region_data.get('dispatch_count', 0)}</td>
                    <td>{region_data.get('device_count', 0):,}</td>
                    <td>{region_data.get('grid_power', 0):.1f}</td>
                    <td>${region_data.get('profit', 0):.2f}</td>
                </tr>
"""

    html_content += """
            </tbody>
        </table>

        <h3 class="section-subtitle">调度记录明细</h3>
        <table>
            <thead>
                <tr>
                    <th>时间</th>
                    <th>地区</th>
                    <th>指令</th>
                    <th>设备数</th>
                    <th>下发成功率</th>
                    <th>停止成功率</th>
                </tr>
            </thead>
            <tbody>
"""

    # 添加调度记录
    dispatch_records = stats_data.get('dispatch_records', [])
    for record in dispatch_records:
        html_content += f"""
                <tr>
                    <td>{record.get('time', 'N/A')}</td>
                    <td>{record.get('region', 'N/A')}</td>
                    <td>{record.get('command', 'N/A')}</td>
                    <td>{record.get('device_count', 0)}</td>
                    <td>{record.get('start_success_rate', 0):.1f}%</td>
                    <td>{record.get('stop_success_rate', 0):.1f}%</td>
                </tr>
"""

    html_content += """
            </tbody>
        </table>

        <h3 class="section-subtitle">异常情况记录</h3>
        <table>
            <thead>
                <tr>
                    <th>时间</th>
                    <th>地区</th>
                    <th>指令</th>
                    <th>设备序列号</th>
                    <th>品牌</th>
                    <th>重试次数</th>
                    <th>异常原因</th>
                </tr>
            </thead>
            <tbody>
"""

    # 添加异常记录
    exceptions = stats_data.get('exceptions', [])
    for exc in exceptions:
        html_content += f"""
                <tr>
                    <td>{exc.get('time', 'N/A')}</td>
                    <td>{exc.get('region', 'N/A')}</td>
                    <td>{exc.get('command', 'N/A')}</td>
                    <td>{exc.get('sn', 'N/A')}</td>
                    <td>{exc.get('brand', 'N/A')}</td>
                    <td>{exc.get('retry_count', 0)}</td>
                    <td>{exc.get('error_reason', 'N/A')}</td>
                </tr>
"""

    html_content += f"""
            </tbody>
        </table>
    </div>

    <!-- 页脚 -->
    <div class="footer">
        <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>旭衡电子（深圳）有限公司 VPP 虚拟电厂监控平台</p>
    </div>
</body>
</html>
"""

    # 3. 生成PDF文件
    print("🔄 正在转换为PDF...")
    output_filename = f"VPP运维报告_{stats_data.get('date', datetime.now().strftime('%Y年%m月%d日'))}.pdf"

    # 使用WeasyPrint转换
    HTML(string=html_content).write_pdf(output_filename)

    # 4. 获取绝对路径
    abs_path = os.path.abspath(output_filename)

    print("=" * 60)
    print("✅ PDF报告生成成功!")
    print("=" * 60)
    print(f"文件名: {output_filename}")
    print(f"完整路径: {abs_path}")
    print(f"文件大小: {os.path.getsize(output_filename) / 1024:.1f} KB")
    print("=" * 60)
    print("📂 您可以直接双击打开PDF文件查看")
    print("=" * 60)

    return abs_path


if __name__ == "__main__":
    generate_pdf_report()
