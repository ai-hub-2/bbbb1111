# Dockerfile للتطبيق السحابي
# Cloud Blue Badge Application Dockerfile

FROM python:3.11-slim

# تعيين متغيرات البيئة
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# تحديث النظام وتثبيت المكتبات المطلوبة
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements_cloud.txt .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements_cloud.txt

# نسخ ملفات التطبيق
COPY . .

# إنشاء مستخدم غير root
RUN useradd -m -u 1000 streamlit && \
    chown -R streamlit:streamlit /app
USER streamlit

# فتح المنفذ
EXPOSE 8501

# تشغيل التطبيق
CMD ["streamlit", "run", "cloud_app.py", "--server.port=8501", "--server.address=0.0.0.0"]