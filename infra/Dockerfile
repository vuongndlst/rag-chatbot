FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir 'hatchling' && pip install --no-cache-dir .[test]
COPY backend ./backend
CMD ["python", "-m", "backend.app.main"]
