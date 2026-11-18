# Customer Accounts Microservice

A Flask-based REST microservice for managing customer accounts. It provides create, list, retrieve, update, and delete operations with input validation, security headers, CORS configuration, automated tests, container packaging, Kubernetes resources, and a Tekton CI/CD pipeline.

![CI](https://github.com/ThePranish03/customer-accounts-microservice/actions/workflows/ci-build.yaml/badge.svg)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
flask --app service run --debug
```

The API listens on `http://127.0.0.1:5000`.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/accounts` | Create an account |
| GET | `/accounts` | List accounts |
| GET | `/accounts/<id>` | Read one account |
| PUT | `/accounts/<id>` | Replace account fields |
| DELETE | `/accounts/<id>` | Delete an account |
| GET | `/health` | Health check |

Example:
```bash
curl -X POST http://localhost:5000/accounts -H 'Content-Type: application/json' -d '{"name":"Asha Rao","email":"asha@example.com","status":"active"}'
curl http://localhost:5000/accounts
```

## Quality checks

```bash
flake8 service tests
nosetests
```

## Container

```bash
docker build -t customer-accounts:1.0 .
docker run --rm -p 5000:5000 customer-accounts:1.0
```

## Kubernetes

Apply the resources in `kubernetes/` with `kubectl apply -f kubernetes/`. The Deployment uses two replicas and exposes the API through a ClusterIP Service.

## CI/CD

GitHub Actions runs lint and unit tests on pushes and pull requests. A Tekton Pipeline definition is provided in `tekton/pipeline.yaml`.

## Security

Talisman adds common browser security headers. CORS is configurable through `CORS_ORIGINS`; by default, cross-origin access is disabled. Set a comma-separated allowlist for approved front-end origins.

## Project status

Source files and deployment definitions are committed. CI, Docker, and Kubernetes execution status should be verified in the repository Actions tab and on a live cluster; configuration files alone do not establish a successful deployment.
