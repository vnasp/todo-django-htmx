FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Install Node.js so we can build Tailwind CSS during image build
RUN apt-get update \
  && apt-get install -y curl ca-certificates gnupg \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install npm dependencies and build CSS
RUN npm ci --omit=optional --no-audit --no-fund || npm install --no-audit --no-fund
RUN npm run build:css

RUN python manage.py collectstatic --no-input
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
