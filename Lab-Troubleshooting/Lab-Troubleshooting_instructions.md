# ✅ Lab-Troubleshooting: Kubernetes Diagnostics & Fixes

**Time:** 25–30 Minutes  
**Cluster:** Minikube  
**Scope:** Pods, ReplicaSets, Deployments, and Services  

---

## 🧾 Lab Overview

In a production Kubernetes environment, issues typically occur across distinct architectural layers:
1. **Pod Layer**: Runtime failures, image pull errors, and resource constraints.
2. **ReplicaSet & Deployment Layer**: Rolling update stalls, crashed pods preventing replica readiness, and revision tracking.
3. **Service Layer**: Connectivity blackholes and misrouted traffic due to selector or port mismatches.

This lab provides **3 focused, real-world troubleshooting scenarios** designed to sharpen your diagnostic intuition using standard `kubectl` commands.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- 🔍 Troubleshoot a Pod stuck in `ImagePullBackOff` using `kubectl describe` and event inspection.
- 🔄 Diagnose why a **Deployment** rollout is stalled and inspect how the underlying **ReplicaSet** manages failing pods using `kubectl rollout status`, `kubectl get rs`, and container logs.
- 🌐 Resolve a **Service** routing failure by inspecting `Endpoints` and fixing mismatched label selectors.

---

## ☘️ Pre-requisite: Verify Minikube

Ensure your Minikube cluster is healthy before beginning:

```bash
minikube status
kubectl get nodes
```

Navigate to the lab directory:

```bash
cd D:\trainings\Modern_Platform_Engineering\Lab-Troubleshooting
```

---

## 🧩 Task 1: The Broken Pod (`ImagePullBackOff`)

### 📌 Problem Description
A developer submitted a Pod manifest, but the Pod refuses to start. You need to inspect the pod, identify the error, and fix it.

### Step 1: Deploy the Broken Pod
Deploy the provided `task1-broken-pod.yaml`:

```bash
kubectl apply -f task1-broken-pod.yaml
```

### Step 2: Observe the Symptom
Check the status of the Pod:

```bash
kubectl get pod broken-web-pod
```

**Observed Output:**
```
NAME             READY   STATUS         RESTARTS   AGE
broken-web-pod   0/1     ErrImagePull   0          10s
```
*(After a few seconds, it transitions to `ImagePullBackOff`)*.

### Step 3: Investigate Root Cause
Use `kubectl describe` to inspect the pod's recent lifecycle events:

```bash
kubectl describe pod broken-web-pod
```

Look at the **Events** section at the bottom:
```
Events:
  Type     Reason   Message
  ----     ------   -------
  Normal   BackOff  Back-off pulling image "nginx:alpine-nonexistent-tag"
  Warning  Failed   Error: ImagePullBackOff
  Warning  Failed   Failed to pull image "nginx:alpine-nonexistent-tag": manifest unknown
```

**Diagnostic Analysis:**
- The kubelet cannot pull `nginx:alpine-nonexistent-tag` because the tag does not exist in the container registry (`manifest unknown`).

### Step 4: Fix the Issue
Edit the file `task1-broken-pod.yaml` (or use `kubectl edit pod broken-web-pod`) and change the image tag to a valid image:

```yaml
    image: nginx:alpine
```

Delete and re-apply the corrected file:

```bash
kubectl delete -f task1-broken-pod.yaml
kubectl apply -f task1-broken-pod.yaml
```

### Step 5: Verify Recovery
Check the Pod status:

```bash
kubectl get pod broken-web-pod
```

**Expected Result:**
```
NAME             READY   STATUS    RESTARTS   AGE
broken-web-pod   1/1     Running   0          5s
```

Cleanup Task 1 before moving to Task 2:
```bash
kubectl delete pod broken-web-pod
```

---

## 🧩 Task 2: The Stalled Deployment & ReplicaSet (`CrashLoopBackOff`)

### 📌 Problem Description
A new version of an API service was deployed via a Kubernetes **Deployment**. The deployment rollout has stalled, and 0 of 2 replicas are available. You need to investigate the Deployment and its underlying **ReplicaSet** to understand why the rollout cannot finish.

### Step 1: Deploy the Stalled Deployment
Apply `task2-broken-deployment.yaml`:

```bash
kubectl apply -f task2-broken-deployment.yaml
```

### Step 2: Observe the Deployment Status
Check the status of the deployment:

```bash
kubectl get deployment api-deployment
```

**Observed Output:**
```
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
api-deployment   0/2     2            0           15s
```

Now check the rollout status:

```bash
kubectl rollout status deployment api-deployment
```

**Observed Output:**
```
Waiting for deployment "api-deployment" rollout to finish: 0 of 2 updated replicas are available...
```
*(Press `Ctrl + C` to exit the rollout status command)*.

### Step 3: Inspect the Underlying ReplicaSet
A Deployment does not manage Pods directly; it manages **ReplicaSets**. Inspect the ReplicaSet created by this deployment:

```bash
kubectl get rs -l app=api-app
```

**Observed Output:**
```
NAME                        DESIRED   CURRENT   READY   AGE
api-deployment-666bb85468   2         2         0       40s
```

The ReplicaSet created 2 pods as desired, but `0` are `READY`. Inspect the pods:

```bash
kubectl get pods -l app=api-app
```

**Observed Output:**
```
NAME                              READY   STATUS             RESTARTS      AGE
api-deployment-666bb85468-9dwc2   0/1     CrashLoopBackOff   2 (20s ago)   45s
api-deployment-666bb85468-w4r8c   0/1     CrashLoopBackOff   2 (20s ago)   45s
```

