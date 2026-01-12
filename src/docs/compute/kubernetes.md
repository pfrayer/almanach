# Kubernetes

## Get objects

Filter pods per label:
```shell
$ kubectl get pods -l "mycompanny.region=EU"
```

Get pod current metrics:
```shell
$ kubectl describe PodMetrics <pod_name>
```

List available API resources (which depends on the k8s server version):
```shell
$ kubectl api-resources -o wide
NAME                               SHORTNAMES                                          APIVERSION                             NAMESPACED   KIND                              VERBS
bindings                                                                               v1                                     true         Binding                           [create]
componentstatuses                  cs                                                  v1                                     false        ComponentStatus                   [get list]
configmaps                         cm                                                  v1                                     true         ConfigMap                         [create delete deletecollection get list patch update watch]
endpoints                          ep                                                  v1                                     true         Endpoints                         [create delete deletecollection get list patch update watch]
events                             ev                                                  v1                                     true         Event                             [create delete deletecollection get list patch update watch]
limitranges                        limits                                              v1                                     true         LimitRange                        [create delete deletecollection get list patch update watch]
namespaces                         ns                                                  v1                                     false        Namespace                         [create delete get list patch update watch]
nodes                              no                                                  v1                                     false        Node                              [create delete deletecollection get list patch update watch]
...
```

## Logs

Get deployment logs:
```shell
$ kubectl logs deployment/<name-of-deployment>
```

## Failure analysis

List non-running pods, display their events:
```shell
$ for pod in $(kubectl get pods --field-selector status.phase!=Running | grep -v "^NAME" | awk '{print $1}' | sort -u)
do
    echo "POD: {$pod}"
    kubectl get event --field-selector involvedObject.name=${pod}
    echo "----"
done
```

## Helm

### Render a Chart template localy

```shell
$ ls
Chart.yaml  README.md  templates  values.yaml

$ helm template . --debug
---
# Source: l2c-router/templates/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: l2c-router-release-name
  labels:
    ...
```
