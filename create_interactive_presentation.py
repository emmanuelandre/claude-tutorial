#!/usr/bin/env python3
"""
Generate comprehensive interactive Claude Code tutorial presentation
All examples use React (frontend) and Go (backend)
"""

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
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

def create_hands_on_slide(story, styles, title, prompt, expected_result):
    """Hands-on exercise slide"""
    slide_title = Paragraph(f'<font color="#003E7E" size="28"><b>🔨 Hands-On: {title}</b></font>', styles['Heading1'])
    story.append(slide_title)
    story.append(Spacer(1, 0.3*inch))

    # Instruction
    instruction = Paragraph('<font color="#0076CE" size="16"><b>YOUR PROMPT:</b></font>', styles['BodyText'])
    story.append(instruction)
    story.append(Spacer(1, 0.15*inch))

    # Prompt box
    prompt_text = Paragraph(f'<font color="#5B5B5B" size="12" face="Courier">{prompt}</font>',
                           ParagraphStyle('Code', parent=styles['BodyText'], leftIndent=20, backColor=LIGHT_GRAY))
    story.append(prompt_text)
    story.append(Spacer(1, 0.25*inch))

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
    story.append(Spacer(1, 0.2*inch))

    lang_label = Paragraph(f'<font color="#0076CE" size="12"><b>{language}</b></font>', styles['BodyText'])
    story.append(lang_label)
    story.append(Spacer(1, 0.1*inch))

    # Code in monospace
    code_lines = code.split('\n')
    for line in code_lines[:20]:  # Limit to 20 lines
        code_p = Paragraph(f'<font color="#5B5B5B" size="9" face="Courier">{line}</font>', styles['BodyText'])
        story.append(code_p)
        story.append(Spacer(1, 0.05*inch))

    story.append(PageBreak())

