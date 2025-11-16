#!/usr/bin/env python3
"""
Generate comprehensive interactive Claude Code tutorial presentation
All examples use React (frontend) and Go (backend)
Properly formatted prompts with line breaks
"""

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# 16:9 aspect ratio
PAGESIZE = (11.0 * inch, 6.1875 * inch)

# Color scheme
PRIMARY_BLUE = HexColor('#0076CE')
DARK_BLUE = HexColor('#003E7E')
LIGHT_BLUE = HexColor('#48B9E8')
DARK_GRAY = HexColor('#5B5B5B')
MED_GRAY = HexColor('#999999')
LIGHT_GRAY = HexColor('#E5E5E5')
WHITE = HexColor('#FFFFFF')
SUCCESS_GREEN = HexColor('#00B388')
WARNING_ORANGE = HexColor('#FF8300')

# Global list to collect all prompts
ALL_PROMPTS = []

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setStrokeColor(PRIMARY_BLUE)
        self.setLineWidth(2)
        self.line(0.5*inch, 0.4*inch, PAGESIZE[0] - 0.5*inch, 0.4*inch)

        self.setFont("Helvetica", 9)
        self.setFillColor(MED_GRAY)
        page = "Page %d of %d" % (self._pageNumber, page_count)
        self.drawRightString(PAGESIZE[0] - 0.5*inch, 0.25*inch, page)

def create_title_slide(story, styles):
    """Title slide"""
    story.append(Spacer(1, 1.5*inch))

    title = Paragraph('<font color="#003E7E" size="48"><b>Claude Code</b></font>', styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))

    subtitle = Paragraph('<font color="#0076CE" size="32">Interactive Tutorial & Workshop</font>', styles['Title'])
    story.append(subtitle)
    story.append(Spacer(1, 0.3*inch))

    desc = Paragraph('<font color="#5B5B5B" size="16">AI-First Development for Modern Software Teams</font>', styles['Title'])
    story.append(desc)
    story.append(Spacer(1, 0.5*inch))

    footer = Paragraph('<font color="#999999" size="12">https://github.com/emmanuelandre/claude-tutorial</font>', styles['Title'])
    story.append(footer)

    story.append(PageBreak())

def create_section_slide(story, styles, title):
    """Section divider slide"""
    story.append(Spacer(1, 1.8*inch))

    section_text = Paragraph(
        f'<font color="#FFFFFF" size="38"><b>{title}</b></font>',
        ParagraphStyle('SectionContent', parent=styles['Normal'], fontSize=38,
                      textColor=WHITE, alignment=TA_CENTER, leading=48,
                      spaceAfter=30, spaceBefore=30)
    )

    data = [[section_text]]
    table = Table(data, colWidths=[9.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY_BLUE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 40),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),
    ]))

    story.append(table)
    story.append(PageBreak())

def create_content_slide(story, styles, title, content_items):
    """Standard content slide"""
    slide_title = Paragraph(f'<font color="#003E7E" size="28"><b>{title}</b></font>', styles['Heading1'])
    story.append(slide_title)
    story.append(Spacer(1, 0.3*inch))

    for item in content_items:
        if isinstance(item, str):
            p = Paragraph(f'<font color="#5B5B5B" size="14">• {item}</font>', styles['BodyText'])
            story.append(p)
            story.append(Spacer(1, 0.15*inch))
        elif isinstance(item, tuple):
            p = Paragraph(f'<font color="#5B5B5B" size="14"><b>{item[0]}</b></font>', styles['BodyText'])
            story.append(p)
            story.append(Spacer(1, 0.1*inch))
            for sub in item[1]:
                sp = Paragraph(f'<font color="#666666" size="12">   ◦ {sub}</font>', styles['BodyText'])
                story.append(sp)
                story.append(Spacer(1, 0.08*inch))
            story.append(Spacer(1, 0.1*inch))

    story.append(PageBreak())

