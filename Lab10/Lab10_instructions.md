# ✅ Lab 10: Run ArgoCD on Minikube Cluster Using ArgoCD Helm Chart & Access UI

🕒 **Estimated Time:** 25–35 Minutes  
🎯 **Focus Areas:** GitOps, ArgoCD, Helm 3, Minikube, Kubernetes Services, Port-Forwarding, Secret Management

---

## 🧠 Lab Summary

In this lab, you will deploy **ArgoCD**—the declarative, GitOps continuous delivery tool for Kubernetes—on a local **Minikube** cluster using the official **ArgoCD Helm Chart**.

You will learn how to:
1. Prepare a Minikube cluster and dedicated namespace for ArgoCD.
2. Add and update the official Argo Helm repository.
3. Configure ArgoCD server settings via custom `values.yaml` for local development.
4. Install ArgoCD with Helm.
5. Extract the initial auto-generated admin password from Kubernetes secrets.
6. Access the ArgoCD Web UI in your local browser via Port-Forwarding and NodePort.
7. Deploy a sample GitOps application using an ArgoCD Application manifest.
8. Clean up all resources.

---

## 🎯 Objectives

- 🚀 Setup and verify Minikube cluster readiness.
- 📦 Add the official `argo-helm` repository and search available charts.
- ⚙️ Customize ArgoCD server settings for Minikube (disabling TLS termination or using NodePort).
- 🛠️ Install and manage the ArgoCD release using Helm 3.
- 🔐 Retrieve and decode the admin secret from `argocd-initial-admin-secret`.
- 🌐 Expose and access the ArgoCD web console at `http://localhost:8080`.
- 📋 Deploy a sample application to observe automated GitOps synchronization.
- 🧹 Uninstall the Helm release and clean up namespaces.

---

## 🏗️ Architecture Overview

```
                      +------------------------------------------+
                      |             Minikube Cluster             |
                      |                                          |
                      |   Namespace: 'argocd'                    |
                      |  +------------------------------------+  |
  Browser / User      |  | ArgoCD Server (Port 80/443)        |  |
  http://localhost:8080 ----> [Service: argocd-server]        |  |
        |             |  +------------------------------------+  |
        |             |  +------------------------------------+  |
        v             |  | ArgoCD Repo Server                 |  |
  [Git Repository]    |  | ArgoCD Application Controller      |  |
  (e.g., Guestbook) <------- Syncs desired state to cluster   |  |
                      |  +------------------------------------+  |
                      +------------------------------------------+
```

---

## ☘️ Step 1: Start and Verify Minikube Cluster

Ensure your Minikube cluster has sufficient resources (minimum 2 CPUs, 4GB RAM recommended for ArgoCD):

```bash
minikube start --cpus=2 --memory=4096 --driver=docker
```

Verify that the node is ready:

```bash
kubectl get nodes
```

---

## ☘️ Step 2: Create a Dedicated Namespace for ArgoCD

ArgoCD components should be isolated in their own namespace (typically `argocd`):

```bash
kubectl create namespace argocd
```

Verify namespace creation:

```bash
kubectl get namespaces
```

---

## ☘️ Step 3: Add the Argo Helm Repository

Add the official Argo chart repository to your Helm client:

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```

Search for the ArgoCD chart to verify available versions:

```bash
helm search repo argo/argo-cd
```

---

## ☘️ Step 4: Review and Configure Custom Helm Values

For local Minikube development, we can configure the ArgoCD server:
- Run in **insecure mode** (`--insecure`), allowing plain HTTP behind port-forwarding without SSL certificate warnings.
- Optional: Set service type to `NodePort` or `ClusterIP`.

Inspect `Lab10/argocd-values.yaml`:

```yaml
global:
  domain: localhost:8080

server:
  extraArgs:
    - --insecure
  service:
    type: ClusterIP
```

---

## ☘️ Step 5: Install ArgoCD with Helm

Deploy ArgoCD into the `argocd` namespace using our custom values:

```bash
cd Lab10
helm install argocd argo/argo-cd -n argocd -f argocd-values.yaml
```

Check the status of the Helm release:

```bash
helm list -n argocd
```

---

## ☘️ Step 6: Wait for ArgoCD Pods to be Ready

ArgoCD consists of multiple microservices:
- `argocd-server`: Web UI and API server
- `argocd-repo-server`: Clones Git repos and renders manifests
- `argocd-application-controller`: Reconciles cluster state with Git
- `argocd-dex-server`: Identity provider
- `argocd-redis`: Cache backend

Watch until all pods transition to `Running`:

```bash
kubectl get pods -n argocd -w
```

Press `Ctrl+C` once all pods are in `Running` or `Completed` state.

---

## ☘️ Step 7: Retrieve the Initial Admin Password

ArgoCD generates an initial random admin password and stores it in a Kubernetes secret named `argocd-initial-admin-secret`.

### On Linux / macOS / Git Bash:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

### On Windows PowerShell:
```powershell
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}")))
```

> 🔐 **Default Username:** `admin`  
> 🔑 **Default Password:** Output from the command above.

---

## ☘️ Step 8: Access the ArgoCD Web UI

### Option A: Port-Forwarding (Recommended for Local Dev)

Forward local port `8080` to the `argocd-server` service:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:80
```

Now open your web browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

### Option B: Minikube Service (Alternative)

If using `NodePort`, you can use Minikube's built-in service helper:

```bash
minikube service argocd-server -n argocd
```

---

## ☘️ Step 9: Log in to ArgoCD UI

1. Open **`http://localhost:8080`** in your browser.
2. Enter username: **`admin`**
3. Enter the decoded password from **Step 7**.
4. Click **Sign In**.
5. You are now greeted by the ArgoCD Applications dashboard! 🎉

---

## ☘️ Step 10: Deploy a Sample GitOps Application (Guestbook)

Deploy a sample application to witness declarative GitOps synchronization in action.

Review `Lab10/guestbook-app.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

Apply the application manifest:

```bash
kubectl apply -f guestbook-app.yaml
```

Now return to your ArgoCD web UI at `http://localhost:8080`:
- Click on the **guestbook** card.
- Watch ArgoCD visualize the real-time resource dependency tree (Deployment, ReplicaSet, Pods, Service).
- Notice the **Healthy** and **Synced** status badges!

---

## ☘️ Step 11: Cleanup

When you are done experimenting, clean up all resources:

1. Delete the sample guestbook application:
```bash
kubectl delete -f guestbook-app.yaml
```

2. Uninstall the ArgoCD Helm release:
```bash
helm uninstall argocd -n argocd
```

3. Delete the `argocd` namespace:
```bash
kubectl delete namespace argocd
```

---

## ✅ Conclusion

In this lab, you:
- Provisioned ArgoCD on a local Minikube cluster using the official Helm chart.
- Configured customized Helm values to optimize local development.
- Extracted and decoded initial cluster admin credentials.
- Connected to the ArgoCD web console and navigated its UI.
- Deployed a GitOps application and observed declarative synchronization in real time.

🎉 **Congratulations! You have completed Lab 10: Running ArgoCD on Minikube!**  
✨ **END OF LAB** ✨
