#!/usr/bin/env python3
"""
PDF报告生成模块 - 现代设计风格
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as pdf_canvas
from datetime import datetime
from typing import Dict
import io


class ModernMetricCard(Flowable):
    """现代化指标卡片 - 简洁专业版"""

    def __init__(self, title, value, subtitle="", gradient_start="#667eea",
                 gradient_end="#764ba2", trend="neutral", width=5.5*cm, height=6*cm):
        Flowable.__init__(self)
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.gradient_start = colors.HexColor(gradient_start)
        self.gradient_end = colors.HexColor(gradient_end)
        self.trend = trend
        self.width = width
        self.height = height

    def draw(self):
        """绘制现代化指标卡片"""
        canvas = self.canv

        # 1. 绘制卡片阴影层
        shadow_color = colors.Color(0, 0, 0, alpha=0.06)
        canvas.setFillColor(shadow_color)
        canvas.roundRect(1.5*mm, -1.5*mm, self.width, self.height, 8*mm, fill=1, stroke=0)

        # 2. 绘制白色卡片背景
        canvas.setFillColor(colors.white)
        canvas.roundRect(0, 0, self.width, self.height, 8*mm, fill=1, stroke=0)

        # 3. 绘制顶部渐变色装饰条
        gradient_height = 18*mm
        steps = 30

        for i in range(steps):
            ratio = i / steps
            r = self.gradient_start.red + (self.gradient_end.red - self.gradient_start.red) * ratio
            g = self.gradient_start.green + (self.gradient_end.green - self.gradient_start.green) * ratio
            b = self.gradient_start.blue + (self.gradient_end.blue - self.gradient_start.blue) * ratio

            canvas.setFillColor(colors.Color(r, g, b))
            y_pos = self.height - gradient_height + (gradient_height / steps * i)

            if i == 0:
                # 第一层保持圆角
                canvas.roundRect(0, y_pos, self.width, gradient_height / steps + 0.2*mm, 8*mm, fill=1, stroke=0)
            else:
                canvas.rect(0, y_pos, self.width, gradient_height / steps + 0.2*mm, fill=1, stroke=0)

        # 4. 绘制标题（白色，居中）
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 11)
        title_y = self.height - gradient_height/2 - 2*mm
        canvas.drawCentredString(self.width/2, title_y, self.title.upper())

        # 5. 绘制大数字
        canvas.setFillColor(colors.HexColor("#1A237E"))
        canvas.setFont("Helvetica-Bold", 44)
        value_str = str(self.value)
        value_y = self.height/2 - 10*mm
        canvas.drawCentredString(self.width/2, value_y, value_str)

        # 6. 绘制趋势信息
        if self.subtitle:
            # 确定趋势颜色
            if self.trend == "up":
                trend_color = colors.HexColor("#4CAF50")
                trend_symbol = "▲"
            elif self.trend == "down":
                trend_color = colors.HexColor("#F44336")
                trend_symbol = "▼"
            else:
                trend_color = colors.HexColor("#9E9E9E")
                trend_symbol = "●"

            # 绘制趋势符号
            canvas.setFillColor(trend_color)
            canvas.setFont("Helvetica-Bold", 12)
            symbol_width = canvas.stringWidth(trend_symbol, "Helvetica-Bold", 12)
            symbol_x = self.width/2 - (canvas.stringWidth(self.subtitle, "Helvetica", 9) + symbol_width + 2*mm) / 2
            canvas.drawString(symbol_x, 15*mm, trend_symbol)

            # 绘制副标题文字
            canvas.setFillColor(colors.HexColor("#5D6D7E"))
            canvas.setFont("Helvetica", 9)
            canvas.drawString(symbol_x + symbol_width + 2*mm, 15*mm, self.subtitle)


class CoverPage(Flowable):
    """PDF封面页"""

    def __init__(self, title, subtitle, date, width=21*cm, height=29.7*cm):
        Flowable.__init__(self)
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.width = width
        self.height = height

    def draw(self):
        """绘制封面"""
        canvas = self.canv

        # 1. 背景渐变色（深蓝到浅蓝）
        for i in range(100):
            ratio = i / 100
            r = 15/255 + (26/255 - 15/255) * ratio
            g = 20/255 + (31/255 - 20/255) * ratio
            b = 25/255 + (46/255 - 25/255) * ratio
            canvas.setFillColor(colors.Color(r, g, b))
            canvas.rect(0, self.height - (self.height/100 * (i+1)),
                       self.width, self.height/100 + 1, fill=1, stroke=0)

        # 2. 装饰性几何图形
        canvas.setFillColor(colors.Color(0, 1, 0.533, alpha=0.1))
        canvas.circle(self.width * 0.85, self.height * 0.85, 150, fill=1, stroke=0)

        canvas.setFillColor(colors.Color(0.306, 0.792, 0.89, alpha=0.08))
        canvas.circle(self.width * 0.15, self.height * 0.2, 200, fill=1, stroke=0)

        # 3. Logo区域
        logo_y = self.height - 8*cm
        canvas.setFillColor(colors.Color(0, 1, 0.533, alpha=0.15))
        canvas.roundRect(self.width/2 - 4*cm, logo_y - 0.5*cm,
                        8*cm, 1.2*cm, 0.6*cm, fill=1, stroke=0)

        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 32)
        canvas.drawCentredString(self.width/2, logo_y, "⚡")

        # 4. 主标题
        title_y = self.height/2 + 3*cm
        canvas.setFont("Helvetica-Bold", 56)
        canvas.setFillColor(colors.white)
        canvas.drawCentredString(self.width/2, title_y, self.title)

        # 装饰线
        canvas.setStrokeColor(colors.HexColor("#00ff88"))
        canvas.setLineWidth(4)
        canvas.line(self.width/2 - 4*cm, title_y - 1*cm,
                   self.width/2 + 4*cm, title_y - 1*cm)

        # 5. 副标题
        subtitle_y = title_y - 2.5*cm
        canvas.setFont("Helvetica", 20)
        canvas.setFillColor(colors.HexColor("#8899a6"))
        canvas.drawCentredString(self.width/2, subtitle_y, self.subtitle)

        # 6. 日期
        date_y = self.height/2 - 5*cm
        canvas.setFont("Helvetica-Bold", 28)
        canvas.setFillColor(colors.HexColor("#00ff88"))
        canvas.drawCentredString(self.width/2, date_y, self.date)

        # 7. 底部信息
        footer_y = 3*cm
        canvas.setFont("Helvetica", 11)
        canvas.setFillColor(colors.HexColor("#8899a6"))
        canvas.drawCentredString(self.width/2, footer_y, "Virtual Power Plant Monitoring System")

        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(self.width/2, footer_y - 0.6*cm,
                               f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


class VPPReportGenerator:
    """VPP运行报告PDF生成器 - 现代设计"""

    def __init__(self):
        """初始化PDF生成器"""
        # 注册中文字体（macOS系统字体）
        try:
            # 尝试多个可能的中文字体路径
            font_paths = [
                '/System/Library/Fonts/PingFang.ttc',
                '/System/Library/Fonts/STHeiti Light.ttc',
                '/System/Library/Fonts/Hiragino Sans GB.ttc',
            ]

            font_registered = False
            for font_path in font_paths:
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    self.chinese_font = 'ChineseFont'
                    font_registered = True
                    break
                except:
                    continue

            if not font_registered:
                self.chinese_font = 'Helvetica'
        except:
            self.chinese_font = 'Helvetica'

    def _draw_cover_page(self, canvas, doc, stats):
        """绘制封面页 - 白色背景专业版"""
        page_width, page_height = A4

        # 1. 白色背景渐变
        for i in range(100):
            ratio = i / 100
            r = 248/255 + (233/255 - 248/255) * ratio
            g = 249/255 + (236/255 - 249/255) * ratio
            b = 250/255 + (239/255 - 250/255) * ratio
            canvas.setFillColor(colors.Color(r, g, b))
            canvas.rect(0, page_height - (page_height/100 * (i+1)),
                       page_width, page_height/100 + 1, fill=1, stroke=0)

        # 2. 装饰性几何图形 - 蓝紫色系
        canvas.setFillColor(colors.Color(99/255, 102/255, 241/255, alpha=0.08))
        canvas.circle(page_width * 0.85, page_height * 0.85, 150, fill=1, stroke=0)

        canvas.setFillColor(colors.Color(139/255, 92/255, 246/255, alpha=0.08))
        canvas.circle(page_width * 0.15, page_height * 0.2, 200, fill=1, stroke=0)

        # 3. Logo区域 - 渐变背景
        logo_y = page_height - 8*cm

        # 绘制渐变logo背景（用多个矩形模拟渐变）
        for i in range(20):
            ratio = i / 20
            r = 99/255 + (139/255 - 99/255) * ratio
            g = 102/255 + (92/255 - 102/255) * ratio
            b = 241/255 + (246/255 - 241/255) * ratio
            canvas.setFillColor(colors.Color(r, g, b))
            canvas.roundRect(page_width/2 - 4*cm + (8*cm/20 * i), logo_y - 0.5*cm,
                            8*cm/20 + 0.5*mm, 1.2*cm, 0.6*cm, fill=1, stroke=0)

        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 32)
        canvas.drawCentredString(page_width/2, logo_y, "⚡")

        # 4. 主标题 - 深色文字
        title_y = page_height/2 + 3*cm
        canvas.setFont("Helvetica-Bold", 56)
        canvas.setFillColor(colors.HexColor("#1e293b"))
        canvas.drawCentredString(page_width/2, title_y, "VPP Operation Report")

        # 装饰线 - 蓝紫渐变（用多条线模拟）
        for i in range(10):
            ratio = i / 10
            r = 99/255 + (139/255 - 99/255) * ratio
            g = 102/255 + (92/255 - 102/255) * ratio
            b = 241/255 + (246/255 - 241/255) * ratio
            canvas.setStrokeColor(colors.Color(r, g, b))
            canvas.setLineWidth(0.4)
            x_start = page_width/2 - 4*cm + (8*cm/10 * i)
            canvas.line(x_start, title_y - 1*cm, x_start + 8*cm/10, title_y - 1*cm)

        # 5. 副标题
        subtitle_y = title_y - 2.5*cm
        canvas.setFont("Helvetica", 20)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawCentredString(page_width/2, subtitle_y, "Virtual Power Plant Monitoring System")

        # 6. 日期 - 蓝紫色高亮
        date_y = page_height/2 - 5*cm
        canvas.setFont("Helvetica-Bold", 28)
        canvas.setFillColor(colors.HexColor("#6366f1"))
        canvas.drawCentredString(page_width/2, date_y, stats.get('date', 'N/A'))

        # 7. 底部信息
        footer_y = 3*cm
        canvas.setFont("Helvetica", 11)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawCentredString(page_width/2, footer_y, "Virtual Power Plant Monitoring System")

        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(page_width/2, footer_y - 0.6*cm,
                               f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def generate_report(self, stats: Dict) -> bytes:
        """
        生成PDF报告 - 现代设计风格

        Args:
            stats: 统计数据字典

        Returns:
            bytes: PDF文件的二进制数据
        """
        # 创建封面PDF
        cover_buffer = io.BytesIO()
        canvas = pdf_canvas.Canvas(cover_buffer, pagesize=A4)
        self._draw_cover_page(canvas, None, stats)
        canvas.showPage()
        canvas.save()

        # 准备内容
        story = []

        # 获取样式
        styles = getSampleStyleSheet()

        # 模块标题样式
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#1A237E'),
            spaceAfter=15,
            spaceBefore=25,
            fontName=self.chinese_font,
            borderColor=colors.HexColor('#4ECAE3'),
            borderWidth=0,
            borderPadding=5,
            leftIndent=0
        )

        # 今日数据
        today_data = stats.get('today', {})
        yesterday_data = stats.get('yesterday', {})

        # ========== 模块1: 用户数据 ==========
        section_title = Paragraph("<b>用户数据概览</b>", section_style)
        story.append(section_title)

        # 计算对比数据
        total_change = today_data.get('total_users', 0) - yesterday_data.get('total_users', 0)
        new_users = today_data.get('new_users', 0)
        exit_users = today_data.get('exit_users', 0)

        # 判断趋势
        total_trend = "up" if total_change > 0 else ("down" if total_change < 0 else "neutral")
        total_change_text = f"{'+' if total_change >= 0 else ''}{total_change} from yesterday"

        # 创建用户数据大数字卡片（3列布局）- 现代渐变风格
        user_cards_data = [
            [
                ModernMetricCard(
                    title="Total Users",
                    value=f"{today_data.get('total_users', 0):,}",
                    subtitle=total_change_text,
                    gradient_start="#667eea",
                    gradient_end="#764ba2",
                    trend=total_trend
                ),
                ModernMetricCard(
                    title="New Users",
                    value=f"+{new_users}",
                    subtitle=f"{new_users} joined",
                    gradient_start="#06beb6",
                    gradient_end="#48b1bf",
                    trend="up"
                ),
                ModernMetricCard(
                    title="Exit Users",
                    value=f"{exit_users}",
                    subtitle=f"{exit_users} left",
                    gradient_start="#fc4a1a",
                    gradient_end="#f7b733",
                    trend="down"
                )
            ]
        ]

        user_cards_table = Table(user_cards_data, colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
        user_cards_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2*mm),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2*mm),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))

        story.append(user_cards_table)
        story.append(Spacer(1, 2*cm))

        # ========== TODO: 其他模块待添加 ==========

        # 生成时间
        gen_time_style = ParagraphStyle(
            'GenTime',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#95A5A6'),
            alignment=TA_CENTER,
            fontName=self.chinese_font
        )
        gen_time = f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        story.append(Paragraph(gen_time, gen_time_style))

        # 构建内容页PDF
        content_buffer = io.BytesIO()
        content_doc = SimpleDocTemplate(
            content_buffer,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        content_doc.build(story)

        # 合并封面和内容
        from PyPDF2 import PdfReader, PdfWriter

        # 读取封面PDF
        cover_buffer.seek(0)
        cover_reader = PdfReader(cover_buffer)

        # 读取内容PDF
        content_buffer.seek(0)
        content_reader = PdfReader(content_buffer)

        # 合并
        writer = PdfWriter()

        # 添加封面
        writer.add_page(cover_reader.pages[0])

        # 添加内容页
        for page in content_reader.pages:
            writer.add_page(page)

        # 输出最终PDF
        final_buffer = io.BytesIO()
        writer.write(final_buffer)

        # 获取PDF数据
        final_buffer.seek(0)
        pdf_data = final_buffer.getvalue()
        cover_buffer.close()
        content_buffer.close()
        final_buffer.close()

        return pdf_data

    def _calc_change(self, current, previous):
        """计算变化百分比"""
        if previous == 0:
            return "0%"
        change = current - previous
        percent = (change / previous) * 100
        arrow = "↑" if change > 0 else "↓" if change < 0 else "─"
        return f"{arrow} {abs(percent):.1f}%"


# 测试代码
if __name__ == "__main__":
    from user_stats import UserStatsCollector

    collector = UserStatsCollector()
    stats_data = collector.get_stats_for_card()

    generator = VPPReportGenerator()
    pdf_bytes = generator.generate_report(stats_data)

    # 保存到文件测试
    with open("test_report.pdf", "wb") as f:
        f.write(pdf_bytes)

    print("✓ PDF报告生成成功: test_report.pdf")
