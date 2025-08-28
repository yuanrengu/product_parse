# 支持 API/CLI 双模式
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 允许通过 CMD 覆盖运行模式
ENTRYPOINT ["python"]

# 默认运行 API
CMD ["-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
