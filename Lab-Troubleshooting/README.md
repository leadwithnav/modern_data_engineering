# Lab-Troubleshooting: Pods, ReplicaSets, Deployments, and Services

This lab contains 3 hands-on troubleshooting exercises for Minikube:

1. **Task 1: The Broken Pod (`ImagePullBackOff`)**
   - File: `task1-broken-pod.yaml`
   - Troubleshoot Pod image pull errors using `kubectl describe pod`.

2. **Task 2: The Stalled Deployment & ReplicaSet (`CrashLoopBackOff`)**
   - File: `task2-broken-deployment.yaml`
   - Troubleshoot rollout stalls and inspect the Deployment -> ReplicaSet -> Pod lifecycle using `kubectl rollout status`, `kubectl get rs`, and `kubectl logs`.

3. **Task 3: The Silent Service (`Endpoints: <none>`)**
   - Files: `task3-deployment.yaml`, `task3-broken-service.yaml`
   - Troubleshoot routing blackholes and selector label mismatches using `kubectl get endpoints` and `kubectl describe svc`.

For full step-by-step instructions, see [`Lab-Troubleshooting_instructions.md`](./Lab-Troubleshooting_instructions.md).
