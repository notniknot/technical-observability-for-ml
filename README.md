# technical-observability-for-ml
This is an example how observability can be achieved in a technical sense with ML-Models

# Prerequisites
## Creating a K8s-Namespace
```
kubectl create ns technical-observability-for-ml
```
## Installing Tool-Chain via Helm

### Grafana
Installation
```
# see https://artifacthub.io/packages/helm/grafana/grafana/6.50.8
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade -f helm-config/grafana/values.yaml --install -n technical-observability-for-ml grafana grafana/grafana --version 6.50.8
```

Get your 'admin' user password by running:
```
kubectl get secret --namespace technical-observability-for-ml grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

### MinIO
Installation
```
# see https://artifacthub.io/packages/helm/bitnami/minio/12.1.8
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade -f helm-config/minio/values.yaml --install -n technical-observability-for-ml minio bitnami/minio --version 12.1.8
```

Get credentials:
```
kubectl get secret --namespace technical-observability-for-ml minio -o jsonpath="{.data.root-user}" | base64 -d
kubectl get secret --namespace technical-observability-for-ml minio -o jsonpath="{.data.root-password}" | base64 -d
```

Login into MinIO by navigating to "http://localhost:30001" and create a new bucket called "loki"

### Loki
```
# see https://artifacthub.io/packages/helm/grafana/loki-simple-scalable/1.8.11
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade -f helm-config/loki/values.yaml --install -n technical-observability-for-ml loki grafana/loki-simple-scalable
```

### Promtail
```
# see https://artifacthub.io/packages/helm/grafana/promtail/6.9.0
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade -f helm-config/promtail/values.yaml --install -n technical-observability-for-ml promtail grafana/promtail --version 6.9.0
```

### Tempo
```
# see https://artifacthub.io/packages/helm/grafana/tempo/1.0.0
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade -f helm-config/tempo/values.yaml --install -n technical-observability-for-ml tempo grafana/tempo --version 1.0.0
```

### Prometheus
```
# see https://artifacthub.io/packages/helm/prometheus-community/prometheus/19.6.1
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade -f helm-config/prometheus/values.yaml --install -n technical-observability-for-ml prometheus prometheus-community/prometheus --version 19.6.1
```
