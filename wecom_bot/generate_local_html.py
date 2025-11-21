#!/usr/bin/env python3
"""
生成本地HTML报告文件
可以直接在浏览器中打开，无需运行服务器
"""
from user_stats import UserStatsCollector
from datetime import datetime
import os


def generate_local_html_report():
    """生成本地HTML报告文件"""

    # 1. 收集数据
    collector = UserStatsCollector()
    stats_data = collector.get_stats_for_card()

    today_data = stats_data.get('today', {})
    yesterday_data = stats_data.get('yesterday', {})

    # 2. 计算对比数据
    total_change = today_data.get('total_users', 0) - yesterday_data.get('total_users', 0)

    # 3. 生成HTML内容（审计风格：黑白+荧光绿）
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VPP运维审计报告 - {stats_data.get('date', 'N/A')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'SF Mono', 'Monaco', 'Consolas', 'Courier New', monospace;
            background: #0a0a0a;
            color: #ffffff;
            padding: 40px 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #1a1a1a;
            border: 2px solid #00ff41;
            padding: 60px;
        }}

        .header {{
            border-bottom: 1px solid #333;
            padding-bottom: 30px;
            margin-bottom: 50px;
        }}

        .header h1 {{
            font-size: 32px;
            font-weight: 400;
            color: #00ff41;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }}

        .header .subtitle {{
            font-size: 13px;
            color: #888;
            letter-spacing: 1px;
            font-weight: 300;
        }}

        .section-title {{
            font-size: 14px;
            font-weight: 400;
            color: #00ff41;
            margin-bottom: 30px;
            padding-bottom: 8px;
            border-bottom: 1px solid #00ff41;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        .cards-row {{
            display: flex;
            gap: 30px;
            margin-bottom: 50px;
        }}

        .metric-card {{
            flex: 1;
            background: #1a1a1a;
            border: 1px solid #333;
            padding: 0;
            transition: all 0.3s ease;
        }}

        .metric-card:hover {{
            border-color: #00ff41;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
        }}

        .card-header {{
            background: #0a0a0a;
            padding: 15px 20px;
            border-bottom: 1px solid #00ff41;
        }}

        .card-title {{
            font-size: 11px;
            color: #888;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 400;
        }}

        .card-body {{
            padding: 40px 20px 30px;
            text-align: center;
        }}

        .card-value {{
            font-size: 56px;
            font-weight: 300;
            color: #00ff41;
            margin-bottom: 20px;
            line-height: 1;
            letter-spacing: -2px;
        }}

        .card-subtitle {{
            font-size: 12px;
            color: #666;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-weight: 300;
        }}

        .trend-indicator {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 5px;
        }}

        .trend-up {{
            background: #00ff41;
            box-shadow: 0 0 10px #00ff41;
        }}

        .trend-down {{
            background: #ff4136;
            box-shadow: 0 0 10px #ff4136;
        }}

        .trend-neutral {{
            background: #888;
        }}

        .footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid #333;
            color: #666;
            font-size: 11px;
            letter-spacing: 1px;
        }}

        .export-btn {{
            display: inline-block;
            margin: 30px auto 50px;
            padding: 12px 40px;
            background: transparent;
            color: #00ff41;
            border: 1px solid #00ff41;
            font-size: 11px;
            font-weight: 400;
            cursor: pointer;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            font-family: 'SF Mono', 'Monaco', 'Consolas', 'Courier New', monospace;
        }}

        .export-btn:hover {{
            background: #00ff41;
            color: #0a0a0a;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }}

        .data-grid {{
            position: relative;
            padding: 20px 0;
        }}

        .data-grid::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image:
                repeating-linear-gradient(0deg, transparent, transparent 19px, #111 19px, #111 20px),
                repeating-linear-gradient(90deg, transparent, transparent 19px, #111 19px, #111 20px);
            opacity: 0.3;
            pointer-events: none;
        }}

        @media print {{
            body {{
                background: white !important;
                color: black !important;
                padding: 20px !important;
            }}

            .container {{
                background: white !important;
                border: 2px solid black !important;
                padding: 40px !important;
            }}

            .header {{
                border-bottom: 2px solid black !important;
            }}

            .header h1 {{
                color: black !important;
            }}

            .header .subtitle {{
                color: #333 !important;
            }}

            .section-title {{
                color: black !important;
                border-bottom: 2px solid black !important;
            }}

            .export-btn {{
                display: none !important;
            }}

            .data-grid::before {{
                display: none !important;
            }}

            .metric-card {{
                background: white !important;
                border: 1px solid black !important;
                page-break-inside: avoid;
            }}

            .card-header {{
                background: #f5f5f5 !important;
                border-bottom: 1px solid black !important;
            }}

            .card-title {{
                color: #333 !important;
            }}

            .card-value {{
                color: black !important;
            }}

            .card-subtitle {{
                color: #333 !important;
            }}

            .trend-indicator {{
                border: 1px solid black !important;
            }}

            .trend-up {{
                background: black !important;
                box-shadow: none !important;
            }}

            .trend-down {{
                background: #666 !important;
                box-shadow: none !important;
            }}

            .trend-neutral {{
                background: #999 !important;
            }}

            .footer {{
                color: #333 !important;
                border-top: 1px solid black !important;
            }}
        }}

        @media (max-width: 768px) {{
            .cards-row {{
                flex-direction: column;
            }}

            .container {{
                padding: 30px 20px;
            }}

            .card-value {{
                font-size: 42px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>VPP 运维审计报告</h1>
            <p class="subtitle">{stats_data.get('date', 'N/A')} | OPERATIONAL AUDIT REPORT</p>
        </div>

        <!-- Export Button -->
        <div style="text-align: center;">
            <button class="export-btn" onclick="window.print()">[ EXPORT PDF ]</button>
        </div>

        <!-- Section: User Data -->
        <h2 class="section-title">User Metrics Overview</h2>
        <div class="data-grid">
            <div class="cards-row">
                <!-- Card 1: Total Users -->
                <div class="metric-card">
                    <div class="card-header">
                        <div class="card-title">Total Users</div>
                    </div>
                    <div class="card-body">
                        <div class="card-value">{today_data.get('total_users', 0):,}</div>
                        <div class="card-subtitle">
                            <span class="trend-indicator {'trend-up' if total_change > 0 else 'trend-down' if total_change < 0 else 'trend-neutral'}"></span>
                            <span>{'+' if total_change >= 0 else ''}{total_change} from yesterday</span>
                        </div>
                    </div>
                </div>

                <!-- Card 2: New Users -->
                <div class="metric-card">
                    <div class="card-header">
                        <div class="card-title">New Users</div>
                    </div>
                    <div class="card-body">
                        <div class="card-value">+{today_data.get('new_users', 0)}</div>
                        <div class="card-subtitle">
                            <span class="trend-indicator trend-up"></span>
                            <span>{today_data.get('new_users', 0)} joined today</span>
                        </div>
                    </div>
                </div>

                <!-- Card 3: Exit Users -->
                <div class="metric-card">
                    <div class="card-header">
                        <div class="card-title">Exit Users</div>
                    </div>
                    <div class="card-body">
                        <div class="card-value">{today_data.get('exit_users', 0)}</div>
                        <div class="card-subtitle">
                            <span class="trend-indicator trend-down"></span>
                            <span>{today_data.get('exit_users', 0)} left today</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>REPORT GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC+8</p>
        </div>
    </div>
</body>
</html>
"""

    # 4. 保存到文件
    output_file = f"VPP运维报告_{stats_data.get('date', datetime.now().strftime('%Y年%m月%d日'))}.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 5. 获取绝对路径
    abs_path = os.path.abspath(output_file)

    print("=" * 60)
    print("✓ HTML报告生成成功！")
    print("=" * 60)
    print(f"文件名: {output_file}")
    print(f"完整路径: {abs_path}")
    print("=" * 60)
    print("使用方法:")
    print("1. 双击HTML文件在浏览器中打开")
    print("2. 点击页面上的'📥 导出为 PDF'按钮")
    print("3. 或按 Cmd+P 使用浏览器打印功能导出PDF")
    print("=" * 60)

    return abs_path


if __name__ == "__main__":
    generate_local_html_report()
