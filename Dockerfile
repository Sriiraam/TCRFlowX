FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /opt/tcrflowx

COPY requirements-dashboard.txt .

RUN pip install --no-cache-dir -r requirements-dashboard.txt

COPY streamlit_app/ streamlit_app/

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
