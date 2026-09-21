FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

# Güvenlik açıklarını kapatmak için önce temel Python paketleyicilerini (pip, setuptools, wheel) güncelliyoruz.
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Alpine sisteminde C++ kodlarını derlemek için gcc gibi araçları kurup, 
# kurulum bitince hemen geri siliyoruz ki paketimiz küçük ve güvenli kalsın.
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Son temizlik: Bazı kütüphaneler (fastapi vs.) kurulurken kendi içlerinde eski 'msgpack' ve 'setuptools' getirmiş.
# Bunları zorla en son sürüme güncelleyerek son güvenlik açıklarını da kapatıyoruz!
RUN pip install --no-cache-dir --upgrade msgpack setuptools

COPY . .

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