def create_hands_on_slide(story, styles, title, prompt, expected_result, page_num):
    """Hands-on exercise slide with properly formatted prompts"""
    # Store prompt for export
    ALL_PROMPTS.append({
        'page': page_num,
        'title': title,
        'prompt': prompt,
        'expected': expected_result
    })

    slide_title = Paragraph(f'<font color="#003E7E" size="28"><b>🔨 Hands-On: {title}</b></font>', styles['Heading1'])
    story.append(slide_title)
    story.append(Spacer(1, 0.2*inch))

    # Instruction
    instruction = Paragraph('<font color="#0076CE" size="16"><b>YOUR PROMPT (See prompts.md):</b></font>', styles['BodyText'])
    story.append(instruction)
    story.append(Spacer(1, 0.15*inch))

    # Format prompt with line breaks preserved
    prompt_html = prompt.replace('\n', '<br/>')

    # Prompt box with preformatted style
    prompt_para = Paragraph(
        f'<font color="#5B5B5B" size="10" face="Courier">{prompt_html}</font>',
        ParagraphStyle('PromptBox',
                      parent=styles['BodyText'],
                      leftIndent=20,
                      rightIndent=20,
                      backColor=LIGHT_GRAY,
                      spaceBefore=5,
                      spaceAfter=5,
                      leading=14)
    )
    story.append(prompt_para)
    story.append(Spacer(1, 0.2*inch))

    # Expected result
    result = Paragraph('<font color="#0076CE" size="14"><b>What You Should See:</b></font>', styles['BodyText'])
    story.append(result)
    story.append(Spacer(1, 0.1*inch))

    result_text = Paragraph(f'<font color="#5B5B5B" size="12">• {expected_result}</font>', styles['BodyText'])
    story.append(result_text)

    story.append(PageBreak())

def create_code_slide(story, styles, title, language, code):
    """Code example slide"""
    slide_title = Paragraph(f'<font color="#003E7E" size="24"><b>{title}</b></font>', styles['Heading1'])
    story.append(slide_title)
    story.append(Spacer(1, 0.25*inch))

    # Language label
    lang_label = Paragraph(f'<font color="#0076CE" size="12"><b>{language.upper()}</b></font>', styles['BodyText'])
    story.append(lang_label)
    story.append(Spacer(1, 0.1*inch))

    # Code with line breaks preserved
    code_html = code.replace('\n', '<br/>').replace(' ', '&nbsp;')
    code_para = Paragraph(
        f'<font color="#5B5B5B" size="9" face="Courier">{code_html}</font>',
        ParagraphStyle('CodeBox',
                      parent=styles['BodyText'],
                      leftIndent=15,
                      rightIndent=15,
                      backColor=LIGHT_GRAY,
                      spaceBefore=5,
                      spaceAfter=5,
                      leading=12)
    )
    story.append(code_para)
    story.append(PageBreak())

def export_prompts_to_markdown():
    """Export all prompts to prompts.md file"""
    with open('prompts.md', 'w') as f:
        f.write('# Claude Code Tutorial - Workshop Prompts\n\n')
        f.write('Copy and paste these prompts during the workshop exercises.\n\n')
        f.write('---\n\n')

        for item in ALL_PROMPTS:
            f.write(f'## Page {item["page"]}: {item["title"]}\n\n')
            f.write('**PROMPT:**\n```\n')
            f.write(item['prompt'])
            f.write('\n```\n\n')
            f.write(f'**EXPECTED RESULT:**\n')
            f.write(f'{item["expected"]}\n\n')
            f.write('---\n\n')

