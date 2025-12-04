# Performance Optimization

How to identify and resolve performance issues in AI-first development.

## Performance-First Mindset

**Core principle:** Measure before optimizing.

```
1. Define performance goals
2. Measure current state
3. Identify bottlenecks
4. Optimize the bottleneck
5. Measure again
6. Repeat
```

**Don't:**
- Optimize without measuring
- Assume you know where the problem is
- Optimize everything at once
- Sacrifice readability for micro-optimizations

---

## Performance Budgets

Set clear targets before implementation:

| Metric | Target | Measurement |
|--------|--------|-------------|
| API response (p50) | < 100ms | Server-side |
| API response (p95) | < 500ms | Server-side |
| Page load (FCP) | < 1.5s | Lighthouse |
| Page load (LCP) | < 2.5s | Lighthouse |
| Time to Interactive | < 3.5s | Lighthouse |
| Bundle size (JS) | < 200KB gzip | Build output |

---

## Database Performance

### Query Optimization

**Identify slow queries:**
```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1s
```

**Common optimizations:**

**1. Add indexes:**
```sql
-- Before: Full table scan
SELECT * FROM users WHERE email = 'user@example.com';
-- Query time: 500ms (1M rows)

-- After: Index scan
CREATE INDEX idx_users_email ON users(email);
-- Query time: 1ms
```

**2. Use composite indexes for multi-column queries:**
```sql
-- Query pattern
SELECT * FROM orders WHERE user_id = 1 AND status = 'pending';

-- Single column index - partially effective
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index - optimal for this query
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

**3. Avoid SELECT *:**
```go
// ❌ Fetches all columns
rows, _ := db.Query("SELECT * FROM users WHERE id = $1", id)

// ✅ Fetch only needed columns
rows, _ := db.Query("SELECT id, email, name FROM users WHERE id = $1", id)
```

### N+1 Query Problem

The most common performance issue in AI-generated code.

**Problem:**
```go
// Fetches all orders
orders, _ := db.Query("SELECT * FROM orders")

for orders.Next() {
    var order Order
    orders.Scan(&order.ID, &order.UserID, ...)

    // N additional queries!
    user, _ := db.QueryRow("SELECT * FROM users WHERE id = $1", order.UserID)
}
// 1 + N queries total
```

**Solution - JOIN:**
```go
query := `
    SELECT o.id, o.total, u.id, u.name, u.email
    FROM orders o
    JOIN users u ON u.id = o.user_id
`
rows, _ := db.Query(query)
// 1 query total
```

**Solution - Batch load:**
```go
// Get all orders
orders, _ := getOrders()

// Collect unique user IDs
userIDs := make(map[int]bool)
for _, o := range orders {
    userIDs[o.UserID] = true
}

// Single query for all users
users, _ := getUsersByIDs(keys(userIDs))
// 2 queries total (regardless of order count)
```

### Connection Pooling

```go
import "database/sql"

func SetupDB() *sql.DB {
    db, _ := sql.Open("postgres", connectionString)

    // Configure pool
    db.SetMaxOpenConns(25)              // Max concurrent connections
    db.SetMaxIdleConns(5)               // Idle connections to keep
    db.SetConnMaxLifetime(5 * time.Minute)  // Recycle connections

    return db
}
```

### Caching Strategies

**Application-level cache:**
```go
import "github.com/patrickmn/go-cache"

var userCache = cache.New(5*time.Minute, 10*time.Minute)

