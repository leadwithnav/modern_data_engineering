# Kubernetes Lab: Pod Affinity & Pod Anti-Affinity (Complete Practical Lab)

## 🕒 Estimated Time
30 minutes

## 🎯 Objective
Learn how Kubernetes uses **pod affinity** and **pod anti-affinity** rules to place pods close together or far apart for performance, resilience, and availability.

---

# 🧠 Concept Overview

## 🔵 Pod Affinity
Pods prefer or require to run **close to** another pod  
(usually on the same node or zone).

Use cases:
- Low-latency services  
- Sidecar-style co-location  
- Cache + API combo

---

## 🔴 Pod Anti-Affinity
Pods prefer or require to run **away from** other pods  
(usually on different nodes).

Use cases:
- High availability  
- Multi-zone replicas  
- Reduce single-node risk

---

# 🏗 Cluster Requirement
A cluster with **2 or more nodes**  
(ex: Minikube with 3 nodes)

---

# 🪜 STEP 1 — Label the Nodes

We add custom labels for affinity rules.

```bash
kubectl label nodes minikube-m02 zone=zoneA
kubectl label nodes minikube-m03 zone=zoneB
```

Verify:

```bash
kubectl get nodes --show-labels
```

---

# 🟦 STEP 2 — Deploy the Anchor Pod  
(This pod will be used for affinity/anti-affinity tests)

Create `anchor-pod.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: anchor-pod
  labels:
    app: anchor
spec:
  containers:
  - name: nginx
    image: nginx
```

Apply:

```bash
kubectl apply -f anchor-pod.yaml
kubectl get pod -o wide
```

Observe which node the pod is running on.

---

# 💙 STEP 3 — Pod Affinity: Run on SAME Node as anchor-pod

Create `pod-affinity.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-affinity
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - anchor
        topologyKey: kubernetes.io/hostname
  containers:
  - name: nginx
    image: nginx
```

Apply:

```bash
kubectl apply -f pod-affinity.yaml
kubectl get pod -o wide
```

### ✔ Expected:
Pod **MUST** run on the **same node** as `anchor-pod`.

---

# ❤️ STEP 4 — Pod Anti-Affinity: Run on DIFFERENT Node than anchor-pod

Create `pod-anti-affinity.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-anti-affinity
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - anchor
        topologyKey: kubernetes.io/hostname
  containers:
  - name: nginx
    image: nginx
```

Apply:

```bash
kubectl apply -f pod-anti-affinity.yaml
kubectl get pod -o wide
```

### ✔ Expected:
Pod **MUST NOT** run on the same node as `anchor-pod`.

---

# ⚡ STEP 5 — Soft Pod Affinity (Preferred Scheduling)

Create `pod-soft-affinity.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-soft-affinity
spec:
  affinity:
    podAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - anchor
          topologyKey: kubernetes.io/hostname
  containers:
  - name: nginx
    image: nginx
```

Apply:

```bash
kubectl apply -f pod-soft-affinity.yaml
kubectl get pod -o wide
```

### ✔ Expected:
Pod **prefers** same node as `anchor-pod`,  
but scheduler may place it elsewhere if resources are constrained.

---

# ⚡ STEP 6 — Soft Pod Anti-Affinity (Preferred Separation)

Create `pod-soft-anti-affinity.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-soft-anti-affinity
spec:
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - anchor
          topologyKey: kubernetes.io/hostname
  containers:
  - name: nginx
    image: nginx
```

Apply:

```bash
kubectl apply -f pod-soft-anti-affinity.yaml
kubectl get pod -o wide
```

### ✔ Expected:
Pod **prefers** to avoid anchor-pod’s node  
but may run on same node if no other nodes fit.

---

# 🧹 STEP 7 — Cleanup Resources

```bash
kubectl delete pod anchor-pod
kubectl delete pod pod-with-affinity
kubectl delete pod pod-with-anti-affinity
kubectl delete pod pod-soft-affinity
kubectl delete pod pod-soft-anti-affinity
```

---

# 🎉 LAB COMPLETED — WHAT YOU LEARNED

## 🔵 Pod Affinity
- Forces pods to run *together*
- Useful for low-latency workloads  
- `requiredDuringScheduling`: strict  
- `preferredDuringScheduling`: soft  

## 🔴 Pod Anti-Affinity
- Forces pods to run *apart*  
- Useful for high-availability replicas  
- `requiredDuringScheduling`: guaranteed  
- `preferredDuringScheduling`: best-effort  

---

This completes the **Pod Affinity & Pod Anti-Affinity Lab**!
