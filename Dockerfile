FROM tiangolo/uvicorn-gunicorn:python3.10-slim
ENV APP_HOME /app
WORKDIR $APP_HOME
ADD requirements.txt /app/requirements.txt
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install curl -y
COPY api.env.prod .env
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]