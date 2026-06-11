---
description: "Kubernetes kubectl cheatsheet: contexts, logs, exec and debug, rollouts, failure analysis, secrets, ConfigMaps and k9s."
---

# Kubernetes

## Context & namespace

```shell
kubectl config get-contexts                    # list contexts
kubectl config current-context
kubectl config use-context <context>

kubectl config set-context --current --namespace=<ns>  # set default namespace
kubectl get namespaces
```

!!! tip "kubectx / kubens"
    [`kubectx` and `kubens`](https://github.com/ahmetb/kubectx){target=_blank} let you switch context and namespace in one command:
    ```shell
    kubectx <context>
    kubens <namespace>
    ```

---

## Get & describe

```shell
# Common shortnames: po, deploy, svc, cm, secret, ing, ns, no, pvc
kubectl get pods
kubectl get pods -n <namespace>
kubectl get pods -A                            # all namespaces
kubectl get pods -o wide                       # + node, IP
kubectl get pods -l app=myapp                  # filter by label
kubectl get pods --field-selector status.phase=Running

kubectl get all                                # pods + services + deployments + replicasets
kubectl get events --sort-by=.lastTimestamp
kubectl get events -A --sort-by=.lastTimestamp # cluster-wide events

kubectl describe pod <pod>
kubectl describe deployment <name>
kubectl describe node <node>

kubectl api-resources -o wide                  # all resource types on this cluster
```

### Output formats

```shell
kubectl get pod <pod> -o yaml                  # full YAML spec
kubectl get pod <pod> -o json
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
```

---

## Logs

```shell
kubectl logs <pod>
kubectl logs <pod> -c <container>              # multi-container pod
kubectl logs <pod> -f                          # follow
kubectl logs <pod> --tail=100
kubectl logs <pod> --previous                  # crashed previous container

kubectl logs deployment/<name>
kubectl logs -l app=myapp --all-containers=true
```

---

## Exec & debug

```shell
# Shell into a running pod
kubectl exec -it <pod> -- bash
kubectl exec -it <pod> -c <container> -- sh

# Run a one-off debug pod
kubectl run debug --rm -it --image=alpine -- sh
kubectl run debug --rm -it --image=nicolaka/netshoot -- bash

# Port-forward to local machine
kubectl port-forward pod/<pod> 8080:80
kubectl port-forward svc/<service> 8080:80
kubectl port-forward deployment/<name> 8080:80

# Copy files
kubectl cp <pod>:/path/to/file ./local
kubectl cp ./local <pod>:/path/to/file
```

---

## Apply & manage

```shell
kubectl apply -f manifest.yaml
kubectl apply -f ./dir/                        # apply all files in directory
kubectl delete -f manifest.yaml

kubectl scale deployment <name> --replicas=3
kubectl set image deployment/<name> <container>=<image>:<tag>

# Rollout
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>
kubectl rollout restart deployment/<name>      # rolling restart (e.g. to reload ConfigMap)

kubectl patch deployment <name> -p '{"spec":{"replicas":2}}'
```

---

## Failure analysis

```shell
# Non-running pods + their events
for pod in $(kubectl get pods --field-selector status.phase!=Running \
    | grep -v "^NAME" | awk '{print $1}'); do
    echo "=== POD: ${pod} ==="
    kubectl describe pod "${pod}" | tail -20
    kubectl get events --field-selector involvedObject.name="${pod}"
done

# Pod stuck in Pending — check resource pressure
kubectl describe pod <pod> | grep -A5 Events

# CrashLoopBackOff — check last logs
kubectl logs <pod> --previous

# OOMKilled — check limits
kubectl get pod <pod> -o jsonpath='{.spec.containers[*].resources}'

# Node pressure
kubectl describe node <node> | grep -A10 Conditions
kubectl top nodes
kubectl top pods -A
```

---

## Secrets & ConfigMaps

```shell
# Read a secret (base64 decoded)
kubectl get secret <name> -o jsonpath='{.data.<key>}' | base64 -d

# Create a secret from literals
kubectl create secret generic <name> --from-literal=key=value

# Create from file
kubectl create secret generic <name> --from-file=config.yaml

# Create a ConfigMap
kubectl create configmap <name> --from-literal=ENV=prod
kubectl create configmap <name> --from-file=app.conf
```

---

## k9s

[k9s](https://k9scli.io){target=_blank} is a terminal UI for Kubernetes — the fastest way to browse and debug a cluster.

```shell
k9s                           # open on current context/namespace
k9s -n <namespace>
k9s --context <context>
```

### Key bindings

| Key | Action |
|-----|--------|
| `:pod` | Go to pods view (works with any resource: `:deploy`, `:svc`…) |
| `:ns` | Switch namespace |
| `0` | Show all namespaces |
| `/` | Filter by name |
| `l` | Logs |
| `s` | Shell into container |
| `d` | Describe |
| `e` | Edit YAML |
| `ctrl-d` | Delete resource |
| `ctrl-k` | Kill pod |
| `y` | View YAML |
| `?` | Help / all shortcuts |
| `esc` | Back |
| `q` | Quit |

---

## Helm

```shell
helm repo add <name> <url>
helm repo update
helm search repo <keyword>

helm install <release> <chart>
helm install <release> <chart> -f values.yaml
helm install <release> <chart> --set key=value

helm upgrade <release> <chart> -f values.yaml
helm upgrade --install <release> <chart>       # install if not exists

helm rollback <release> <revision>
helm uninstall <release>

helm list
helm list -A                                   # all namespaces
helm history <release>

# Render templates locally without deploying
helm template <release> . -f values.yaml

# Diff before applying (requires helm-diff plugin)
helm diff upgrade <release> <chart> -f values.yaml
```
