## Docker

### Build an image using a secret file

In your Docker image build you need a temporary config file to install some dependencies. Set this in your `Dockerfile` to declare en temporary secret config file:

```dockerfile
FROM python:3.13

COPY pyproject.toml setup.py /app
RUN --mount=type=secret,id=pip.conf,dst=/etc/pip.conf pip install .
...
```
Then build you image like this:
```bash
$ docker build -t my-image \
    --secret id=pip.conf,src=$HOME/.pip/pip.conf \
   .
```
Ensure the secret `id` is the same in both the command & the `Dockerfile`. [Official doc is here](https://docs.docker.com/build/building/secrets/){target=_blank}.

### Keep a Docker container running for ever

```dockerfile
FROM ubuntu:latest

ENTRYPOINT ["tail", "-f", "/dev/null"]
```
