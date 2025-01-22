## Docker

### Keep a Docker container running for ever

```dockerfile
FROM ubuntu:latest

ENTRYPOINT ["tail", "-f", "/dev/null"]
```
