FROM python:3.9
WORKDIR /secret_santa

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .