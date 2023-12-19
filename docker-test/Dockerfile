# 使用官方的 Python 長輩為基底映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app


COPY requirements.txt .

# 安裝 Flask 應用程式所需的套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製 requirements.txt 到工作目錄


# 複製整個應用程式到工作目錄
COPY . .

# 開放 Flask 預設的 5000 埠口
EXPOSE 5000
ENV FLASK_DEBUG=True

# 定義默認的啟動命令
CMD ["flask", "run"]

