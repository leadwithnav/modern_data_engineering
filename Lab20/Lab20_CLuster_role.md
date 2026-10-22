# Lab: Kubernetes ClusterRole, ClusterRoleBinding, RoleBinding & Multi-User RBAC Testing

This lab demonstrates how to create two users, assign cluster-wide and namespace-wide permissions, and validate access using RBAC.

---

## ✅ Step 1: Create Two Users

Use your **user CSR process** to create two Kubernetes users:

- **nav**
- **joy**

(Generate key → CSR → submit via CSR API → admin approves → download certificate → set kubeconfig users.)

---

## ✅ Step 2: Create Two Namespaces

```bash
kubectl create namespace dev
kubectl create namespace prod
```

You now have two isolated environments:

- Namespace: **dev**
- Namespace: **prod**

---

## ✅ Step 3: Create a ClusterRole to Delete Deployments

This role gives permission to delete deployments **cluster-wide**.

```bash
kubectl create clusterrole deploy-deleter --verb=delete --resource=deployment
```

---

## ✅ Step 4: ClusterRoleBinding for First User (nav)

Bind the ClusterRole to user **nav** using a **ClusterRoleBinding**:

```bash
kubectl create clusterrolebinding deploy-deleter   --clusterrole=deploy-deleter   --user=nav
```

This gives user **nav** delete access to deployments **in all namespaces**.

---

## ✅ Step 5: RoleBinding for Second User (joy) Only in `dev` Namespace

Bind the same ClusterRole for user **joy**, but only inside namespace **dev**:

```bash
kubectl -n dev create rolebinding deploy-deleter   --clusterrole=deploy-deleter   --user=joy
```

This gives **joy** permissions only in namespace **dev**.

---

## ✅ Step 6: Test First User (nav)

```bash
kubectl auth can-i delete deploy --as nav               # yes
kubectl auth can-i delete deploy --as nav -n dev        # yes
kubectl auth can-i delete deploy --as nav -n prod       # yes
kubectl auth can-i delete deploy --as nav -A            # yes
kubectl auth can-i create deploy --as nav --all-namespaces  # no
```

### ✔ Observation
Because **nav** is bound using a **ClusterRoleBinding**,  
he has **delete access to deployments in every namespace**.

But nav does **not** have permission to create deployments.

---

## ✅ Step 7: Test Second User (joy)

```bash
kubectl auth can-i delete deploy --as joy                # no
kubectl auth can-i delete deploy --as joy -A            # no
kubectl auth can-i delete deploy --as joy -n dev        # yes
kubectl auth can-i delete deploy --as joy -n prod       # no
```

### ✔ Observation
Because **joy** is bound using a **RoleBinding** (namespace-scoped),  
he has delete access **only** inside namespace **dev**.

---

## 🎯 Lab Summary

| User | Binding Type | Scope | Can Delete Deployments |
|------|--------------|--------|------------------------|
| **nav** | ClusterRoleBinding | Cluster-wide | ✔ Yes, in all namespaces |
| **joy** | RoleBinding | Namespace-scoped (`dev`) | ✔ Yes, only in `dev` |

---

## 🎉 Lab Completed!

You learned:

- Difference between **ClusterRoleBinding** and **RoleBinding**
- How to assign cluster-level vs namespace-level permissions
- How to test RBAC using `kubectl auth can-i`
- How multiple users can have different privileges across namespaces

