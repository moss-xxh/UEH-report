#!/usr/bin/env python3
"""
使用ReportLab直接生成PDF报告
纯Python实现,无需系统依赖
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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

    # 2. 准备PDF文件
    output_filename = f"VPP运维报告_{stats_data.get('date', datetime.now().strftime('%Y年%m月%d日'))}.pdf"
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )

    # 3. 准备样式
    styles = getSampleStyleSheet()

    # 标题样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#000000'),
        spaceAfter=12,
        alignment=1  # 居中
    )

    # 章节标题样式
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#000000'),
        spaceAfter=10,
        spaceBefore=15
    )

    # 子标题样式
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        spaceBefore=10
    )

    # 正文样式
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#000000')
    )

    # 4. 构建PDF内容
    print("📝 正在生成PDF内容...")
    story = []

    # 标题
    story.append(Paragraph("VPP 运维数据报告", title_style))
    story.append(Paragraph(f"报告日期: {stats_data.get('date', 'N/A')}", normal_style))
    story.append(Spacer(1, 20))

    # ===== 1. 用户统计 =====
    story.append(Paragraph("1. 用户统计", heading_style))

    # 用户统计卡片数据
    user_stats_data = [
        ['指标', '数值', '变化'],
        ['总用户数', f"{today.get('total_users', 0):,}",
         f"较昨日 {'+' if (today.get('total_users', 0) - yesterday.get('total_users', 0)) >= 0 else ''}{today.get('total_users', 0) - yesterday.get('total_users', 0)}"],
        ['新增用户', f"+{today.get('new_users', 0):,}", '今日新增'],
        ['退出用户', f"{today.get('exit_users', 0):,}", '今日退出']
    ]

    user_stats_table = Table(user_stats_data, colWidths=[60*mm, 60*mm, 60*mm])
    user_stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    story.append(user_stats_table)
    story.append(Spacer(1, 15))

    # 地区分布
    story.append(Paragraph("地区分布", subheading_style))
    device_by_region = today.get('device_by_region', {})
    total_devices = sum(device_by_region.values()) if device_by_region else 1

    region_data = [['地区', '设备数量', '占比']]
    for region, count in sorted(device_by_region.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_devices * 100) if total_devices > 0 else 0
        region_data.append([region, f"{count:,}", f"{percentage:.1f}%"])

    region_table = Table(region_data, colWidths=[60*mm, 60*mm, 60*mm])
    region_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    story.append(region_table)
    story.append(Spacer(1, 15))

    # 品牌分布
    story.append(Paragraph("品牌分布", subheading_style))
    device_by_brand = today.get('device_by_brand', {})
    total_brand_devices = sum(device_by_brand.values()) if device_by_brand else 1

    brand_data = [['品牌', '设备数量', '占比']]
    for brand, count in sorted(device_by_brand.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_brand_devices * 100) if total_brand_devices > 0 else 0
        brand_data.append([brand, f"{count:,}", f"{percentage:.1f}%"])

    brand_table = Table(brand_data, colWidths=[60*mm, 60*mm, 60*mm])
    brand_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    story.append(brand_table)
    story.append(Spacer(1, 20))

    # ===== 2. 调度统计 =====
    story.append(Paragraph("2. 调度统计", heading_style))

    # 调度统计卡片
    dispatch_stats_data = [
        ['调度次数', '充电次数', '放电次数'],
        [
            f"{today.get('dispatch_count', 0):,}",
            f"{today.get('charge_count', 0):,}",
            f"{today.get('discharge_count', 0):,}"
        ]
    ]

    dispatch_stats_table = Table(dispatch_stats_data, colWidths=[60*mm, 60*mm, 60*mm])
    dispatch_stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 14),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
    ]))
    story.append(dispatch_stats_table)
    story.append(Spacer(1, 15))

    # 地区调度详情
    story.append(Paragraph("地区调度详情(前5)", subheading_style))
    regional_operation = stats_data.get('regional_operation', [])[:5]

    regional_data = [['地区', '调度次数', '设备数量', '馈网量(kWh)', '获利($)']]
    for region_data in regional_operation:
        regional_data.append([
            region_data.get('region', 'N/A'),
            str(region_data.get('dispatch_count', 0)),
            f"{region_data.get('device_count', 0):,}",
            f"{region_data.get('grid_power', 0):.1f}",
            f"${region_data.get('profit', 0):.2f}"
        ])

    regional_table = Table(regional_data, colWidths=[35*mm, 35*mm, 35*mm, 40*mm, 35*mm])
    regional_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(regional_table)
    story.append(Spacer(1, 15))

    # 调度记录明细
    story.append(Paragraph("调度记录明细", subheading_style))
    dispatch_records = stats_data.get('dispatch_records', [])

    dispatch_data = [['时间', '地区', '指令', '设备数', '下发成功率', '停止成功率']]
    for record in dispatch_records:
        dispatch_data.append([
            record.get('time', 'N/A'),
            record.get('region', 'N/A'),
            record.get('command', 'N/A'),
            str(record.get('device_count', 0)),
            f"{record.get('start_success_rate', 0):.1f}%",
            f"{record.get('stop_success_rate', 0):.1f}%"
        ])

    dispatch_table = Table(dispatch_data, colWidths=[25*mm, 25*mm, 25*mm, 30*mm, 35*mm, 35*mm])
    dispatch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(dispatch_table)
    story.append(Spacer(1, 20))

    # ===== 3. 异常情况 =====
    story.append(Paragraph("3. 异常情况记录", heading_style))
    exceptions = stats_data.get('exceptions', [])

    exception_data = [['时间', '地区', '指令', '序列号', '品牌', '重试', '原因']]
    for exc in exceptions:
        exception_data.append([
            exc.get('time', 'N/A')[-8:],  # 只取时间部分
            exc.get('region', 'N/A'),
            exc.get('command', 'N/A'),
            exc.get('sn', 'N/A')[:12] + '...',  # 缩短序列号
            exc.get('brand', 'N/A')[:8],
            str(exc.get('retry_count', 0)),
            exc.get('error_reason', 'N/A')[:10]  # 缩短原因
        ])

    exception_table = Table(exception_data, colWidths=[24*mm, 20*mm, 24*mm, 32*mm, 22*mm, 16*mm, 32*mm])
    exception_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#333333')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
    ]))
    story.append(exception_table)
    story.append(Spacer(1, 30))

    # 页脚
    footer_text = f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 旭衡电子（深圳）有限公司 VPP 虚拟电厂监控平台"
    story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey, alignment=1)))

    # 5. 生成PDF
    print("🔄 正在写入PDF文件...")
    doc.build(story)

    # 6. 输出结果
    abs_path = os.path.abspath(output_filename)
    file_size = os.path.getsize(output_filename) / 1024

    print("=" * 60)
    print("✅ PDF报告生成成功!")
    print("=" * 60)
    print(f"文件名: {output_filename}")
    print(f"完整路径: {abs_path}")
    print(f"文件大小: {file_size:.1f} KB")
    print("=" * 60)
    print("📂 您可以直接双击打开PDF文件查看")
    print("=" * 60)

    return abs_path


if __name__ == "__main__":
    generate_pdf_report()
