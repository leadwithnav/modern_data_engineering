# Lab: Kubernetes RBAC - Roles, RoleBindings, and User Access Testing

This lab demonstrates how to create Roles, RoleBindings, set context to a user, and validate permissions across namespaces.

---

## ✅ Step 1: Make Sure You Are in Admin Context

```bash
kubectl config get-contexts
kubectl config use-context minikube
```

Ensure you are using the minikube context which has admin permission before modifying RBAC.

---

## ✅ Step 2: Create Pods in `default` and `sample` Namespace

### Create a pod in the **default** namespace:

```bash
kubectl run httpd-default --image httpd
```

### Create the **sample** namespace:

```bash
kubectl create namespace sample
```

### Create a pod inside **sample** namespace:

```bash
kubectl run httpd-default --image httpd -n sample
```

Now you have:

- `httpd-default` in **default**
- `httpd-default` in **sample**

---

## ✅ Step 3: Create a Role Using `roles.yaml`

Your `roles.yaml` gives:  
✔ get  
✔ list  
✔ delete  
✔ describe  
permissions on **pods** in the **default** namespace.

Apply the Role:

```bash
kubectl create -f roles.yaml
```

---

## ✅ Step 4: Create a RoleBinding Using `rolebinding.yaml`

> Update the YAML file to bind the Role to your user (e.g., `nav`).

Example:

```bash
kubectl create -f rolebinding.yaml
```

This binds the Role to the user and grants access only in the **default** namespace.

---

## ✅ Step 5: Switch Context to the User

```bash
kubectl config get-contexts
kubectl config use-context nav
```

This makes kubectl operate as your restricted user.

---

## ✅ Step 6: Test User Permissions

### ✔ User tries to view pods:

```bash
kubectl get pod
```

➡️ User **can** view pods in default namespace.

---

### ✔ User tries to delete pod:

```bash
kubectl delete pod httpd-default
```

➡️ User **can** delete because role includes delete.

---

### ✔ User tries to access pods in another namespace:

```bash
kubectl get pod -n sample
```

➡️ User **cannot** access pods in `sample` namespace  
(because RoleBinding is only for `default`).

---

## ✅ Step 7: Return to Admin Context

```bash
kubectl config get-contexts
kubectl config use-context minikube
```

Always return to minikube (admin) context before creating new RBAC objects.

---

## ✅ Step 8: Create Roles and RoleBindings Using Commands (No YAML)

### Create a Role:

```bash
kubectl create -n default role secret-manager   --verb=get --verb=list --resource=secret
```

### Bind it to user `nav`:

```bash
kubectl create -n default rolebinding secret-manager   --role=secret-manager --user=nav
```

---

## ✅ Step 9: Test User Permissions Again

### Test if user can view secrets:

```bash
kubectl auth can-i get secret --as nav
```

### Test if user can delete secrets:

```bash
kubectl auth can-i delete secret --as nav
```

Expected:

- `get secret` → **yes**
- `delete secret` → **no**

---

## 🎉 Lab Completed!

You learned how to:

- Create pods in namespaces  
- Create Roles and RoleBindings  
- Switch kubectl context to a user  
- Validate RBAC permissions  
- Create RBAC using both YAML and command-line  
- Test fine‑grained access control  

This lab is fully compatible with minikube, kubeadm clusters, EKS, k3s, and AKS.

