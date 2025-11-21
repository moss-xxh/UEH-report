#!/usr/bin/env python3
"""
使用Playwright直接从HTML页面生成PDF
完美保留所有样式,1:1还原
"""
import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime


async def generate_pdf_from_html():
    """从HTML页面生成PDF"""

    print("=" * 60)
    print("🚀 开始生成PDF报告...")
    print("=" * 60)

    async with async_playwright() as p:
        # 启动浏览器
        print("🌐 正在启动浏览器...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 获取HTML文件路径
        date_str = datetime.now().strftime('%Y年%m月%d日')
        html_file = f"VPP运维报告_打印版_{date_str}.html"
        html_path = os.path.abspath(html_file)

        # 直接加载本地HTML文件
        print(f"📊 正在加载本地HTML文件...")
        print(f"文件路径: {html_path}")
        await page.goto(f'file://{html_path}', wait_until='networkidle')

        # 简单等待确保渲染完成
        print("⏳ 等待渲染完成...")
        await page.wait_for_timeout(1000)

        # 输出文件名
        output_filename = f"VPP运维报告_{date_str}.pdf"

        # 生成PDF
        print("📝 正在生成PDF文件...")
        await page.pdf(
            path=output_filename,
            format='A4',
            print_background=True,  # 保留背景颜色
            margin={
                'top': '15mm',
                'right': '15mm',
                'bottom': '15mm',
                'left': '15mm'
            }
        )

        # 关闭浏览器
        await browser.close()

        # 获取文件信息
        abs_path = os.path.abspath(output_filename)
        file_size = os.path.getsize(output_filename) / 1024

        print("=" * 60)
        print("✅ PDF报告生成成功!")
        print("=" * 60)
        print(f"文件名: {output_filename}")
        print(f"完整路径: {abs_path}")
        print(f"文件大小: {file_size:.1f} KB")
        print("=" * 60)
        print("📂 PDF已完美保留所有HTML样式和数据!")
        print("   可以直接双击打开查看")
        print("=" * 60)

        return abs_path


def main():
    """主函数"""
    asyncio.run(generate_pdf_from_html())


if __name__ == "__main__":
    main()
