# syntax=docker/dockerfile:1@sha256:87999aa3d42bdc6bea60565083ee17e86d1f3339802f543c0d03998580f9cb89
FROM python:3.12.4-slim-bookworm@sha256:a3e58f9399353be051735f09be0316bfdeab571a5c6a24fd78b92df85bcb2d85

LABEL org.opencontainers.image.title="Berry-Esseen 0.45 verifier" \
      org.opencontainers.image.description="Rigorous construction and verification of the finite interval certificate" \
      org.opencontainers.image.authors="Kacper Rodziewicz" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="1.2.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements-container.txt ./
RUN python -c "import sys; assert sys.version_info[:3] == (3, 12, 4)"
RUN python -m pip install --require-hashes --no-deps \
    --requirement requirements-container.txt
RUN python -c "import flint; assert flint.__version__ == '0.9.0'; assert flint.__FLINT_VERSION__ == '3.6.0'"

RUN groupadd --gid 10001 verifier \
    && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin verifier \
    && mkdir -p /app/data/parameter_bank /app/artifacts \
    && chown -R verifier:verifier /app

COPY --chown=verifier:verifier proof ./proof
COPY --chown=verifier:verifier construction ./construction
COPY --chown=verifier:verifier certificate.schema.json bundle.schema.json LICENSE ./

USER 10001:10001

ENTRYPOINT ["python", "-m", "construction.verify"]
CMD ["--workers", "6", "--parameter-bank", "/app/data/parameter_bank", "--output", "/app/artifacts/certificate"]
