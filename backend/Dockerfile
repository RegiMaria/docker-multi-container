# Stage 1: Build stage
FROM python:3.12-slim as build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

# Stage 2: Production stage
FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home appuser
USER appuser

COPY --from=build /root/.local /home/appuser/.local
COPY --chown=appuser:appuser --from=build /app ./

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]