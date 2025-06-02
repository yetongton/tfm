@echo off
echo 安装城市新闻情感分析系统依赖...

:: 安装基本依赖
echo 安装基本依赖...
pip install flask flask-login werkzeug pandas

:: 安装汉字转拼音库
echo 安装汉字转拼音库...
pip install pypinyin

:: 安装PyTorch和Transformers（用于情感分析）
echo 安装PyTorch和Transformers...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers

echo 依赖安装完成！
pause 