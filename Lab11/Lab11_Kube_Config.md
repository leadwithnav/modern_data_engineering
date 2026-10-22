# Lab: Understanding Kubeconfig & Switching Between Minikube and K3s

## Estimated Time
15–20 minutes

---

## 🎯 Objective
Learn how to:
- Understand kubeconfig structure
- List clusters, contexts, and users
- Switch between Minikube and K3s
- Merge multiple kubeconfig files
- Set default namespaces per context

---

## 🔍 Step 1: View Your Kubeconfig

```bash
kubectl config view
```

---

## 🧩 Step 2: List Clusters, Users & Contexts

```bash
kubectl config get-clusters
kubectl config get-users
kubectl config get-contexts
```

---

## ☸️ Step 3: Start Both Clusters

### Start Minikube
```bash
minikube start
```

### Start K3s
```bash
sudo systemctl start k3s
```

K3s kubeconfig location:
```
/etc/rancher/k3s/k3s.yaml
```

---

## 🪄 Step 4: Import & Merge K3s Kubeconfig

```bash
sudo cat /etc/rancher/k3s/k3s.yaml > ~/k3s.yaml
export KUBECONFIG=~/.kube/config:~/k3s.yaml
kubectl config view --flatten > ~/.kube/config-merged
mv ~/.kube/config-merged ~/.kube/config
```

---

## 🔄 Step 5: Switch Between Clusters

### Switch to Minikube
```bash
kubectl config use-context minikube
kubectl get nodes
```

### Switch to K3s
```bash
kubectl config use-context default
kubectl get nodes
```

---

## 🧪 Step 6: Test Deployments

### Minikube
```bash
kubectl config use-context minikube
kubectl create deployment nginx --image=nginx
kubectl get pods
```

### K3s
```bash
kubectl config use-context default
kubectl create deployment nginx --image=nginx
kubectl get pods
```

---

## 🎯 Step 7: Check Current Context

```bash
kubectl config current-context
```

---

## 🧭 Step 8: Set Default Namespace

### Minikube:
```bash
kubectl config set-context minikube --namespace=dev
```

### K3s:
```bash
kubectl config set-context default --namespace=qa
```

---

## 🧹 Step 9: Clean Up

```bash
kubectl config use-context minikube
kubectl delete deployment nginx -n default

kubectl config use-context default
kubectl delete deployment nginx -n default
```

---

## 🎉 End of Lab
You have learned how to manage multi-cluster kubeconfigs, switch contexts, and operate Minikube and K3s together.
