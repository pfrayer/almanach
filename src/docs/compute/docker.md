---
description: "Docker cheatsheet: images, containers, volumes, networks, registry, cleanup, Docker Compose and Dockerfile tips."
---

# Docker

## Images

```shell
docker pull <image>:<tag>
docker push <image>:<tag>
docker tag <image> <registry>/<image>:<tag>

docker images                          # list local images
docker rmi <image>                     # remove an image
docker rmi $(docker images -q)         # remove all images

docker image inspect <image>
docker history <image>                 # layer-by-layer breakdown
```

### Build

```shell
docker build -t <name>:<tag> .
docker build -t <name>:<tag> -f path/Dockerfile .
docker build --no-cache -t <name>:<tag> .
docker build --platform linux/amd64 -t <name>:<tag> .   # cross-build
```

### Build with a secret (not baked into image)

```dockerfile
# Dockerfile
RUN --mount=type=secret,id=pip.conf,dst=/etc/pip.conf pip install .
```

```shell
docker build -t my-image \
    --secret id=pip.conf,src=$HOME/.pip/pip.conf \
    .
```

---

## Containers

### Run

```shell
docker run <image>                     # foreground
docker run -d <image>                  # detached (background)
docker run -it <image> bash            # interactive shell
docker run --rm <image>                # auto-remove on exit

docker run -p 8080:80 <image>          # host:container port
docker run -v /host/path:/container/path <image>   # bind mount
docker run -v myvolume:/data <image>   # named volume

docker run --name mycontainer <image>
docker run -e VAR=value <image>
docker run --env-file .env <image>
docker run --network mynet <image>
```

### Lifecycle

```shell
docker ps                              # running containers
docker ps -a                           # all containers (including stopped)

docker stop <container>
docker start <container>
docker restart <container>
docker kill <container>                # SIGKILL immediately
docker rm <container>
docker rm -f <container>               # force remove (even if running)
docker rm $(docker ps -aq)             # remove all stopped containers
```

### Inspect & debug

```shell
docker logs <container>
docker logs -f <container>             # follow
docker logs --tail 100 <container>

docker exec -it <container> bash       # shell into running container
docker exec <container> <cmd>          # run a single command

docker inspect <container>             # full JSON metadata
docker stats                           # live CPU/mem/net usage
docker top <container>                 # running processes inside

docker cp <container>:/path/file .     # copy file out of container
docker cp ./file <container>:/path/    # copy file into container
```

---

## Volumes

```shell
docker volume create <name>
docker volume ls
docker volume inspect <name>
docker volume rm <name>
docker volume prune                    # remove all unused volumes
```

---

## Networks

```shell
docker network create <name>
docker network create --driver bridge <name>
docker network ls
docker network inspect <name>
docker network connect <network> <container>
docker network disconnect <network> <container>
docker network rm <name>
docker network prune
```

---

## Registry

```shell
docker login <registry>                # defaults to Docker Hub
docker login ghcr.io
docker logout <registry>
```

---

## Cleanup

```shell
docker system prune                    # stopped containers + dangling images + unused nets
docker system prune -a                 # + all unused images (not just dangling)
docker system prune --volumes          # + volumes

docker container prune
docker image prune
docker image prune -a
docker volume prune
docker network prune

docker system df                       # disk usage breakdown
```

---

## Docker Compose

```shell
docker compose up                      # start services (foreground)
docker compose up -d                   # detached
docker compose up --build              # rebuild images before starting
docker compose up --pull always        # always pull latest images

docker compose down                    # stop + remove containers & networks
docker compose down -v                 # + remove volumes

docker compose ps                      # list services
docker compose logs -f                 # follow all logs
docker compose logs -f <service>

docker compose exec <service> bash     # shell into a service
docker compose run --rm <service> <cmd>  # one-off command

docker compose build
docker compose pull
docker compose restart <service>
docker compose scale <service>=3       # (v1) / use replicas in v2
```

---

## Dockerfile tips

```dockerfile
# Keep a container running indefinitely (debug image)
FROM ubuntu:latest
ENTRYPOINT ["tail", "-f", "/dev/null"]
```

```dockerfile
# Multi-stage build — keep final image lean
FROM node:22 AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

```dockerfile
# .dockerignore — always add it
node_modules
.git
*.log
.env
```
