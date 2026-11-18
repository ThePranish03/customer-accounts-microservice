# Submission evidence checklist

This folder is reserved for evidence captured from actual execution of the assignment.

Do not treat screenshots, command outputs, or pipeline logs written by hand as proof that a service, workflow, Docker image, Kubernetes cluster, or Tekton Pipeline ran successfully.

Suggested evidence to capture after executing the relevant steps:

- GitHub Actions workflow run showing lint and tests.
- REST cURL terminal output for POST, GET list, GET by ID, PUT, and DELETE.
- Security headers from `curl -I http://localhost:5000/health`.
- Docker build and running container output.
- Kubernetes Deployment, Pods, ReplicaSets, Service and image output.
- Tekton PipelineRun logs from the cluster.

Record environment details and timestamps alongside screenshots.
