FROM python:3
WORKDIR /book_bot
COPY main.py /book_bot/main.py
ENTRYPOINT [ "python", "main.py" ]