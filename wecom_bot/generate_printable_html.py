#!/usr/bin/env python3
"""
生成用于打印的简洁HTML文件
完全保留原始样式,但简化结构
"""
from user_stats import UserStatsCollector
from datetime import datetime
import os


def generate_print_html():
    """生成可打印的HTML"""

    print("=" * 60)
    print("🚀 正在生成可打印HTML...")
    print("=" * 60)

    # 收集数据
    collector = UserStatsCollector()
    stats_data = collector.get_stats_for_card()

    today = stats_data.get('today', {})
    yesterday = stats_data.get('yesterday', {})

    # 生成HTML
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>VPP运维报告 - {stats_data.get('date', 'N/A')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: #ffffff;
            color: #000000;
            line-height: 1.6;
            padding: 40px;
        }}

        h1 {{
            font-size: 28px;
            margin-bottom: 8px;
            border-bottom: 2px solid #000;
            padding-bottom: 15px;
        }}

        .date {{
            font-size: 14px;
            color: #666;
            margin-bottom: 30px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 20px;
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
            gap: 20px;
            margin-bottom: 25px;
        }}

        .metric-card {{
            background: #f5f5f7;
            padding: 28px 24px;
            border-radius: 12px;
            border: 1px solid #ddd;
        }}

        .card-label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 12px;
        }}

        .card-value {{
            font-size: 36px;
            font-weight: 700;
            color: #000;
            margin-bottom: 8px;
        }}

        .card-subtitle {{
            font-size: 14px;
            color: #888;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}

        table th {{
            background: #333;
            color: #fff;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #000;
        }}

        table td {{
            padding: 10px 12px;
            border: 1px solid #ddd;
        }}

        table tbody tr:nth-child(even) {{
            background: #f9f9f9;
        }}

        /* 打印样式优化 */
        @media print {{
            /* 强制打印背景颜色 */
            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                color-adjust: exact !important;
            }}

            /* 移除页边距 */
            @page {{
                margin: 0;
                size: A4 portrait;
            }}

            body {{
                background: white;
                padding: 20px !important;
                margin: 0 !important;
            }}

            /* 防止元素跨页分割 */
            .section,
            .metric-card,
            table {{
                page-break-inside: avoid;
            }}

            /* 表格优化 */
            table {{
                page-break-after: auto;
            }}

            table tr {{
                page-break-inside: avoid;
                page-break-after: auto;
            }}

            /* 确保标题不在页面底部孤立 */
            h2, h3 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
    <h1>VPP 运维数据报告</h1>
    <p class="date">{stats_data.get('date', 'N/A')}</p>

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

    # 地区数据
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

    html_content += f"""
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

    # 品牌数据
    device_by_brand = today.get('device_by_brand', {})
    total_brand = sum(device_by_brand.values()) if device_by_brand else 1

    for brand, count in sorted(device_by_brand.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_brand * 100) if total_brand > 0 else 0
        html_content += f"""
                <tr>
                    <td>{brand}</td>
                    <td>{count:,}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
"""

    html_content += f"""
            </tbody>
        </table>
    </div>

    <!-- 2. 调度统计 -->
    <div class="section">
        <h2 class="section-title">2. 调度统计</h2>

        <div class="cards-grid">
            <div class="metric-card">
                <div class="card-label">调度次数</div>
                <div class="card-value">{today.get('dispatch_count', 0):,}</div>
                <div class="card-subtitle">今日调度</div>
            </div>

            <div class="metric-card">
                <div class="card-label">充电次数</div>
                <div class="card-value">{today.get('charge_count', 0):,}</div>
                <div class="card-subtitle">今日充电</div>
            </div>

            <div class="metric-card">
                <div class="card-label">放电次数</div>
                <div class="card-value">{today.get('discharge_count', 0):,}</div>
                <div class="card-subtitle">今日放电</div>
            </div>
        </div>

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

    # 调度记录
    for record in stats_data.get('dispatch_records', []):
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

    html_content += f"""
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
                    <th>重试</th>
                    <th>异常原因</th>
                </tr>
            </thead>
            <tbody>
"""

    # 异常记录
    for exc in stats_data.get('exceptions', []):
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

    <p style="text-align: center; margin-top: 40px; font-size: 12px; color: #666;">
        报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 旭衡电子（深圳）有限公司
    </p>
</body>
</html>
"""

    # 保存文件
    output_file = f"VPP运维报告_打印版_{stats_data.get('date', datetime.now().strftime('%Y年%m月%d日'))}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    abs_path = os.path.abspath(output_file)

    print("✅ HTML生成成功!")
    print(f"文件: {output_file}")
    print(f"路径: {abs_path}")
    print("=" * 60)

    return abs_path


if __name__ == "__main__":
    generate_print_html()
