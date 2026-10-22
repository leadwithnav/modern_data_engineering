# Lab: Creating a Kubernetes User Using Certificates + CSR API + kubeconfig

## Objective
This lab teaches you how to create a Kubernetes user using certificates, CSR API, admin approval, and kubeconfig setup.

## Step 1: Start Minikube

```bash
minikube start
```

---

## Step 1: Generate a Private Key

```bash
cd ~/swift_training/Lab18
openssl genrsa -out nav.key 2048
```

---

## Step 2: Create CSR (Certificate Signing Request)

👉 While running below, populate **Common Name (CN)** with the username.

```bash
openssl req -new -key nav.key -out nav.csr
```

Example prompt:

```
Common Name (CN): nav
```

---

## Step 3: Sign CSR Using Kubernetes API

### 3.1 Base64‑encode CSR

```bash
cat nav.csr | base64 -w 0
```

Copy the output.

### 3.2 Create csr.yaml

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: nav
spec:
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 31536000
  request: |
    <BASE64_CSR_HERE>
  usages:
  - client auth
```

Apply:

```bash
kubectl create -f csr.yaml
```

---

## Step 4: Admin Approves CSR

```bash
kubectl get csr
kubectl certificate approve nav
```

---

## Step 5: Download Signed Certificate

```bash
kubectl get csr nav -o=jsonpath='{.status.certificate}' | base64 -d > nav.crt
```

Files now available:

- **nav.key**
- **nav.crt**

---

## Step 6: Add User to Kubeconfig

View current config:

```bash
kubectl config view
```

Add user:

```bash
kubectl config set-credentials nav --client-key=nav.key --client-certificate=nav.crt
```


Check:

```bash
kubectl config view
```

---

## Step 7: Create/Use Context for New User

```bash
kubectl config set-context nav --user=nav --cluster=minikube
kubectl config get-contexts
kubectl config use-context nav
```

---

## Step 8: Check Permissions

```bash
kubectl auth can-i get pod -A
```

Expected: **no** (until RBAC is assigned)

---

---

## Lab Completed
You successfully created a new Kubernetes user and authenticated using signed certificates.

