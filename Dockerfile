FROM tiangolo/uvicorn-gunicorn:python3.11-slim

WORKDIR /app
ADD requirements.txt /app/requirements.txt
COPY . ./
# RUN pip install --default-timeout=100 --upgrade pip setuptools
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# RUN apt-get update
# RUN apt-get install curl -y

#RUN ls -la
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]