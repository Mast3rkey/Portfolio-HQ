# Provider-neutral container for the Portfolio-HQ private owner interface.
#
# Deliberately dependency-free: the hosted half of the owner interface
# (service / render / chart_inbox / auth / export_io) uses only the Python
# standard library, so this image installs nothing from requirements.txt. That
# keeps the runtime small enough for any modest private host and keeps pandas,
# the market-data clients and the brokerage client entirely out of the deployed
# image — they are build-time-only concerns of `portfolio_hq.owner.export`.
#
# No secret is baked in. PORTFOLIO_HQ_OWNER_TOKEN must be supplied at run time
# as a platform secret; without it the service refuses to start.
#
# TLS is terminated by the host in front of this container. The session cookie
# is marked Secure on any non-loopback bind and will not be sent over plain HTTP.

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8080 \
    PORTFOLIO_HQ_OWNER_EXPORT=/data/export.json \
    PORTFOLIO_HQ_OWNER_INBOX=/data/inbox

WORKDIR /app

# Only the presentation package is copied in. No repository state file
# (holdings.yaml, targets.yaml, gates.yaml, governance/, intelligence/) is
# present in the image: the running service never reads them. This image
# therefore supports `serve` only -- `export` is a build-time command that
# needs the repository and its dependencies, and is run outside the container.
COPY portfolio_hq/__init__.py /app/portfolio_hq/__init__.py
COPY portfolio_hq/owner /app/portfolio_hq/owner

# Persistent volume: the chart inbox lives here. An ephemeral filesystem would
# discard received charts on restart.
VOLUME ["/data"]

RUN useradd --create-home --uid 10001 owner \
    && mkdir -p /data \
    && chown -R owner:owner /data /app
USER owner

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import os,urllib.request,sys; \
url='http://127.0.0.1:%s/healthz' % os.environ.get('PORT','8080'); \
sys.exit(0 if b'ok' in urllib.request.urlopen(url, timeout=4).read() else 1)"

# Shell form so ${VAR} expansion happens at run time, not build time.
CMD python -m portfolio_hq.owner serve \
      --host "${HOST}" --port "${PORT}" \
      --export "${PORTFOLIO_HQ_OWNER_EXPORT}" \
      --inbox "${PORTFOLIO_HQ_OWNER_INBOX}"
