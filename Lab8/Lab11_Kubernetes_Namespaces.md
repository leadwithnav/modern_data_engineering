
# ✅ Lab 8: Understanding Namespaces in Kubernetes

🕒 **Estimated Time**: 15–20 minutes

---

## 🎯 Objective
This lab helps you understand how namespaces work in Kubernetes and how they help in organizing, isolating, and managing resources within a cluster. You will create namespaces, deploy resources inside them, and explore namespace-scoped operations.

---

## 🔍 Introduction

Namespaces in Kubernetes provide a way to divide cluster resources between multiple users or teams. They help:
- Avoid name collisions.
- Apply role-based access control (RBAC) at a fine-grained level.
- Scope resource quotas and limits.
- Organize deployments in large clusters.

---

## 🪜 Step 1: List Default Namespaces

```bash
kubectl get namespaces
```

You should see default namespaces like:
- `default`
- `kube-system`
- `kube-public`
- `kube-node-lease`

---

## ☘️ Step 2: Create a New Namespace

```bash
kubectl create namespace dev-team
kubectl create namespace qa-team
```

Verify:

```bash
kubectl get namespaces
```

---

## ☸️ Step 3: Deploy Applications in Specific Namespaces

Create a deployment in the `dev-team` namespace:

```bash
kubectl create deployment nginx-dev --image=nginx --namespace=dev-team
```

Create a deployment in the `qa-team` namespace:

```bash
kubectl create deployment nginx-qa --image=nginx --namespace=qa-team
```

---

## 🔍 Step 4: Verify Deployments in Namespaces

```bash
kubectl get all -n dev-team
kubectl get all -n qa-team
```

---

## 🔁 Step 5: Set a Default Namespace (Optional)

To avoid specifying `-n` repeatedly, set the default namespace for your context:

```bash
kubectl config set-context --current --namespace=dev-team
kubectl get pods
```

Reset:

```bash
kubectl config set-context --current --namespace=default
```

---

## 🧹 Step 6: Clean Up Resources

```bash
kubectl delete namespace dev-team
kubectl delete namespace qa-team
```

---

## ✅ End of Lab

You have learned how to:
- Create and manage namespaces.
- Deploy resources into specific namespaces.
- Scope commands and clean up namespace-specific workloads.
