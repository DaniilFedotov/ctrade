FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
COPY  --chmod=0755 entrypoint.sh .

RUN chmod u+x entrypoint.sh
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .