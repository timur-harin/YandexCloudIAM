FROM python:3.11-slim

COPY backend/requirements.txt .

RUN pip install --user -r requirements.txt

COPY ./ ./app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1); s.connect(('localhost', 5000))" || exit 1

WORKDIR app/

CMD [ "python", "-u", "backend/app.py"]