def create_presentation():
    """Generate the complete interactive presentation"""
    doc = SimpleDocTemplate(
        "claude-code-interactive-tutorial.pdf",
        pagesize=PAGESIZE,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.7*inch,
        bottomMargin=0.7*inch
    )

    styles = getSampleStyleSheet()
    story = []
    page_num = 1

    # TITLE
    create_title_slide(story, styles)
    page_num += 1

    # AGENDA
    create_content_slide(story, styles, "Workshop Agenda", [
        "Part 1: Philosophy & Foundation",
        "Part 2: Getting Started Hands-On",
        "Part 3: Core Workflow (Interactive)",
        "Part 4: Testing Strategy (Live Demo)",
        "Part 5: Best Practices",
        "Part 6: Real-World Application"
    ])
    page_num += 1

    # =================
    # PART 1: PHILOSOPHY
    # =================
    create_section_slide(story, styles, "Part 1: Philosophy & Foundation")
    page_num += 1

    create_content_slide(story, styles, "The AI-First Philosophy", [
        "Traditional: Human writes code → AI assists",
        "AI-First: AI executes 100% → Human validates 100%",
        ("This means:", [
            "AI handles ALL coding, testing, documentation",
            "Human handles ALL validation, review, decisions",
            "Clear handoff points at each step",
            "Systematic quality gates"
        ])
    ])
    page_num += 1

    create_content_slide(story, styles, "Core Development Philosophy", [
        ("API-First Development:", [
            "Specifications drive implementation",
            "Database schema → API contracts → UI components",
            "E2E tests validate complete user journeys"
        ]),
        ("Micro-Teams of 2:", [
            "2 humans + Claude Code = redundancy without overhead",
            "Each team owns end-to-end features",
            "Parallel development without bottlenecks"
        ]),
        ("Zero External Dependencies:", [
            "Be your own QA engineer",
            "Be your own DevOps engineer",
            "Own the entire vertical slice"
        ])
    ])
    page_num += 1

    create_content_slide(story, styles, "Testing Philosophy", [
        "E2E tests are MANDATORY (API + UI user journeys)",
        "Unit tests are MANDATORY (business logic, utilities, edge cases)",
        "Component tests are GOOD TO HAVE (test containers for microservices)",
        ("Test-First Approach:", [
            "Define coverage targets before implementation",
            "Build testing infrastructure/framework first",
            "Track coverage from unit, component, and E2E tests",
            "Coverage thresholds vary by project (higher is better)",
            "Tests are your regression safety net"
        ]),
        "Measure coverage to ensure quality and confidence"
    ])
    page_num += 1

    # =================
    # PART 2: GETTING STARTED
    # =================
    create_section_slide(story, styles, "Part 2: Getting Started")
    page_num += 1

    create_content_slide(story, styles, "What You Need", [
        "Git 2.x or higher",
        "Code editor (VS Code, Cursor)",
        "Claude Code access (claude.ai/code)",
        ("Language-specific tools:", [
            "Go 1.21+ for backend",
            "Node.js 18+ (via nvm) for React",
            "Docker for deployment"
        ]),
        "GitHub CLI (gh) for PR management"
    ])
    page_num += 1

    create_hands_on_slide(story, styles, "Create Your First Project",
"""mkdir my-api-project
cd my-api-project
git init

# Now ask Claude:
Help me create a CLAUDE.md file for a Go API project with:
- PostgreSQL database
- JWT authentication
- RESTful endpoints
- Docker deployment

Include project structure, git workflow, and testing strategy.""",
        "Claude creates a comprehensive CLAUDE.md with architecture, commands, and conventions",
        page_num)
    page_num += 1

    create_hands_on_slide(story, styles, "Initialize Git Workflow",
"""Create feature branch and set up git workflow:
- Branch naming convention: feature/initial-setup
- Conventional commits enabled
- Pre-commit hooks for linting and testing

Follow the git workflow section in CLAUDE.md""",
        "Git repository with proper branch structure and commit conventions",
        page_num)
    page_num += 1

    # =================
    # PART 3: CORE WORKFLOW
    # =================
    create_section_slide(story, styles, "Part 3: AI-First Workflow")
    page_num += 1

    create_content_slide(story, styles, "The 10-Step Process", [
        "1. Specification (Human writes detailed spec)",
        "2. Database Schema (AI designs → Human reviews)",
        "3. Repository Layer (AI implements → Human reviews)",
        "4. API Endpoints (AI creates → Human reviews)",
        "5. API E2E Tests (AI writes → Human verifies)",
        "6. Frontend Components (AI builds → Human reviews)",
        "7. UI E2E Tests (AI creates → Human verifies)",
        "8. Documentation (AI updates → Human reviews)",
        "9. Code Review (Human conducts)",
        "10. Deployment (AI executes → Human verifies)"
    ])
    page_num += 1

    # Step 1: Specification
    create_hands_on_slide(story, styles, "Step 1 - Write Specification",
"""I need to implement user authentication for my API.

Requirements:
- Users register with email/password
- JWT tokens for authentication
- Password hashing with bcrypt
- Token refresh endpoint
- Logout (token invalidation)

Database:
- users table: id, email, password_hash, created_at, updated_at

API Endpoints:
POST /api/auth/register - Register new user
POST /api/auth/login - Login and get JWT
POST /api/auth/refresh - Refresh JWT token
POST /api/auth/logout - Invalidate token

Please create the database migration first.""",
        "Claude asks clarifying questions and confirms the specification",
        page_num)
    page_num += 1

    # Step 2: Database Schema
    create_code_slide(story, styles, "Expected: Database Migration (Go)", "sql",
"""-- migrations/001_create_users.up.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);""")
    page_num += 1

    create_hands_on_slide(story, styles, "Step 2 - Review Schema",
"""Review the migration file Claude created.

Check:
- Column types are appropriate
- Indexes are in place
- Constraints are correct

If approved, say: "Looks good, please proceed to repository layer"
If changes needed: "Change X to Y because..."

Run the migration:
psql -d mydb -f migrations/001_create_users.up.sql""",
        "Database table created successfully with proper indexes",
        page_num)
    page_num += 1

    # Step 3: Repository Layer
    create_code_slide(story, styles, "Expected: Repository Layer (Go)", "go",
"""// internal/repository/user.go
type UserRepository struct {
    db *sql.DB
}

func (r *UserRepository) Create(ctx context.Context, email, passwordHash string) (*User, error) {
    query := `INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email, created_at`
    var user User
    err := r.db.QueryRowContext(ctx, query, email, passwordHash).Scan(&user.ID, &user.Email, &user.CreatedAt)
    return &user, err
}

func (r *UserRepository) FindByEmail(ctx context.Context, email string) (*User, error) {
    query := `SELECT id, email, password_hash, created_at FROM users WHERE email = $1`
    var user User
    err := r.db.QueryRowContext(ctx, query, email).Scan(&user.ID, &user.Email, &user.PasswordHash, &user.CreatedAt)
    return &user, err
}""")
    page_num += 1

    # Step 4: API Endpoints
    create_hands_on_slide(story, styles, "Step 4 - Request API Implementation",
"""The repository layer looks good.

Now implement the API handlers:
1. POST /api/auth/register
   - Validate email format
   - Check password strength (min 8 chars)
   - Hash password with bcrypt
   - Return JWT token

2. POST /api/auth/login
   - Validate credentials
   - Compare password hash
   - Return JWT token

3. POST /api/auth/refresh
   - Validate existing token
   - Issue new token

Include error handling and proper HTTP status codes.""",
        "Claude creates handler files with validation and error handling",
        page_num)
    page_num += 1

    create_code_slide(story, styles, "Expected: API Handler (Go)", "go",
"""// internal/handlers/auth.go
func (h *AuthHandler) Register(w http.ResponseWriter, r *http.Request) {
    var req RegisterRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "Invalid request")
        return
    }

    // Validate
    if !isValidEmail(req.Email) {
        respondError(w, http.StatusBadRequest, "Invalid email")
        return
    }
    if len(req.Password) < 8 {
        respondError(w, http.StatusBadRequest, "Password too short")
        return
    }

    // Hash password
    hash, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
    if err != nil {
        respondError(w, http.StatusInternalServerError, "Failed to hash password")
        return
    }

    // Create user
    user, err := h.userRepo.Create(r.Context(), req.Email, string(hash))
    if err != nil {
        respondError(w, http.StatusConflict, "Email already exists")
        return
    }

    // Generate JWT
    token, err := h.jwtService.Generate(user.ID)
    respondJSON(w, http.StatusCreated, map[string]string{"token": token})
}""")
    page_num += 1

    # Step 5: API E2E Tests
    create_hands_on_slide(story, styles, "Step 5 - Request API Tests",
"""Create comprehensive E2E tests for the auth endpoints using Cypress.

Test cases:
1. Register - Happy path
2. Register - Duplicate email (409 error)
3. Register - Invalid email (400 error)
4. Register - Weak password (400 error)
5. Login - Valid credentials
6. Login - Invalid credentials (401 error)
7. Login - Non-existent user (401 error)
8. Refresh - Valid token
9. Refresh - Expired token (401 error)

Use Cypress API testing (cy.request)""",
        "Cypress test file created with all test cases",
        page_num)
    page_num += 1

    create_code_slide(story, styles, "Expected: E2E API Tests (Cypress)", "javascript",
"""// cypress/e2e/api/auth.cy.js
describe('API: Authentication', () => {
  it('registers new user successfully', () => {
    cy.request('POST', '/api/auth/register', {
      email: 'test@example.com',
      password: 'SecurePass123'
    })
    .then((response) => {
      expect(response.status).to.eq(201)
      expect(response.body).to.have.property('token')
    })
  })

  it('rejects duplicate email', () => {
    cy.request({
      method: 'POST',
      url: '/api/auth/register',
      body: { email: 'test@example.com', password: 'SecurePass123' },
      failOnStatusCode: false
    })
    .then((response) => {
      expect(response.status).to.eq(409)
    })
  })

  it('rejects weak password', () => {
    cy.request({
      method: 'POST',
      url: '/api/auth/register',
      body: { email: 'new@example.com', password: 'weak' },
      failOnStatusCode: false
    })
    .then((response) => {
      expect(response.status).to.eq(400)
    })
  })
})""")
    page_num += 1

    create_hands_on_slide(story, styles, "Run API Tests",
"""Run the API tests Claude created:

npx cypress run --spec "cypress/e2e/api/auth.cy.js"

Verify all tests pass.

If any fail, ask Claude:
"Test X is failing with error Y. Please investigate and fix.""",
        "All API tests pass (green checkmarks in terminal)",
        page_num)
    page_num += 1

    # Step 6: Frontend Components
    create_hands_on_slide(story, styles, "Step 6 - Request Frontend",
"""Now let's build the UI for authentication.

Create React components:
1. LoginForm component
   - Email and password inputs
   - Form validation
   - Submit calls /api/auth/login
   - Stores JWT in localStorage

2. RegisterForm component
   - Email, password, confirm password inputs
   - Client-side validation
   - Submit calls /api/auth/register
   - Auto-login after registration

Use React Hook Form for form handling and Zustand for auth state.""",
        "React components created with forms and state management",
        page_num)
    page_num += 1

    create_code_slide(story, styles, "Expected: Login Component (React)", "jsx",
"""// src/components/LoginForm.jsx
import { useForm } from 'react-hook-form'
import { useAuthStore } from '../stores/authStore'

export function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm()
  const login = useAuthStore(state => state.login)

  const onSubmit = async (data) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })

      if (!response.ok) throw new Error('Login failed')

      const { token } = await response.json()
      login(token) // Store in Zustand + localStorage
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('email', { required: true, pattern: /^[^@]+@[^@]+$/ })}
        placeholder="Email"
      />
      {errors.email && <span>Valid email required</span>}

      <input
        type="password"
        {...register('password', { required: true, minLength: 8 })}
        placeholder="Password"
      />
      {errors.password && <span>Password must be 8+ characters</span>}

      <button type="submit">Login</button>
    </form>
  )
}""")
    page_num += 1

    # Step 7: UI E2E Tests
    create_hands_on_slide(story, styles, "Step 7 - Request UI Tests",
"""Create UI E2E tests for the authentication flow.

Test scenarios:
1. User can register new account
2. User can login with valid credentials
3. User cannot login with invalid password
4. Form validation works (weak password, invalid email)
5. User stays logged in after page refresh
6. User can logout

Use data-test attributes for stable selectors.""",
        "Cypress UI test file created with user journey tests",
        page_num)
    page_num += 1

    create_code_slide(story, styles, "Expected: E2E UI Tests (Cypress)", "javascript",
"""// cypress/e2e/ui/auth.cy.js
describe('UI: Authentication Flow', () => {
  beforeEach(() => {
    cy.visit('/login')
  })

  it('registers and logs in new user', () => {
    // Register
    cy.get('[data-test="register-link"]').click()
    cy.get('[data-test="email-input"]').type('newuser@example.com')
    cy.get('[data-test="password-input"]').type('SecurePass123')
    cy.get('[data-test="submit-button"]').click()

    // Should redirect to dashboard
    cy.url().should('include', '/dashboard')
    cy.get('[data-test="user-email"]').should('contain', 'newuser@example.com')
  })

  it('shows validation errors for weak password', () => {
    cy.get('[data-test="password-input"]').type('weak')
    cy.get('[data-test="submit-button"]').click()
    cy.get('[data-test="error-message"]').should('contain', '8+ characters')
  })

  it('persists login after refresh', () => {
    // Login first
    cy.get('[data-test="email-input"]').type('test@example.com')
    cy.get('[data-test="password-input"]').type('SecurePass123')
    cy.get('[data-test="submit-button"]').click()

    // Refresh page
    cy.reload()

    // Still logged in
    cy.url().should('include', '/dashboard')
  })
})""")
    page_num += 1

    # =================
    # PART 4: TESTING STRATEGY
    # =================
    create_section_slide(story, styles, "Part 4: Testing Strategy")
    page_num += 1

    create_content_slide(story, styles, "E2E First Testing", [
        "Inverted testing pyramid: E2E tests are primary",
        ("Why E2E First?", [
            "Test actual user flows",
            "Catch integration issues",
            "Verify the whole system",
            "Enable confident refactoring"
        ]),
        "Component tests: Only for complex UI logic",
        "Unit tests: Optional - only for critical algorithms"
    ])
    page_num += 1

    create_hands_on_slide(story, styles, "Practice: Write E2E Test",
"""Write an E2E test for a password reset flow.

Feature requirements:
- User enters email on /forgot-password page
- System sends reset link to email
- User clicks link, enters new password
- User can login with new password

Create BOTH API and UI E2E tests for this flow.

Ask Claude to implement the feature + tests following the 10-step process.""",
        "Complete password reset feature with passing E2E tests",
        page_num)
    page_num += 1

    create_content_slide(story, styles, "Testing Best Practices", [
        "Test user journeys, not implementation details",
        "Use stable data-test attributes, not CSS selectors",
        ("Coverage priorities:", [
            "Happy path - must pass",
            "Critical failures - invalid inputs, permissions",
            "Edge cases - boundary conditions",
            "Error scenarios - network failures, timeouts"
        ]),
        "Separate API and UI E2E tests"
    ])
    page_num += 1

    # =================
    # PART 5: BEST PRACTICES
    # =================
    create_section_slide(story, styles, "Part 5: Best Practices")
    page_num += 1

    create_content_slide(story, styles, "Git Workflow Standards", [
        ("Branch naming: <type>/<description>", [
            "feature/, fix/, refactor/, docs/, test/, chore/"
        ]),
        ("Conventional commits: <type>(scope): subject", [
            "feat, fix, refactor, docs, test, chore, perf"
        ]),
        ("Hard rules:", [
            "Never commit directly to main",
            "Never merge without review",
            "Pre-commit checks MUST pass (lint, test, build)"
        ])
    ])
    page_num += 1

    create_hands_on_slide(story, styles, "Practice: Proper Git Workflow",
"""You've implemented the auth feature. Now create a proper PR.

Steps:
1. Review your changes: git status, git diff
2. Run pre-commit checks (lint, tests, build)
3. Commit with conventional format
4. Push branch
5. Create PR with description

Ask Claude:
"Please help me commit the auth feature and create a PR.
Run all pre-commit checks first.
Use conventional commit format.
Include a detailed PR description.""",
        "PR created with passing CI checks and proper commit messages",
        page_num)
    page_num += 1

    create_content_slide(story, styles, "Effective Prompt Engineering", [
        "Be specific, not vague",
        "Provide context - architecture, patterns, constraints",
        "Include examples - API contracts, expected behavior",
        ("Multi-step requests:", [
            "Break complex features into clear steps",
            "Define validation criteria",
            "Request tests explicitly"
        ]),
        "Reference existing patterns for consistency"
    ])
    page_num += 1

    create_hands_on_slide(story, styles, "Practice: Better Prompts",
"""Compare these two prompts:

❌ BAD:
"Add search to the users page"

✅ GOOD:
"Add search functionality to users page:
- Search input in page header
- Filter by email and name (case-insensitive)
- Debounce 300ms
- Update URL query params
- Clear button
- Show 'No results' when empty

Follow our existing search pattern from products page.
Include E2E test for search + clear + no results."

Practice: Write a detailed prompt for adding pagination.""",
        "You create a comprehensive, specific prompt with clear requirements",
        page_num)
    page_num += 1

    # =================
    # PART 6: REAL-WORLD APPLICATION
    # =================
    create_section_slide(story, styles, "Part 6: Real-World Application")
    page_num += 1

    create_content_slide(story, styles, "Keys to Success", [
        ("1. CLAUDE.md is essential", [
            "Keep it current and comprehensive",
            "Document all conventions and patterns"
        ]),
        ("2. Clear handoffs between AI and human", [
            "AI completes a step fully before handoff",
            "Human approves or requests changes"
        ]),
        ("3. Systematic quality gates", [
            "Tests must pass before proceeding",
            "Reviews must approve before merging"
        ])
    ])
    page_num += 1

    create_content_slide(story, styles, "Common Mistakes to Avoid", [
        "❌ Vague prompts → Be specific with examples",
        "❌ Skipping tests → Always write E2E tests first",
        "❌ Committing untested code → Run checks locally",
        "❌ Ignoring CLAUDE.md → Keep it updated",
        "❌ Large unfocused PRs → Make small, atomic changes",
        "✅ Review all AI output before committing",
        "✅ Use conventional commits",
        "✅ Run pre-commit checks"
    ])
    page_num += 1

    create_hands_on_slide(story, styles, "Final Exercise: Complete Feature",
"""Build a complete feature end-to-end:

Feature: User Profile Management
- View profile page showing user info
- Edit profile (name, email, avatar)
- Password change form
- Profile picture upload

Follow the full 10-step process:
1. Write specification (you)
2. Database schema (Claude → you review)
3. Repository layer (Claude → you review)
4. API endpoints (Claude → you review)
5. API E2E tests (Claude → you verify)
6. React components (Claude → you review)
7. UI E2E tests (Claude → you verify)
8. Documentation (Claude → you review)
9. Code review (you conduct)
10. Create PR (Claude → you merge)

Time limit: 30 minutes""",
        "Complete profile feature with passing tests and PR ready for review",
        page_num)
    page_num += 1

    # =================
    # SUMMARY
    # =================
    create_section_slide(story, styles, "Summary & Action Plan")
    page_num += 1

    create_content_slide(story, styles, "What We Learned", [
        "✓ AI-First philosophy: AI executes, Human validates",
        "✓ 10-step systematic development process",
        "✓ E2E tests as primary testing strategy",
        "✓ Proper git workflow and conventional commits",
        "✓ Effective prompt engineering techniques",
        "✓ CLAUDE.md as project instruction manual",
        "✓ Quality gates at every step"
    ])
    page_num += 1

    create_content_slide(story, styles, "Your Action Plan", [
        ("Next Steps:", [
            "1. Create CLAUDE.md for your project",
            "2. Set up git workflow (branches, conventional commits)",
            "3. Start with one feature using 10-step process",
            "4. Write E2E tests for everything",
            "5. Review and iterate"
        ]),
        ("Resources:", [
            "Tutorial: github.com/emmanuelandre/claude-tutorial",
            "Claude Code: claude.ai/code",
            "Prompts: See prompts.md file"
        ])
    ])
    page_num += 1

    # Thank You
    story.append(Spacer(1, 2*inch))
    thank_you = Paragraph('<font color="#003E7E" size="48"><b>Thank You!</b></font>', styles['Title'])
    story.append(thank_you)
    story.append(Spacer(1, 0.4*inch))

    questions = Paragraph('<font color="#5B5B5B" size="24">Questions?</font>', styles['Title'])
    story.append(questions)
    story.append(Spacer(1, 0.3*inch))

    repo = Paragraph('<font color="#0076CE" size="16">github.com/emmanuelandre/claude-tutorial</font>', styles['Title'])
    story.append(repo)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Interactive presentation created: claude-code-interactive-tutorial.pdf")

    # Export prompts
    export_prompts_to_markdown()
    print(f"✅ Prompts exported to: prompts.md")

if __name__ == "__main__":
    create_presentation()
