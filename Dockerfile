FROM python:3.8-slim

WORKDIR /app


RUN apt-get update && apt-get install -y gcc libpq-dev 

RUN pip install uv

COPY . .

RUN uv pip install --system -e .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
