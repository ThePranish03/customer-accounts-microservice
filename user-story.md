# Customer Accounts — User Stories

## Product goal
Provide a small, dependable service through which a client application can manage customer account records over HTTP.

## User stories

1. **Create account** — As an account administrator, I want to create an account with a name and email so that a customer can be registered.
   - Acceptance: valid JSON creates a record and returns HTTP 201; missing required fields return HTTP 400; duplicate email returns HTTP 409.
2. **List accounts** — As a support agent, I want to list accounts so that I can find a customer record.
   - Acceptance: the endpoint returns a JSON array and returns an empty array when no records exist.
3. **Read account** — As a support agent, I want to retrieve one account by ID so that I can inspect its details.
   - Acceptance: a known ID returns HTTP 200; an unknown ID returns HTTP 404.
4. **Update account** — As an account administrator, I want to update account details so that customer information remains current.
   - Acceptance: valid updates return the updated record; invalid values return HTTP 400; unknown IDs return HTTP 404.
5. **Delete account** — As an account administrator, I want to remove an account so that obsolete records are not retained.
   - Acceptance: deletion returns HTTP 204; repeating the deletion returns HTTP 404.
6. **Protect API clients** — As an application owner, I want security headers and an explicit CORS allowlist so that browser access is controlled.
   - Acceptance: responses include security headers and only configured origins are allowed.
7. **Automate quality checks** — As a maintainer, I want lint and tests to run on every push and pull request so that defects are caught early.
   - Acceptance: CI executes Flake8 and nose tests and reports their true status.

## Definition of done
Code is reviewed, tests pass, lint is clean, API behavior is documented, and Docker/Kubernetes/Tekton resources are checked against the target runtime. Screenshots and logs used as submission evidence must come from actual tool execution.
