FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python", "src/bot.py"]
