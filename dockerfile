FROM python:3.10-slim
ENV TOKEN='Your token from GodFather'
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]