FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV TOKEN='token from @BotFather'
ENTRYPOINT ["python", "model.py", "bot.py"]