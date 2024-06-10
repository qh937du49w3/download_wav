FROM --platform=linux/amd64 python:3

RUN mkdir /app
WORKDIR /app
COPY web.py .
COPY requirements.txt .
RUN pip  install -r requirements.txt

RUN apt-get update && apt-get install -y \
    libasound2 \
    libasound2-dev \
    libpulse0 \
    libpulse-dev \
    libffi-dev

RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb
RUN dpkg -i libssl1.1_1.1.0g-2ubuntu4_amd64.deb

ENTRYPOINT [ "python","web.py" ]