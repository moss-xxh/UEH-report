#!/bin/bash

# 企业微信机器人安装脚本

echo "================================"
echo "企业微信机器人 - 安装向导"
echo "================================"
echo ""

# 检查Python版本
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python3"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python版本: $python_version"
echo ""

# 安装依赖
echo "安装依赖包..."
pip3 install -r requirements.txt
echo ""

# 提示配置
echo "================================"
echo "安装完成！"
echo "================================"
echo ""
echo "下一步："
echo "1. 编辑 config.py，配置企业微信Webhook地址"
echo "2. 根据项目需求修改 data_collector.py"
echo "3. 运行测试：python3 main.py --test"
echo "4. 正式启动：python3 main.py"
echo ""
echo "详细文档请查看 README.md"