func GetUser(id int) (*User, error) {
    // Check cache first
    key := fmt.Sprintf("user:%d", id)
    if cached, found := userCache.Get(key); found {
        return cached.(*User), nil
    }

    // Cache miss - fetch from DB
    user, err := db.GetUser(id)
    if err != nil {
        return nil, err
    }

    // Store in cache
    userCache.Set(key, user, cache.DefaultExpiration)
    return user, nil
}
```

**Redis cache:**
```go
func GetUser(ctx context.Context, id int) (*User, error) {
    key := fmt.Sprintf("user:%d", id)

    // Try cache
    data, err := redis.Get(ctx, key).Bytes()
    if err == nil {
        var user User
        json.Unmarshal(data, &user)
        return &user, nil
    }

    // Cache miss
    user, err := db.GetUser(id)
    if err != nil {
        return nil, err
    }

    // Cache for 5 minutes
    data, _ := json.Marshal(user)
    redis.Set(ctx, key, data, 5*time.Minute)

    return user, nil
}
```

**Cache invalidation:**
```go
func UpdateUser(ctx context.Context, user *User) error {
    // Update database
    if err := db.UpdateUser(user); err != nil {
        return err
    }

    // Invalidate cache
    key := fmt.Sprintf("user:%d", user.ID)
    redis.Del(ctx, key)

    return nil
}
```

---

## API Performance

### Response Time Optimization

**1. Pagination:**
```go
type PaginatedResponse struct {
    Data  []Item `json:"data"`
    Meta  Meta   `json:"meta"`
}

type Meta struct {
    Page       int `json:"page"`
    PerPage    int `json:"per_page"`
    TotalItems int `json:"total_items"`
    TotalPages int `json:"total_pages"`
}

func GetItems(page, perPage int) (*PaginatedResponse, error) {
    // Limit per_page to prevent abuse
    if perPage > 100 {
        perPage = 100
    }

    offset := (page - 1) * perPage

    items, _ := db.Query(`
        SELECT * FROM items
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
    `, perPage, offset)

    total, _ := db.QueryRow("SELECT COUNT(*) FROM items")

    return &PaginatedResponse{
        Data: items,
        Meta: Meta{
            Page:       page,
            PerPage:    perPage,
            TotalItems: total,
            TotalPages: (total + perPage - 1) / perPage,
        },
    }, nil
}
```

**2. Field selection:**
```go
// Allow clients to request specific fields
// GET /api/users?fields=id,name,email

func GetUsers(fields []string) ([]map[string]interface{}, error) {
    allowedFields := map[string]bool{
        "id": true, "name": true, "email": true, "created_at": true,
    }

    // Validate and build SELECT clause
    selectFields := []string{}
    for _, f := range fields {
        if allowedFields[f] {
            selectFields = append(selectFields, f)
        }
    }

    if len(selectFields) == 0 {
        selectFields = []string{"id", "name", "email"}  // Default
    }

    query := fmt.Sprintf("SELECT %s FROM users", strings.Join(selectFields, ", "))
    // ...
}
```

**3. Compression:**
```go
import "github.com/go-chi/chi/middleware"

router := chi.NewRouter()
router.Use(middleware.Compress(5))  // gzip compression level 5
```

### Async Processing

Move slow operations out of the request cycle:

```go
// ❌ Synchronous - slow response
func CreateOrder(w http.ResponseWriter, r *http.Request) {
    order := createOrder(r)

    sendConfirmationEmail(order)      // 500ms
    updateInventory(order)            // 200ms
    notifyWarehouse(order)            // 300ms

    respondJSON(w, http.StatusCreated, order)
    // Total: 1000ms+
}

// ✅ Async - fast response
func CreateOrder(w http.ResponseWriter, r *http.Request) {
    order := createOrder(r)

    // Queue background tasks
    queue.Publish("order.created", order)

    respondJSON(w, http.StatusCreated, order)
    // Total: ~100ms
}

// Background worker handles slow tasks
func ProcessOrderCreated(order Order) {
    sendConfirmationEmail(order)
    updateInventory(order)
    notifyWarehouse(order)
}
```

---

## Frontend Performance

### Bundle Size Optimization

**1. Code splitting:**
```javascript
// ❌ Everything in one bundle
import { Dashboard } from './Dashboard';
import { Settings } from './Settings';
import { Admin } from './Admin';

// ✅ Lazy load routes
const Dashboard = React.lazy(() => import('./Dashboard'));
const Settings = React.lazy(() => import('./Settings'));
const Admin = React.lazy(() => import('./Admin'));

function App() {
    return (
        <Suspense fallback={<Loading />}>
            <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="/admin" element={<Admin />} />
            </Routes>
        </Suspense>
    );
}
```

**2. Tree shaking:**
```javascript
// ❌ Import entire library
import _ from 'lodash';
const result = _.map(items, 'name');

