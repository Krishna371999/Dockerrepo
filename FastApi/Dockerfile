FROM python:3.11
LABEL app="BOTO3 with FastAPI"
LABEL maintainer="Vamsi Chilukuri"
LABEL email="chilukurivamsi2@gmail.com"
ENV AWS_ACCESS_KEY_ID=SAMPLEKEYID
ENV AWS_SECRET_ACCESS_KEY=SAMEPLSECRETKEY
ARG T_VERSION=1.8.2
WORKDIR /code
ADD .env .env
COPY requirements.txt requirements.txt
ADD https://releases.hashicorp.com/terraform/${T_VERSION}/terraform_${T_VERSION}_linux_amd64.zip terraform.zip
RUN python --version && apt update && apt install -y unzip net-tools jq \
    && unzip terraform.zip && mv terraform /usr/local/bin/ && rm terraform.zip && terraform --version \
    && pip install --no-cache-dir --upgrade -r requirements.txt 
ADD main.py main.py
EXPOSE 80/tcp
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
#ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]
CMD ["--port", "80"]
