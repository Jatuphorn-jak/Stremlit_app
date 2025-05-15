FROM python:3.12.10

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install numpy==2.2.5 && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0
