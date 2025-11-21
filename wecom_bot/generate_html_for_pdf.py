#!/usr/bin/env python3
"""
使用现有HTML模板生成完整的HTML文件(用于PDF导出)
完全保留原始样式,直接嵌入数据
"""
from user_stats import UserStatsCollector
from datetime import datetime
import os


def generate_html_for_pdf():
    """生成用于PDF导出的HTML文件"""

    print("=" * 60)
    print("🚀 开始生成HTML报告...")
    print("=" * 60)

    # 1. 收集数据
    print("📊 正在收集数据...")
    collector = UserStatsCollector()
    stats_data = collector.get_stats_for_card()

    today = stats_data.get('today', {})
    yesterday = stats_data.get('yesterday', {})

    # 2. 读取原始HTML模板
    print("📄 正在读取HTML模板...")
    with open('report_template_professional.html', 'r', encoding='utf-8') as f:
        html_template = f.read()

    # 3. 替换HTML中的占位符数据
    print("🔄 正在填充真实数据...")

    # 用户统计数据
    html_content = html_template.replace(
        '<div class="card-value" id="total-users">19</div>',
        f'<div class="card-value" id="total-users">{today.get("total_users", 0):,}</div>'
    )

    total_change = today.get('total_users', 0) - yesterday.get('total_users', 0)
    html_content = html_content.replace(
        '<div class="card-subtitle">较昨日 +114</div>',
        f'<div class="card-subtitle">较昨日 {"+' if total_change >= 0 else ''}{total_change}</div>',
        1  # 只替换第一个
    )

    html_content = html_content.replace(
        '<div class="card-value value-increase" id="new-users">+156</div>',
        f'<div class="card-value value-increase" id="new-users">+{today.get("new_users", 0)}</div>'
    )

    html_content = html_content.replace(
        '<div class="card-value value-decrease" id="exit-users">42</div>',
        f'<div class="card-value value-decrease" id="exit-users">{today.get("exit_users", 0)}</div>'
    )

    # 调度统计
    html_content = html_content.replace(
        '<div class="card-value">328</div>',
        f'<div class="card-value">{today.get("dispatch_count", 0)}</div>',
        1  # 只替换调度次数
    )

    # 更新日期
    html_content = html_content.replace(
        '2025年11月19日',
        stats_data.get('date', datetime.now().strftime('%Y年%m月%d日'))
    )

    # 移除JavaScript代码(因为我们已经直接嵌入了数据)
    # 保留样式和结构,只去掉动态脚本
    html_content = html_content.replace(
        'window.addEventListener(\'DOMContentLoaded\', function() {\n            populateData();  // 先填充数据\n            generateReportInfo();  // 再更新时间\n        });',
        'window.addEventListener(\'DOMContentLoaded\', function() {\n            generateReportInfo();  // 只更新时间\n        });'
    )

    # 4. 保存到文件
    output_filename = f"VPP运维报告_完整版_{stats_data.get('date', datetime.now().strftime('%Y年%m月%d日'))}.html"

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 5. 获取绝对路径
    abs_path = os.path.abspath(output_filename)

    print("=" * 60)
    print("✅ HTML报告生成成功!")
    print("=" * 60)
    print(f"文件名: {output_filename}")
    print(f"完整路径: {abs_path}")
    print("=" * 60)
    print("使用方法:")
    print("1. 双击HTML文件在浏览器中打开")
    print("2. 按 Cmd+P 打开打印对话框")
    print("3. 选择'存储为PDF'")
    print("4. PDF将完美保留所有样式和数据!")
    print("=" * 60)

    return abs_path


if __name__ == "__main__":
    generate_html_for_pdf()