### Step 4: Investigate Container Logs
Inspect the logs of one of the crashing pods:

```bash
kubectl logs -l app=api-app --tail=10
```

**Observed Output:**
```
python: can't open file '/python-flask/non_existent_server.py': [Errno 2] No such file or directory
```

**Diagnostic Analysis:**
- The container specification has an invalid override `command: ["python", "non_existent_server.py"]`.
- Because the container crashes upon startup, the ReplicaSet cannot bring the pods to `Ready`.
- Consequently, the Deployment controller cannot consider the rollout complete.

### Step 5: Fix the Deployment
Open `task2-broken-deployment.yaml` and remove the broken `command` line:

```yaml
    spec:
      containers:
      - name: api-container
        image: technoavengers/flask-app:v1
        ports:
        - containerPort: 5000
        # REMOVE OR COMMENT OUT: command: ["python", "non_existent_server.py"]
```

Apply the updated file:

```bash
kubectl apply -f task2-broken-deployment.yaml
```

### Step 6: Verify Deployment & ReplicaSet Progression
Watch how the Deployment creates a **new ReplicaSet** and scales down the old broken ReplicaSet:

```bash
kubectl get rs -l app=api-app
```

**Observed Output:**
```
NAME                        DESIRED   CURRENT   READY   AGE
api-deployment-666bb85468   0         0         0       2m
api-deployment-f5dfcc78b    2         2         2       10s
```

Check the rollout status:

```bash
kubectl rollout status deployment api-deployment
```

**Expected Result:**
```
deployment "api-deployment" successfully rolled out
```

Cleanup Task 2 before proceeding:
```bash
kubectl delete deployment api-deployment
```

---

## 🧩 Task 3: The Silent Service (`Endpoints: <none>`)

### 📌 Problem Description
A web frontend deployment is running with 2 healthy pods. A `NodePort` Service was created to expose it to external traffic. However, users report that connecting to the service returns connection errors.

### Step 1: Deploy the Working Backend Application
Apply `task3-deployment.yaml`:

```bash
kubectl apply -f task3-deployment.yaml
```

Verify that the pods are running and healthy:

```bash
kubectl get pods -l app=web-frontend
```

**Expected Output:**
```
NAME                            READY   STATUS    RESTARTS   AGE
web-frontend-6b4b49976b-nf9xs   1/1     Running   0          10s
web-frontend-6b4b49976b-pqv4v   1/1     Running   0          10s
```

### Step 2: Deploy the Broken Service
Apply `task3-broken-service.yaml`:

```bash
kubectl apply -f task3-broken-service.yaml
```

### Step 3: Observe the Symptom
List the services:

```bash
kubectl get svc web-service
```

Try to access the service via Minikube:

```bash
minikube service web-service
```

Or test connectivity via `curl`:
The connection hangs or fails to return any response.

### Step 4: Investigate Service Endpoints
A Kubernetes Service routes traffic to Pods through **Endpoints**. Check the endpoints for `web-service`:

```bash
kubectl get endpoints web-service
```

**Observed Output:**
```
NAME          ENDPOINTS   AGE
web-service   <none>      25s
```

`<none>` means the Service does not know about any pods to route traffic to!

### Step 5: Find the Label Selector Mismatch
Inspect the Service configuration:

```bash
kubectl describe svc web-service
```

Notice:
```
Selector:                 app=web-front
Endpoints:                <none>
```

Now check the actual labels on the running Pods:

```bash
kubectl get pods --show-labels
```

Notice the Pod label:
```
app=web-frontend
```

**Diagnostic Analysis:**
- The Service selector is `app=web-front`, but the Pods have `app=web-frontend`.
- Because the labels do not match, the Service Endpoints controller registers `0` targets.

### Step 6: Fix the Service Selector
Edit `task3-broken-service.yaml` and update the selector to match the Pods:

```yaml
spec:
  type: NodePort
  selector:
    app: web-frontend   # Corrected label
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30080
```

Apply the corrected configuration:

```bash
kubectl apply -f task3-broken-service.yaml
```

### Step 7: Verify Recovery
Check the endpoints again:

```bash
kubectl get endpoints web-service
```

**Expected Result:**
```
NAME          ENDPOINTS                         AGE
web-service   10.244.0.114:80,10.244.0.115:80   2m
```

Test access via Minikube service or port-forward:

```bash
# In Minikube, open the service URL:
minikube service web-service
```

Or using port forwarding:
```bash
kubectl port-forward svc/web-service 8080:80
```
In your browser or terminal: `curl http://localhost:8080` (returns the Nginx Welcome page).

Cleanup Task 3:
```bash
kubectl delete deployment web-frontend
kubectl delete svc web-service
```

---

## 💡 Troubleshooting Cheat Sheet

| Object | Symptom | Diagnostic Command | Common Causes & Fixes |
| :--- | :--- | :--- | :--- |
| **Pod** | `ImagePullBackOff` / `ErrImagePull` | `kubectl describe pod <name>` | Typo in image name/tag, private repo authentication missing. |
| **Pod** | `CrashLoopBackOff` | `kubectl logs <name>` | Faulty startup command, missing config/env var, crash on init. |
| **ReplicaSet** | `DESIRED > READY` | `kubectl describe rs <name>` | Insufficient CPU/memory on node, pod scheduling blocked. |
| **Deployment** | Rollout stalled | `kubectl rollout status deploy/<name>` | Unhealthy new replica pods; check `kubectl get rs` and pod logs. |
| **Service** | Connection refused / `<none>` endpoints | `kubectl get endpoints <svc>` | Selector doesn't match Pod labels, or `targetPort` incorrect. |
