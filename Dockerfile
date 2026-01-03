FROM python:3.11-slim

WORKDIR /app

# Copy server files
COPY server.py .
COPY index.html .
COPY qa.html .

# Create documents directory (will be mounted from host)
RUN mkdir -p /documents

EXPOSE 8000

CMD ["python", "-u", "server.py"]