def create_two_column_slide(story, styles, title, left_title, left_items, right_title, right_items):
    """Two-column comparison slide"""
    slide_title = Paragraph(f'<font color="#003E7E" size="28"><b>{title}</b></font>', styles['Heading1'])
    story.append(slide_title)
    story.append(Spacer(1, 0.3*inch))

    left_content = f'<font color="#0076CE" size="16"><b>{left_title}</b></font><br/><br/>'
    for item in left_items:
        left_content += f'<font color="#5B5B5B" size="12">✓ {item}</font><br/><br/>'

    right_content = f'<font color="#0076CE" size="16"><b>{right_title}</b></font><br/><br/>'
    for item in right_items:
        right_content += f'<font color="#5B5B5B" size="12">• {item}</font><br/><br/>'

    data = [[
        Paragraph(left_content, styles['BodyText']),
        Paragraph(right_content, styles['BodyText'])
    ]]

    table = Table(data, colWidths=[4.5*inch, 4.5*inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))

    story.append(table)
    story.append(PageBreak())

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

    # TITLE
    create_title_slide(story, styles)

    # AGENDA
    create_content_slide(story, styles, "Workshop Agenda", [
        "Part 1: Philosophy & Foundation",
        "Part 2: Getting Started Hands-On",
        "Part 3: Core Workflow (Interactive)",
        "Part 4: Testing Strategy (Live Demo)",
        "Part 5: Real-World Application",
        "Part 6: Q&A and Practice"
    ])

    # =================
    # PART 1: PHILOSOPHY
    # =================
    create_section_slide(story, styles, "Part 1: Philosophy & Foundation")

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

    create_content_slide(story, styles, "Core Development Philosophy", [
        ("API-First Development:", [
            "Specifications drive implementation",
            "Database schema → API contracts → UI components",
            "E2E tests validate complete user journeys"
        ]),
        ("Micro-Teams of 2:", [
            "1 human + Claude = redundancy without overhead",
            "Each team owns end-to-end features",
            "Parallel development without bottlenecks"
        ]),
        ("Zero External Dependencies:", [
            "Be your own QA engineer",
            "Be your own DevOps engineer",
            "Own the entire vertical slice"
        ])
    ])

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

    # =================
    # PART 2: GETTING STARTED
    # =================
    create_section_slide(story, styles, "Part 2: Getting Started")

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

    create_hands_on_slide(story, styles, "Create Your First Project",
        """mkdir my-api-project
cd my-api-project
git init

# Now ask Claude:
"Help me create a CLAUDE.md file for a Go API project with:
- PostgreSQL database
- JWT authentication
- RESTful endpoints
- Docker deployment

Follow the template structure from github.com/emmanuelandre/claude-tutorial"
""",
        "Claude will create a complete CLAUDE.md with your project structure, conventions, and commands"
    )

    create_content_slide(story, styles, "The CLAUDE.md File", [
        "Your project's instruction manual for Claude",
        "Persists context across ALL sessions",
        ("Essential sections:", [
            "Philosophy & team structure",
            "Architecture diagram",
            "Tech stack (Go, React, PostgreSQL, NATS)",
            "Git workflow and commit format",
            "Pre-commit checks (mandatory)",
            "Code patterns and conventions"
        ]),
        "Update it as your project evolves"
    ])

    create_hands_on_slide(story, styles, "Verify Your CLAUDE.md",
        """"Read my CLAUDE.md and summarize:
1. What tech stack am I using?
2. What's my git workflow?
3. What checks must pass before committing?
4. What's my testing strategy?"
""",
        "Claude should accurately describe all your conventions from CLAUDE.md"
    )

    # =================
    # PART 3: CORE WORKFLOW
    # =================
    create_section_slide(story, styles, "Part 3: AI-First Workflow")

    create_content_slide(story, styles, "The 10-Step Process", [
        "1. Human: Write detailed specification",
        "2. AI: Design database schema → Human: Review",
        "3. AI: Implement repository layer (Go) → Human: Review",
        "4. AI: Create API endpoints (Go) → Human: Review",
        "5. AI: Write API E2E tests (Cypress) → Human: Verify pass",
        "6. AI: Build React components → Human: Review",
        "7. AI: Write UI E2E tests (Cypress) → Human: Verify pass",
        "8. AI: Update documentation → Human: Review",
        "9. Human: Conduct security & code review",
        "10. AI: Execute deployment → Human: Verify"
    ])

    create_hands_on_slide(story, styles, "Step 1 - Write Specification",
        """"I need to implement user profile editing. Please help me plan:

Requirements:
- Users can update name, email, bio, avatar
- Email must be unique and validated
- Changes persist to PostgreSQL
- Show success/error messages in React UI

Before implementing:
1. What database changes do we need?
2. What API endpoints are required?
3. What security considerations?
4. What edge cases to handle?"
""",
        "Claude provides detailed implementation plan with DB schema, endpoints, security measures, and edge cases"
    )

    create_hands_on_slide(story, styles, "Step 2 - Database Schema",
        """"Create PostgreSQL migration for user profile updates:
- Add bio TEXT column
- Add avatar_url VARCHAR(500) column
- Add email_verified BOOLEAN
- Follow our naming conventions from CLAUDE.md"
""",
        "Claude creates migration files (up.sql and down.sql) following your project patterns"
    )

    create_code_slide(story, styles, "Example: Migration Output", "SQL",
"""-- migrations/003_user_profile.up.sql
ALTER TABLE users
  ADD COLUMN bio TEXT,
  ADD COLUMN avatar_url VARCHAR(500),
  ADD COLUMN email_verified BOOLEAN DEFAULT FALSE,
  ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();

CREATE INDEX idx_users_email ON users(email)
  WHERE deleted_at IS NULL;

-- migrations/003_user_profile.down.sql
ALTER TABLE users
  DROP COLUMN bio,
  DROP COLUMN avatar_url,
  DROP COLUMN email_verified;
""")

    create_hands_on_slide(story, styles, "Step 3 - Repository Layer",
        """"Implement Go repository methods for user profile:
- UpdateProfile(ctx, userID, data)
- UpdateEmail(ctx, userID, newEmail) - check uniqueness
- GetProfile(ctx, userID)

Use database/sql with prepared statements.
Follow the Handler → Repository pattern from CLAUDE.md"
""",
        "Claude creates repository methods with proper error handling, SQL injection prevention, and context support"
    )

    create_code_slide(story, styles, "Example: Go Repository", "Go",
"""// internal/repository/user_repository.go
func (r *UserRepository) UpdateProfile(
    ctx context.Context,
    userID int,
    data UpdateProfileData,
) (*User, error) {
    query := `
        UPDATE users
        SET name = $1, bio = $2, avatar_url = $3, updated_at = NOW()
        WHERE id = $4 AND deleted_at IS NULL
        RETURNING id, email, name, bio, avatar_url
    `

    var user User
    err := r.db.QueryRowContext(ctx, query,
        data.Name, data.Bio, data.AvatarURL, userID,
    ).Scan(&user.ID, &user.Email, &user.Name,
           &user.Bio, &user.AvatarURL)

    if err == sql.ErrNoRows {
        return nil, ErrNotFound
    }
    return &user, err
}
""")

    create_hands_on_slide(story, styles, "Step 4 - API Endpoints",
        """"Create Go API endpoint for profile update:
- PUT /api/v1/users/:id/profile
- Require JWT authentication
- Check user can only update their own profile
- Validate all inputs
- Return 200 with updated user or 400/403 on error

Use gorilla/mux for routing."
""",
        "Claude creates handler with auth middleware, validation, and proper error responses"
    )

    create_code_slide(story, styles, "Example: Go HTTP Handler", "Go",
"""// internal/handlers/user_handler.go
func (h *UserHandler) UpdateProfile(w http.ResponseWriter, r *http.Request) {
    userID := r.Context().Value("user_id").(int)
    targetID, _ := strconv.Atoi(mux.Vars(r)["id"])

    // Authorization check
    if userID != targetID {
        respondError(w, http.StatusForbidden,
            "Cannot update another user's profile")
        return
    }

    var data UpdateProfileData
    if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
        respondError(w, http.StatusBadRequest, "Invalid request")
        return
    }

    user, err := h.repo.UpdateProfile(r.Context(), userID, data)
    if err != nil {
        respondError(w, http.StatusInternalServerError,
            "Failed to update profile")
        return
    }

    respondJSON(w, http.StatusOK, user)
}
""")

    create_hands_on_slide(story, styles, "Step 5 - API E2E Tests",
        """"Write Cypress E2E tests for profile update API:
- Test successful profile update
- Test 403 when updating another user
- Test 400 for invalid email format
- Test 409 for duplicate email
- Test 401 without auth token

Save in tests/e2e/api/user-profile.cy.js"
""",
        "Claude creates comprehensive Cypress tests covering all scenarios"
    )

    create_code_slide(story, styles, "Example: Cypress API Test", "JavaScript",
"""// tests/e2e/api/user-profile.cy.js
describe('API: User Profile', () => {
  let authToken, userId

  before(() => {
    cy.request('POST', '/api/v1/auth/login', {
      email: 'test@example.com',
      password: 'TestPass123!'
    }).then((res) => {
      authToken = res.body.token
      userId = res.body.user.id
    })
  })

  it('updates profile successfully', () => {
    cy.request({
      method: 'PUT',
      url: `/api/v1/users/${userId}/profile`,
      headers: { Authorization: `Bearer ${authToken}` },
      body: {
        name: 'Updated Name',
        bio: 'New bio text'
      }
    }).then((res) => {
      expect(res.status).to.eq(200)
      expect(res.body.name).to.eq('Updated Name')
    })
  })
})
""")

    create_hands_on_slide(story, styles, "Step 6 - React Components",
        """"Create React component for profile editing:
- Use React Hook Form for validation
- Make PUT request to API
- Show loading state during save
- Display success/error messages
- Optimistic UI updates
- Use Zustand for state if needed

Create in src/components/ProfileEditor.jsx"
""",
        "Claude creates React component with form validation, API integration, and proper error handling"
    )

    create_code_slide(story, styles, "Example: React Component", "JavaScript (React)",
"""// src/components/ProfileEditor.jsx
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { api } from '../api/client'

export function ProfileEditor({ user }) {
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      name: user.name,
      bio: user.bio || ''
    }
  })

  const onSubmit = async (data) => {
    setLoading(true)
    try {
      await api.updateProfile(user.id, data)
      setMessage({ type: 'success', text: 'Profile updated!' })
    } catch (error) {
      setMessage({ type: 'error', text: error.message })
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  )
}
""")

    create_hands_on_slide(story, styles, "Step 7 - UI E2E Tests",
        """"Write Cypress UI E2E tests for profile editing:
- Test user can update their profile
- Test form validation (required fields)
- Test error message display
- Test success message display
- Test loading state visibility

Use data-test attributes for selectors."
""",
        "Claude creates UI tests that verify the complete user journey in the browser"
    )

    create_code_slide(story, styles, "Example: Cypress UI Test", "JavaScript",
"""// tests/e2e/ui/profile.cy.js
describe('UI: Profile Editing', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'TestPass123!')
    cy.visit('/profile/edit')
  })

  it('updates profile successfully', () => {
    cy.get('[data-test="name-input"]')
      .clear()
      .type('New Name')

    cy.get('[data-test="bio-input"]')
      .type('My new bio')

    cy.get('[data-test="save-button"]').click()

    cy.get('[data-test="success-message"]')
      .should('be.visible')
      .and('contain', 'Profile updated')

    // Verify persistence
    cy.reload()
    cy.get('[data-test="name-input"]')
      .should('have.value', 'New Name')
  })
})
""")

    # =================
    # PART 4: TESTING
    # =================
    create_section_slide(story, styles, "Part 4: Testing Strategy")

    create_content_slide(story, styles, "E2E First Philosophy", [
        "Inverted testing pyramid: E2E tests are primary",
        ("Why E2E first?", [
            "Test actual user flows",
            "Catch integration issues",
            "Verify the whole system",
            "Enable confident refactoring"
        ]),
        "Component tests: Only for complex UI logic",
        "Unit tests: Optional - only for critical algorithms",
        "Measure effectiveness, don't assume value"
    ])

    create_hands_on_slide(story, styles, "Write Your First E2E Test",
        """"Write a Cypress E2E test for user login:
1. Visit /login page
2. Enter email and password
3. Click login button
4. Verify redirect to /dashboard
5. Verify JWT token in localStorage
6. Verify welcome message visible

Use data-test attributes for selectors."
""",
        "Claude creates a complete E2E test covering the entire login flow"
    )

    create_content_slide(story, styles, "E2E Testing Best Practices", [
        "Test user journeys, not implementation details",
        "Use stable data-test attributes, never CSS selectors",
        ("Coverage priorities:", [
            "Happy path - must always pass",
            "Critical failures - auth, permissions, validation",
            "Edge cases - boundary conditions",
            "Error scenarios - network failures"
        ]),
        "Separate API and UI E2E tests",
        "Create reusable test commands"
    ])

    create_hands_on_slide(story, styles, "Create Reusable Test Commands",
        """"Create Cypress custom commands for:
1. cy.login(email, password) - Login and store token
2. cy.createUser(userData) - Create user via API
3. cy.deleteUser(userId) - Clean up test data

Save in cypress/support/commands.js"
""",
        "Claude creates reusable commands that simplify your test code"
    )

    create_code_slide(story, styles, "Example: Cypress Commands", "JavaScript",
"""// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.request({
    method: 'POST',
    url: '/api/v1/auth/login',
    body: { email, password }
  }).then((response) => {
    window.localStorage.setItem('token', response.body.token)
    window.localStorage.setItem('user',
      JSON.stringify(response.body.user))
  })
})

Cypress.Commands.add('createUser', (userData) => {
  return cy.request({
    method: 'POST',
    url: '/api/v1/users',
    headers: {
      Authorization: `Bearer ${Cypress.env('adminToken')}`
    },
    body: userData
  })
})

// Usage in tests
beforeEach(() => {
  cy.login('test@example.com', 'TestPass123!')
  cy.visit('/dashboard')
})
""")

    # =================
    # PART 5: BEST PRACTICES
    # =================
    create_section_slide(story, styles, "Part 5: Best Practices")

    create_content_slide(story, styles, "Git Workflow Standards", [
        ("Branch naming: <type>/<description>", [
            "feature/, fix/, refactor/, docs/, test/"
        ]),
        ("Conventional commits: <type>(scope): subject", [
            "feat, fix, refactor, docs, test, chore"
        ]),
        ("HARD RULES - never break:", [
            "Never commit directly to main",
            "Never merge without review",
            "Never commit code that fails tests",
            "Pre-commit checks MUST pass"
        ])
    ])

    create_hands_on_slide(story, styles, "Practice: Create Feature Branch",
        """"Help me create a feature branch for adding password reset:
1. What should I name the branch?
2. What pre-commit checks do I need to run?
3. What should my commit message be?
4. How do I create the PR?"
""",
        "Claude provides step-by-step git workflow commands following your conventions"
    )

    create_content_slide(story, styles, "Pre-Commit Checks (Mandatory)", [
        ("Backend (Go):", [
            "go fmt ./... (format code)",
            "go test -v -race ./... (run tests)",
            "go build ./... (verify builds)",
            "golangci-lint run (if installed)"
        ]),
        ("Frontend (React):", [
            "npm run lint (ESLint)",
            "npm run build (Vite build)"
        ]),
        ("E2E Tests:", [
            "npm run test:e2e (all tests must pass)"
        ]),
        "DO NOT commit if ANY check fails!"
    ])

    create_hands_on_slide(story, styles, "Run Pre-Commit Checks",
        """"I've made changes to my Go API. Walk me through the pre-commit checks:
1. Show me exact commands to run
2. What does each check verify?
3. What do I do if a check fails?
4. When can I commit?"
""",
        "Claude provides exact command sequence with explanations for each check"
    )

    create_content_slide(story, styles, "Prompt Engineering Tips", [
        "Be specific, not vague - include exact requirements",
        "Provide context - architecture, patterns, constraints",
        "Include examples - API contracts, expected behavior",
        ("Multi-step requests:", [
            "Break complex features into clear steps",
            "Define validation criteria for each step",
            "Request tests and documentation explicitly"
        ]),
        "Reference existing code patterns for consistency"
    ])

    create_hands_on_slide(story, styles, "Practice: Good vs Bad Prompts",
        """BAD: "Add user authentication"

GOOD: "Implement JWT authentication for my Go API:
- POST /api/v1/auth/login endpoint
- Accept email and password
- Return JWT token valid for 15 minutes
- Include refresh token valid for 7 days
- Use bcrypt for password hashing (10 rounds)
- Follow the handler pattern from CLAUDE.md
- Include comprehensive E2E tests"
""",
        "Claude implements exactly what you specified vs. making assumptions with vague prompts"
    )

    # =================
    # PART 6: REAL WORLD
    # =================
    create_section_slide(story, styles, "Part 6: Real-World Application")

    create_content_slide(story, styles, "Common Patterns", [
        ("API Layer (Go):", [
            "Route → Handler → Repository pattern",
            "Middleware for auth, CORS, logging",
            "Prepared statements prevent SQL injection",
            "Context for cancellation and timeouts"
        ]),
        ("Frontend (React):", [
            "Page → Container → Component pattern",
            "Zustand/Redux for state management",
            "React Query for API caching",
            "React Hook Form for validation"
        ])
    ])

    create_hands_on_slide(story, styles, "Exercise: Complete Feature",
        """NOW IT'S YOUR TURN!

Implement a complete "Add Comment" feature:

Specification:
- Users can add comments to posts
- Comments have: text (max 500 chars), user_id, post_id
- API: POST /api/v1/posts/:id/comments
- React component shows comment form
- Real-time update after submission

Ask Claude to:
1. Design database schema
2. Create Go repository and handler
3. Write API E2E tests
4. Build React component
5. Write UI E2E tests

Go through all 10 steps!
""",
        "Complete implementation with all tests passing and documentation updated"
    )

    create_content_slide(story, styles, "Debugging with Claude", [
        ("When you encounter errors:", [
            "Share exact error message and stack trace",
            "Describe what you were doing",
            "Show relevant code snippets",
            "Mention recent changes"
        ]),
        ("Claude can help:", [
            "Analyze error messages",
            "Review code for issues",
            "Suggest fixes with explanations",
            "Prevent similar issues in future"
        ])
    ])

    create_hands_on_slide(story, styles, "Practice: Debug an Issue",
        """"I'm getting this error when calling my API:

Error: connect ECONNREFUSED 127.0.0.1:8080

What I did:
1. Started my Go server with 'go run cmd/api/main.go'
2. Made request from React app
3. Got this error

Recent changes:
- Added new endpoint for comments
- Updated .env file

Help me debug this."
""",
        "Claude systematically debugs: checks if server is running, verifies port, checks CORS, reviews .env configuration"
    )

    create_content_slide(story, styles, "Keys to Success", [
        ("1. CLAUDE.md is essential", [
            "Keep it current and comprehensive",
            "Document all conventions and patterns"
        ]),
        ("2. Clear handoffs between AI and human", [
            "AI completes a step fully before handoff",
            "Human approves or requests changes"
        ]),
        ("3. E2E tests are non-negotiable", [
            "Write tests before considering feature complete",
            "Tests are your confidence for refactoring"
        ]),
        ("4. Iterate quickly", [
            "Start working, refine as you go",
            "Commit small, atomic changes"
        ])
    ])

    # SUMMARY
    create_section_slide(story, styles, "Summary & Next Steps")

    create_content_slide(story, styles, "What You Learned Today", [
        "AI-first development philosophy",
        "The 10-step systematic workflow",
        "E2E-first testing strategy",
        "Go backend + React frontend patterns",
        "Git workflow and quality gates",
        "Effective prompt engineering",
        "Real-world debugging techniques"
    ])

    create_content_slide(story, styles, "Your Action Plan", [
        ("This Week:", [
            "Create your project's CLAUDE.md",
            "Set up pre-commit checks",
            "Write your first E2E test"
        ]),
        ("This Month:", [
            "Implement one complete feature using 10-step workflow",
            "Build reusable test commands library",
            "Document your patterns and learnings"
        ]),
        ("Ongoing:", [
            "Measure your testing effectiveness",
            "Update CLAUDE.md as you learn",
            "Share knowledge with your team"
        ])
    ])

    create_content_slide(story, styles, "Resources", [
        ("Tutorial Repository:", [
            "github.com/emmanuelandre/claude-tutorial"
        ]),
        ("Documentation:", [
            "Complete CLAUDE.md template",
            "Step-by-step workflow guides",
            "Testing strategy guide",
            "Troubleshooting common issues"
        ]),
        ("Official Resources:", [
            "Claude Code: claude.ai/code",
            "Anthropic Docs: docs.anthropic.com"
        ])
    ])

    # FINAL SLIDE
    story.append(Spacer(1, 2*inch))
    thank_you = Paragraph('<font color="#003E7E" size="48"><b>Thank You!</b></font>', styles['Title'])
    story.append(thank_you)
    story.append(Spacer(1, 0.4*inch))

    questions = Paragraph('<font color="#5B5B5B" size="24">Questions & Practice Time</font>', styles['Title'])
    story.append(questions)
    story.append(Spacer(1, 0.3*inch))

    repo = Paragraph('<font color="#0076CE" size="16">github.com/emmanuelandre/claude-tutorial</font>', styles['Title'])
    story.append(repo)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print("✅ Interactive presentation created: claude-code-interactive-tutorial.pdf")

if __name__ == "__main__":
    create_presentation()
