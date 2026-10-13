# Lab: Use ConfigMap for PostgreSQL Credentials in Flask App

## 🧩 Objective

You will:
- Create a ConfigMap and Secret to store PostgreSQL connection details.
- Inject values into PostgreSQL and Flask pods.
- Test Application

---

## ☘️ Pre-requiste : Setup K3s Cluster
1. Start Minikube
```bash
minikube start 
```


## 🚀 Step-by-Step Guide

### Step 1: Apply ConfigMap

```bash
cd ~/modern_data_engineering/Lab7
kubectl apply -f configmap.yaml
```

Check Configmap

```bash
kubectl get configmap
```

### Step 2: Create Secret for Postgres Credentials
```bash
kubectl create secret generic postgres-secret \
  --from-literal=DB_USER=flaskuser \
  --from-literal=DB_PASSWORD=flaskpass
```
Check Secrets
```bash
kubectl get secret
```

### Step 3: Create PVC with Storage Class

```bash
kubectl apply -f postgres-pv-pvc.yaml
```

### Step 4: Deploy PostgreSQL

```bash
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
```
Check Postgres Pod & Service
```bash
kubectl get pod
kubectl get svc
```


### Step 5: Deploy Flask App

```bash
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```

Check Flask Pod & Service
```bash
kubectl get pod
kubectl get svc
```

### Step 6: Connect to Flask Pod

Connect to Flask Pod terminal 
```bash
kubectl exec -it flask-pod-name -- bash
```
Once inside the pod, check for environment variables that you have set in configmap
```bash
env
```

Once inside the pod, check for mounted secret
```bash
cat /mnt/secrets/DB_USER
cat /mnt/secrets/DB_PASSWORD
```

Exit the pod
```bash
exit
```

## ☘️ Step 7: Access the Flask App

```bash
minikube service flask-service
```

---

## ☘️ Step 8: Test the App

- Fill in a **username** and **age**
- Click **Submit**
- You should see:  
  `Thank you, <name>! Your age <age> has been recorded.`

---

## 🧹 Cleanup

```bash
cd ~/modern_data_engineering/Lab7
kubectl delete -f .
```
