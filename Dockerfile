FROM python:latest
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "pytest", "--app_env", "dev", "-m", "ecommerce_services", "--html=EcommConnectorAPISuite.html"]
