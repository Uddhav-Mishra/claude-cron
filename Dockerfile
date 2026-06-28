# Claude Code is a Node package; this image adds Python to run the wrapper script.
FROM node:20-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @anthropic-ai/claude-code

WORKDIR /app
COPY send_hi.py .

CMD ["python3", "send_hi.py"]
