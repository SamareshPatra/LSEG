FROM python:3.9-slim
WORKDIR /app
COPY app.py ./
COPY stock_price_data_files ./stock_price_data_files
CMD ["python3", "app.py"]