# 使用官方的 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置 PYTHONPATH 环境变量
ENV PYTHONPATH=/app