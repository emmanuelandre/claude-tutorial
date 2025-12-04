# CI/CD and Deployment

Setting up continuous integration and deployment pipelines for AI-first development.

## CI/CD Philosophy

In AI-first development, automated pipelines are essential:
- **Every commit is tested** - Catch issues early
- **Fast feedback** - Know within minutes if something is broken
- **Consistent quality** - Same checks every time
- **Safe deployment** - Automated, repeatable process

---

## GitHub Actions Setup

### Basic Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Install dependencies
        run: go mod download

      - name: Run tests
        run: go test -v ./...
```

### Complete Go CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  GO_VERSION: '1.21'

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}

      - name: Run golangci-lint
        uses: golangci/golangci-lint-action@v4
        with:
          version: latest

  test:
    name: Test
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/testdb?sslmode=disable
        run: |
          go test -race -coverprofile=coverage.out -covermode=atomic ./...

      - name: Check coverage threshold
        run: |
          coverage=$(go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//')
          echo "Coverage: $coverage%"
          if (( $(echo "$coverage < 70" | bc -l) )); then
            echo "Coverage $coverage% is below 70% threshold"
            exit 1
          fi

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: coverage.out

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}

      - name: Build
        run: go build -o bin/server ./cmd/server

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: server
          path: bin/server

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Gosec
        uses: securego/gosec@master
        with:
          args: ./...

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
```

