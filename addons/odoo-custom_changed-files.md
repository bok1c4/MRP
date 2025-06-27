```Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies (with best practices)
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  git \
  build-essential \
  wget \
  node-less \
  libpq-dev \
  libxml2-dev \
  libxslt1-dev \
  libldap2-dev \
  libsasl2-dev \
  libjpeg-dev \
  zlib1g-dev \
  libffi-dev && \
  rm -rf /var/lib/apt/lists/*

# Copy Odoo source code
COPY . /mnt/odoo
WORKDIR /mnt/odoo

# Install Python dependencies
RUN pip install --no-cache-dir wheel && \
  pip install --no-cache-dir -r requirements.txt

# Run Odoo
CMD ["python3", "odoo-bin", "-c", "/etc/odoo/odoo.conf"]


```
