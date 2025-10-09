FROM python:3.14-bookworm

WORKDIR /docs
COPY . /docs/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8181"]