### Node.js/TypeScript CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Run tests
        run: npm test -- --coverage

      - name: Check coverage
        run: |
          coverage=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          echo "Coverage: $coverage%"
          if (( $(echo "$coverage < 70" | bc -l) )); then
            echo "Coverage below threshold"
            exit 1
          fi

  e2e:
    runs-on: ubuntu-latest
    needs: lint-and-test
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/

  build:
    runs-on: ubuntu-latest
    needs: [lint-and-test, e2e]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload build
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/
```

---

## Pre-Commit Hooks

Run checks locally before pushing.

### Husky Setup (Node.js)

```bash
# Install
npm install husky lint-staged --save-dev
npx husky init
```

```json
// package.json
{
  "scripts": {
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{js,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npm run lint-staged
npm test
```

### Pre-commit Framework (Python/Multi-language)

```yaml
# .pre-commit-config.yaml
repos:
  # Go
  - repo: local
    hooks:
      - id: go-fmt
        name: Go Format
        entry: go fmt ./...
        language: system
        types: [go]
        pass_filenames: false

      - id: go-vet
        name: Go Vet
        entry: go vet ./...
        language: system
        types: [go]
        pass_filenames: false

      - id: go-test
        name: Go Test
        entry: go test ./...
        language: system
        types: [go]
        pass_filenames: false

  # General
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict

  # Secrets
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

```bash
# Install
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Testing in CI

### Running Tests with Services

```yaml
# PostgreSQL service
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_PASSWORD: test
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5

# Redis service
  redis:
    image: redis:7
    ports:
      - 6379:6379
    options: >-
      --health-cmd "redis-cli ping"
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

### E2E Tests with Cypress

```yaml
e2e:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Install dependencies
      run: npm ci

    - name: Start application
      run: npm run start &
      env:
        DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

    - name: Wait for server
      run: npx wait-on http://localhost:3000

    - name: Run Cypress
      uses: cypress-io/github-action@v6
      with:
        wait-on: http://localhost:3000

    - name: Upload screenshots on failure
      if: failure()
      uses: actions/upload-artifact@v4
      with:
        name: cypress-screenshots
        path: cypress/screenshots
```

### Test Containers

```go
// For integration tests with real databases
import (
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
)

func setupTestDB(t *testing.T) *sql.DB {
    ctx := context.Background()

    container, err := postgres.RunContainer(ctx,
        testcontainers.WithImage("postgres:16"),
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
    )
    require.NoError(t, err)

    t.Cleanup(func() { container.Terminate(ctx) })

    connStr, _ := container.ConnectionString(ctx, "sslmode=disable")
    db, _ := sql.Open("postgres", connStr)

    return db
}
```

---

## Deployment Pipelines

### Deploy to Staging on Push

```yaml
# .github/workflows/deploy-staging.yml
name: Deploy Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .

      - name: Push to registry
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USER }} --password-stdin
          docker tag myapp:${{ github.sha }} registry.example.com/myapp:staging
          docker push registry.example.com/myapp:staging

      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp myapp=registry.example.com/myapp:staging
        env:
          KUBECONFIG: ${{ secrets.STAGING_KUBECONFIG }}
```

### Deploy to Production on Release

```yaml
# .github/workflows/deploy-production.yml
name: Deploy Production

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.event.release.tag_name }} .

      - name: Push to registry
        run: |
          docker tag myapp:${{ github.event.release.tag_name }} registry.example.com/myapp:${{ github.event.release.tag_name }}
          docker tag myapp:${{ github.event.release.tag_name }} registry.example.com/myapp:latest
          docker push registry.example.com/myapp:${{ github.event.release.tag_name }}
          docker push registry.example.com/myapp:latest

      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp myapp=registry.example.com/myapp:${{ github.event.release.tag_name }}
        env:
          KUBECONFIG: ${{ secrets.PROD_KUBECONFIG }}

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/myapp --timeout=5m
```

### Database Migrations in CI

```yaml
migrate:
  runs-on: ubuntu-latest
  needs: [test]
  if: github.ref == 'refs/heads/main'
  steps:
    - uses: actions/checkout@v4

    - name: Run migrations
      run: |
        migrate -path ./migrations -database ${{ secrets.DATABASE_URL }} up
      env:
        DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
```

---

## Rollback Strategies

### Kubernetes Rollback

```yaml
# In deployment workflow
- name: Deploy
  id: deploy
  run: |
    kubectl set image deployment/myapp myapp=$IMAGE
    kubectl rollout status deployment/myapp --timeout=5m
  continue-on-error: true

- name: Rollback on failure
  if: steps.deploy.outcome == 'failure'
  run: |
    kubectl rollout undo deployment/myapp
    echo "::error::Deployment failed, rolled back to previous version"
    exit 1
```

### Blue-Green Deployment

```yaml
# Deploy to green environment
- name: Deploy to green
  run: |
    kubectl apply -f k8s/deployment-green.yaml
    kubectl rollout status deployment/myapp-green

# Health check
- name: Health check green
  run: |
    curl -f http://myapp-green.internal/health

# Switch traffic
- name: Switch traffic to green
  run: |
    kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'

# Cleanup old deployment
- name: Remove blue
  run: |
    kubectl delete deployment myapp-blue
```

---

## Environment Management

### GitHub Environments

```yaml
jobs:
  deploy-staging:
    environment: staging  # Requires approval if configured
    env:
      API_URL: ${{ vars.API_URL }}  # Environment-specific variable
      API_KEY: ${{ secrets.API_KEY }}  # Environment-specific secret
```

### Environment-Specific Configs

```yaml
# config/staging.yaml
database:
  host: staging-db.example.com
  pool_size: 5

# config/production.yaml
database:
  host: prod-db.example.com
  pool_size: 25
```

```go
func LoadConfig() *Config {
    env := os.Getenv("ENV")  // staging, production
    configFile := fmt.Sprintf("config/%s.yaml", env)
    // Load config...
}
```

---

## Example Complete Workflows

### Monorepo with Multiple Services

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'services/api/**'
            web:
              - 'services/web/**'

  test-api:
    needs: detect-changes
    if: needs.detect-changes.outputs.api == 'true'
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: services/api
    steps:
      - uses: actions/checkout@v4
      - run: go test ./...

  test-web:
    needs: detect-changes
    if: needs.detect-changes.outputs.web == 'true'
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: services/web
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
```

---

## CI/CD Checklist

### Pre-Merge Checks
- [ ] All tests pass (unit + E2E)
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Coverage meets threshold
- [ ] Security scan clean
- [ ] Build succeeds

### Deployment Checks
- [ ] Migrations run successfully
- [ ] Health checks pass
- [ ] Smoke tests pass
- [ ] Monitoring alerts clear
- [ ] Rollback tested

### Secrets Management
- [ ] Secrets in GitHub Secrets
- [ ] No secrets in code
- [ ] Secrets rotated regularly
- [ ] Minimal access scope

---

**Prev:** [Performance Optimization](./16-performance.md) | **Next:** [Advanced Topics](./18-advanced-topics.md)
