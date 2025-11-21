#!/usr/bin/env python3
"""
PDF报告Web服务
提供VPP运行报告的PDF生成和预览
"""
from flask import Flask, send_file, jsonify
from pdf_generator import VPPReportGenerator
from user_stats import UserStatsCollector
import io
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def index():
    """首页"""
    return """
    <html>
    <head>
        <title>VPP报告服务</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            h1 {
                color: #4ECAE3;
                text-align: center;
                margin-bottom: 30px;
            }
            .btn {
                display: inline-block;
                padding: 14px 28px;
                margin: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-size: 16px;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
            .links {
                text-align: center;
                margin-top: 30px;
            }
            .info {
                background: linear-gradient(135deg, #e8f4f8 0%, #d4e9f2 100%);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .info p {
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 VPP运行报告服务</h1>
            <div class="info">
                <p><strong>服务状态:</strong> 运行中 ✓</p>
                <p><strong>功能:</strong> 动态生成VPP运行详细报告</p>
            </div>
            <div class="links">
                <a href="/report/html" class="btn" target="_blank">📄 查看HTML报告</a>
                <a href="/api/stats" class="btn" target="_blank">📊 统计数据 (JSON)</a>
            </div>
        </div>
    </body>
    </html>
    """


@app.route('/report/html')
def generate_html_report():
    """生成并返回HTML报告"""
    try:
        logger.info("收到HTML报告生成请求")

        # 收集数据
        collector = UserStatsCollector()
        stats_data = collector.get_stats_for_card()

        # 读取HTML模板（专业风格）
        with open('report_template_professional.html', 'r', encoding='utf-8') as f:
            html_template = f.read()

        # 替换数据（使用JavaScript动态加载会更灵活，这里为了简单直接替换）
        from datetime import datetime

        import json

        # 准备完整的数据结构
        today = stats_data.get("today", {})
        yesterday = stats_data.get("yesterday", {})

        data_object = {
            'date': stats_data.get("date", "N/A"),
            'total_users': today.get("total_users", 0),
            'new_users': today.get("new_users", 0),
            'exit_users': today.get("exit_users", 0),
            'total_change': today.get("total_users", 0) - yesterday.get("total_users", 0),
            'device_by_region': today.get("device_by_region", {}),
            'device_by_brand': today.get("device_by_brand", {}),
            'operation': {
                'dispatch_count': today.get("dispatch_count", 0),
                'device_count': sum(today.get("device_by_brand", {}).values()),
                'grid_power': today.get("grid_power", 0),
                'profit': today.get("profit", 0)
            },
            'regional_operation': stats_data.get("regional_operation", []),
            'dispatch_records': stats_data.get("dispatch_records", []),
            'exceptions': stats_data.get("exceptions", []),
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        html_content = html_template.replace(
            'const data = {',
            f'const data = {json.dumps(data_object, ensure_ascii=False)};\n            const original_data = {{'
        )

        logger.info("✓ HTML报告生成成功")

        from flask import Response
        return Response(html_content, mimetype='text/html')

    except Exception as e:
        logger.error(f"✗ 生成HTML时发生错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': '生成HTML失败',
            'message': str(e)
        }), 500


# PDF生成功能已禁用 - 用户可以通过网页浏览器的打印功能导出PDF
# @app.route('/report/pdf')
# def generate_pdf_report():
#     """生成并返回PDF报告"""
#     try:
#         logger.info("收到PDF报告生成请求")
#
#         # 收集数据
#         collector = UserStatsCollector()
#         stats_data = collector.get_stats_for_card()
#
#         # 生成PDF
#         generator = VPPReportGenerator()
#         pdf_bytes = generator.generate_report(stats_data)
#
#         logger.info("✓ PDF报告生成成功")
#
#         # 返回PDF文件
#         return send_file(
#             io.BytesIO(pdf_bytes),
#             mimetype='application/pdf',
#             as_attachment=False,  # 在浏览器中直接预览，不下载
#             download_name=f'VPP运行报告_{stats_data.get("date", "")}.pdf'
#         )
#
#     except Exception as e:
#         logger.error(f"✗ 生成PDF时发生错误: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({
#             'error': '生成PDF失败',
#             'message': str(e)
#         }), 500


@app.route('/api/stats')
def get_stats():
    """获取统计数据（JSON格式）"""
    try:
        collector = UserStatsCollector()
        stats_data = collector.get_stats_for_card()
        return jsonify(stats_data)
    except Exception as e:
        logger.error(f"✗ 获取统计数据失败: {e}")
        return jsonify({
            'error': '获取数据失败',
            'message': str(e)
        }), 500


@app.route('/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'service': 'VPP PDF Report Service',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    import os

    # 从环境变量获取端口（Render会设置PORT环境变量）
    port = int(os.environ.get('PORT', 8080))

    logger.info("\n" + "=" * 60)
    logger.info("🚀 VPP 报告服务启动")
    logger.info("=" * 60)
    logger.info(f"访问地址: http://localhost:{port}")
    logger.info(f"HTML报告: http://localhost:{port}/report/html")
    logger.info("=" * 60 + "\n")

    # 启动Flask服务
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # 生产环境关闭debug
    )
