FROM python:3.15-trixie@sha256:f34e3385a59fd8de7919d46db4a38ab14c0e46928a11b59036a7ee206ac0c129

WORKDIR /docs
COPY . /docs/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8181"]