// ✅ Import only what you need
import map from 'lodash/map';
const result = map(items, 'name');
```

**3. Analyze bundle:**
```bash
# Webpack bundle analyzer
npm install webpack-bundle-analyzer
npx webpack-bundle-analyzer dist/stats.json

# Vite
npm run build -- --stats
```

### Image Optimization

```javascript
// Use responsive images
<img
    src="/image-400.jpg"
    srcset="
        /image-400.jpg 400w,
        /image-800.jpg 800w,
        /image-1200.jpg 1200w
    "
    sizes="(max-width: 600px) 400px, (max-width: 900px) 800px, 1200px"
    loading="lazy"
    alt="Description"
/>

// Or use Next.js Image component
import Image from 'next/image';

<Image
    src="/image.jpg"
    width={800}
    height={600}
    alt="Description"
    placeholder="blur"
/>
```

### Virtual Scrolling

For long lists (100+ items):

```javascript
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
    const Row = ({ index, style }) => (
        <div style={style}>
            {items[index].name}
        </div>
    );

    return (
        <FixedSizeList
            height={400}
            itemCount={items.length}
            itemSize={50}
            width="100%"
        >
            {Row}
        </FixedSizeList>
    );
}
```

---

## Monitoring & Profiling

### Application Metrics

```go
import "github.com/prometheus/client_golang/prometheus"

var (
    requestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration",
            Buckets: []float64{.01, .05, .1, .25, .5, 1, 2.5, 5},
        },
        []string{"method", "path", "status"},
    )

    requestCount = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "path", "status"},
    )
)

func MetricsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        // Wrap response writer to capture status
        ww := &responseWriter{ResponseWriter: w, status: 200}
        next.ServeHTTP(ww, r)

        duration := time.Since(start).Seconds()
        labels := prometheus.Labels{
            "method": r.Method,
            "path":   r.URL.Path,
            "status": strconv.Itoa(ww.status),
        }

        requestDuration.With(labels).Observe(duration)
        requestCount.With(labels).Inc()
    })
}
```

### Profiling Go Applications

```go
import _ "net/http/pprof"

func main() {
    // pprof endpoints available at /debug/pprof/
    go http.ListenAndServe(":6060", nil)

    // Your application
    startServer()
}
```

```bash
# CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Memory profile
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine profile
go tool pprof http://localhost:6060/debug/pprof/goroutine
```

### Performance Testing

```bash
# Load testing with hey
hey -n 10000 -c 100 http://localhost:8080/api/users

# Output:
# Summary:
#   Total:        5.2341 secs
#   Slowest:      0.5234 secs
#   Fastest:      0.0012 secs
#   Average:      0.0523 secs
#   Requests/sec: 1910.5234
```

---

## Prompting Claude for Performance

**For database optimization:**
```
Optimize this database query for performance:
[paste query]

Context:
- Table has 1M+ rows
- Query runs frequently (100+ times/minute)
- Current execution time: 500ms

Please:
1. Analyze the query plan
2. Suggest appropriate indexes
3. Rewrite the query if needed
4. Estimate improvement
```

**For API performance:**
```
This API endpoint is slow (2s average response):
[paste handler code]

Please:
1. Identify performance bottlenecks
2. Suggest N+1 query fixes
3. Add caching where appropriate
4. Consider async processing for slow operations

Target: < 200ms response time
```

---

## Performance Checklist

### Database
- [ ] Queries have appropriate indexes
- [ ] No N+1 query patterns
- [ ] Large result sets are paginated
- [ ] Connection pooling is configured
- [ ] Slow queries are logged and monitored

### API
- [ ] Response times are monitored
- [ ] Large responses use pagination
- [ ] Compression is enabled
- [ ] Slow operations are async
- [ ] Caching is used for frequent reads

### Frontend
- [ ] Bundle size is monitored
- [ ] Routes are code-split
- [ ] Images are optimized and lazy-loaded
- [ ] Long lists use virtualization
- [ ] Core Web Vitals meet targets

---

**Prev:** [Security Practices](./15-security.md) | **Next:** [CI/CD and Deployment](./17-ci-cd.md)
