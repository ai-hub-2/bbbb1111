# Production Dockerfile - ملف Docker للإنتاج
# Multi-stage build for production - بناء متعدد المراحل للإنتاج

# Stage 1: Build - المرحلة الأولى: البناء
FROM python:3.11-slim as builder

# Set working directory - تعيين مجلد العمل
WORKDIR /app

# Install system dependencies - تثبيت تبعيات النظام
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements - نسخ المتطلبات
COPY requirements_production.txt .

# Install Python dependencies - تثبيت تبعيات Python
RUN pip install --no-cache-dir --user -r requirements_production.txt

# Stage 2: Production - المرحلة الثانية: الإنتاج
FROM python:3.11-slim

# Set environment variables - تعيين متغيرات البيئة
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user - إنشاء مستخدم غير root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory - تعيين مجلد العمل
WORKDIR /app

# Install runtime dependencies - تثبيت تبعيات التشغيل
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder - نسخ حزم Python من المرحلة الأولى
COPY --from=builder /root/.local /root/.local

# Copy application code - نسخ كود التطبيق
COPY production_ready_app.py .
COPY .env.example .env

# Set permissions - تعيين الصلاحيات
RUN chown -R appuser:appuser /app
USER appuser

# Expose port - فتح المنفذ
EXPOSE 8000

# Health check - فحص الصحة
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application - تشغيل التطبيق
CMD ["python", "production_ready_app.py"]