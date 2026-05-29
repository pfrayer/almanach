# Helm

## Install Helm

Via the official install script:
```shell
$ curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Via package managers:
```shell
# macOS
$ brew install helm

# Debian / Ubuntu
$ curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
$ sudo apt-get update && sudo apt-get install helm
```

Verify installation:
```shell
$ helm version
```

## Repositories

Add a chart repository:
```shell
$ helm repo add bitnami https://charts.bitnami.com/bitnami
```

List configured repos:
```shell
$ helm repo list
```

Update repo index (fetch latest charts):
```shell
$ helm repo update
```

Remove a repo:
```shell
$ helm repo remove bitnami
```

## Search charts

Search in configured repos:
```shell
$ helm search repo nginx
```

Show all available versions of a chart:
```shell
$ helm search repo nginx --versions
```

Search on Artifact Hub:
```shell
$ helm search hub wordpress
```

## Inspect a chart

Show chart metadata:
```shell
$ helm show chart bitnami/nginx
```

Show default values (useful before installing):
```shell
$ helm show values bitnami/nginx
```

Show the full README:
```shell
$ helm show readme bitnami/nginx
```

## Install a chart

Basic install (generates a release name):
```shell
$ helm install my-release bitnami/nginx
```

Install in a specific namespace (create it if needed):
```shell
$ helm install my-release bitnami/nginx -n my-namespace --create-namespace
```

Override values inline:
```shell
$ helm install my-release bitnami/nginx --set service.type=ClusterIP --set replicaCount=2
```

Override values from a file:
```shell
$ helm install my-release bitnami/nginx -f custom-values.yaml
```

Install a specific chart version:
```shell
$ helm install my-release bitnami/nginx --version 15.0.0
```

Dry-run (render templates without installing):
```shell
$ helm install my-release bitnami/nginx --dry-run
```

## List releases

```shell
$ helm list
$ helm list -n my-namespace
$ helm list --all-namespaces
```

## Upgrade a release

Upgrade with new values:
```shell
$ helm upgrade my-release bitnami/nginx --set replicaCount=3
```

Upgrade from a values file:
```shell
$ helm upgrade my-release bitnami/nginx -f updated-values.yaml
```

Install if not present, upgrade if it is:
```shell
$ helm upgrade --install my-release bitnami/nginx -f values.yaml
```

## Rollback

View release history:
```shell
$ helm history my-release
```

Rollback to previous revision:
```shell
$ helm rollback my-release
```

Rollback to a specific revision:
```shell
$ helm rollback my-release 2
```

## Uninstall a release

```shell
$ helm uninstall my-release
$ helm uninstall my-release -n my-namespace
```

## Get release info

Show computed values for a release:
```shell
$ helm get values my-release
```

Show rendered manifests:
```shell
$ helm get manifest my-release
```

Show release status:
```shell
$ helm status my-release
```

## Template (local rendering)

Render templates locally without connecting to a cluster:
```shell
$ helm template my-release bitnami/nginx -f values.yaml
```
