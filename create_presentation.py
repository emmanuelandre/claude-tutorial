#!/usr/bin/env python3
"""
Generate a professional slide deck for Claude Code Tutorial
Using modern design system colors (inspired by professional tech brands)
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# 16:9 aspect ratio page size
PAGESIZE = (11.0 * inch, 6.1875 * inch)  # 16:9 ratio

# Professional Blue Color Scheme
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
        # Footer line
        self.setStrokeColor(PRIMARY_BLUE)
        self.setLineWidth(2)
        self.line(0.5*inch, 0.4*inch, PAGESIZE[0] - 0.5*inch, 0.4*inch)

        # Page number
        self.setFont("Helvetica", 9)
        self.setFillColor(MED_GRAY)
        page = "Page %d of %d" % (self._pageNumber, page_count)
        self.drawRightString(PAGESIZE[0] - 0.5*inch, 0.25*inch, page)

def create_title_slide(story, styles):
    """Title slide"""
    story.append(Spacer(1, 1.5*inch))

    title = Paragraph(
        '<font color="#003E7E" size="48"><b>Claude Code</b></font>',
        styles['Title']
    )
    story.append(title)
    story.append(Spacer(1, 0.2*inch))

    subtitle = Paragraph(
        '<font color="#0076CE" size="32">Tutorial & Best Practices</font>',
        styles['Title']
    )
    story.append(subtitle)
    story.append(Spacer(1, 0.3*inch))

    desc = Paragraph(
        '<font color="#5B5B5B" size="16">AI-First Development for Modern Software Teams</font>',
        styles['Title']
    )
    story.append(desc)

    story.append(PageBreak())

def create_section_slide(story, styles, title):
    """Section divider slide with full blue background"""
    story.append(Spacer(1, 1.8*inch))

    # Create a table for the blue background section
    section_text = Paragraph(
        f'<font color="#FFFFFF" size="38"><b>{title}</b></font>',
        ParagraphStyle(
            'SectionContent',
            parent=styles['Normal'],
            fontSize=38,
            textColor=WHITE,
            alignment=TA_CENTER,
            leading=48,
            spaceAfter=30,
            spaceBefore=30
        )
    )

    # Table with blue background
    data = [[section_text]]
    table = Table(data, colWidths=[9.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PRIMARY_BLUE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 40),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))

    story.append(table)
    story.append(PageBreak())

def create_content_slide(story, styles, title, content_items):
    """Standard content slide"""
    # Title
    slide_title = Paragraph(
        f'<font color="#003E7E" size="28"><b>{title}</b></font>',
        styles['Heading1']
    )
    story.append(slide_title)
    story.append(Spacer(1, 0.3*inch))

    # Content
    for item in content_items:
        if isinstance(item, str):
            p = Paragraph(
                f'<font color="#5B5B5B" size="14">• {item}</font>',
                styles['BodyText']
            )
            story.append(p)
            story.append(Spacer(1, 0.15*inch))
        elif isinstance(item, tuple):  # (bullet, sub-items)
            p = Paragraph(
                f'<font color="#5B5B5B" size="14"><b>{item[0]}</b></font>',
                styles['BodyText']
            )
            story.append(p)
            story.append(Spacer(1, 0.1*inch))
            for sub in item[1]:
                sp = Paragraph(
                    f'<font color="#666666" size="12">   ◦ {sub}</font>',
                    styles['BodyText']
                )
                story.append(sp)
                story.append(Spacer(1, 0.08*inch))
            story.append(Spacer(1, 0.1*inch))

    story.append(PageBreak())

def create_two_column_slide(story, styles, title, left_title, left_items, right_title, right_items):
    """Two-column comparison slide"""
    slide_title = Paragraph(
        f'<font color="#003E7E" size="28"><b>{title}</b></font>',
        styles['Heading1']
    )
    story.append(slide_title)
    story.append(Spacer(1, 0.3*inch))

    # Create table for two columns
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
    """Generate the complete presentation"""
    doc = SimpleDocTemplate(
        "claude-code-tutorial.pdf",
        pagesize=PAGESIZE,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.7*inch,
        bottomMargin=0.7*inch
    )

    # Styles
    styles = getSampleStyleSheet()

    story = []

    # Slide 1: Title
    create_title_slide(story, styles)

    # Slide 2: Agenda
    create_content_slide(story, styles, "Agenda", [
        "Introduction to Claude Code",
        "AI-First Development Philosophy",
        "Getting Started",
        "Core Workflow",
        "Testing Strategy",
        "Best Practices",
        "Real-World Application"
    ])

    # Section: Introduction
    create_section_slide(story, styles, "Introduction")

    # Slide 3: What is Claude Code?
    create_content_slide(story, styles, "What is Claude Code?", [
        "AI-powered development tool for writing, debugging, and refactoring code",
        "Shifts paradigm from human writes → AI assists to AI writes → human validates",
        ("Core Benefits:", [
            "10-100x faster prototyping",
            "Consistent code standards",
            "Comprehensive testing",
            "Up-to-date documentation"
        ])
    ])

    # Slide 4: Traditional vs AI-First
    create_two_column_slide(story, styles, "Development Paradigm Shift",
        "Traditional Development", [
            "Human writes code",
            "AI assists occasionally",
            "Manual testing",
            "Documentation lags behind",
            "Inconsistent patterns"
        ],
        "AI-First Development", [
            "AI executes 100% of coding",
            "Human validates 100%",
            "Automated comprehensive tests",
            "Documentation generated with code",
            "Enforced consistency via CLAUDE.md"
        ]
    )

    # Section: Getting Started
    create_section_slide(story, styles, "Getting Started")

    # Slide 5: The CLAUDE.md File
    create_content_slide(story, styles, "The CLAUDE.md File", [
        "Your project's instruction manual for Claude Code",
        "Contains architecture, tech stack, and conventions",
        ("Essential Sections:", [
            "Project overview and architecture",
            "Git workflow and commit format",
            "Code standards and testing requirements",
            "Project structure and common commands"
        ]),
        "Updated throughout project lifecycle",
        "Ensures consistency across all sessions"
    ])

    # Slide 6: Setup Requirements
    create_content_slide(story, styles, "Prerequisites & Setup", [
        "Git 2.x or higher",
        "Code editor (VS Code, Cursor)",
        "Claude Code access (claude.ai/code)",
        ("Language-specific tools:", [
            "Node.js (via nvm) for JavaScript/TypeScript",
            "Python 3.10+ with virtual environments",
            "Go 1.20+ for Go projects"
        ]),
        "GitHub CLI (gh) recommended for PR management"
    ])

    # Section: Core Workflow
    create_section_slide(story, styles, "AI-First Workflow")

    # Slide 7: The 10-Step Process
    create_content_slide(story, styles, "The 10-Step Development Process", [
        "1. Human writes detailed specification",
        "2. AI designs database schema → Human reviews",
        "3. AI implements repository layer → Human reviews",
        "4. AI creates API endpoints → Human reviews",
        "5. AI writes comprehensive API E2E tests → Human verifies",
        "6. AI builds frontend components → Human reviews",
        "7. AI creates UI E2E tests → Human verifies",
        "8. AI updates documentation → Human reviews",
        "9. Human conducts code review (security, performance, quality)",
        "10. AI executes deployment → Human verifies"
    ])

    # Slide 8: AI vs Human Responsibilities
    create_two_column_slide(story, styles, "Clear Division of Responsibilities",
        "AI Executes 100%", [
            "Database schema design",
            "Repository implementation",
            "API endpoint creation",
            "E2E test writing",
            "Frontend component building",
            "Documentation updates",
            "Deployment execution"
        ],
        "Human Validates 100%", [
            "Write specifications",
            "Review schema design",
            "Approve implementations",
            "Verify tests pass",
            "Conduct code reviews",
            "Make architectural decisions",
            "Approve deployments"
        ]
    )

    # Section: Testing Strategy
    create_section_slide(story, styles, "Testing Strategy")

    # Slide 9: E2E First Philosophy
    create_content_slide(story, styles, "E2E Tests > Unit Tests", [
        "Inverted testing pyramid: E2E tests are primary",
        ("Why E2E First?", [
            "Test actual user flows",
            "Catch integration issues",
            "Verify the whole system",
            "Enable confident refactoring"
        ]),
        "Component tests: Only for complex UI logic",
        "Unit tests: Optional - only for critical algorithms",
        "Measure test effectiveness, don't assume value"
    ])

    # Slide 10: Testing Best Practices
    create_content_slide(story, styles, "E2E Testing Best Practices", [
        "Test user journeys, not implementation details",
        "Use stable data-test attributes, not CSS selectors",
        ("Coverage priorities:", [
            "Happy path - must pass",
            "Critical failures - invalid inputs, permissions",
            "Edge cases - boundary conditions",
            "Error scenarios - network failures, timeouts"
        ]),
        "Separate API and UI E2E tests",
        "Create reusable test commands and fixtures"
    ])

    # Section: Best Practices
    create_section_slide(story, styles, "Best Practices")

    # Slide 11: Git Workflow
    create_content_slide(story, styles, "Git Workflow Standards", [
        ("Branch naming: <type>/<description>", [
            "feature/, fix/, refactor/, docs/, test/, chore/"
        ]),
        ("Conventional commits: <type>(scope): subject", [
            "feat, fix, refactor, docs, test, chore, perf"
        ]),
        ("Hard rules - never break:", [
            "Never commit directly to main",
            "Never merge without review",
            "Never commit code that fails tests",
            "Pre-commit checks MUST pass (lint, test, build)"
        ])
    ])

    # Slide 12: Prompt Engineering
    create_content_slide(story, styles, "Effective Prompt Engineering", [
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

    # Slide 13: Code Quality Gates
    create_content_slide(story, styles, "Mandatory Quality Gates", [
        ("Pre-Commit (Local):", [
            "Run linter (ESLint, golangci-lint, etc.)",
            "Run all tests",
            "Verify build succeeds",
            "DO NOT commit if any check fails"
        ]),
        ("Pre-Merge (CI):", [
            "All E2E tests pass",
            "No linting errors",
            "Build succeeds",
            "Code review approved"
        ]),
        "AI cannot merge PRs - humans only"
    ])

    # Section: Real-World Application
    create_section_slide(story, styles, "Real-World Application")

    # Slide 14: Key Success Factors
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
        ]),
        ("4. Iterative refinement", [
            "Start working, refine as you go",
            "Commit small, atomic changes"
        ])
    ])

    # Slide 15: Common Mistakes to Avoid
    create_two_column_slide(story, styles, "Do's and Don'ts",
        "✓ DO", [
            "Write detailed specifications",
            "Prioritize E2E tests",
            "Review all AI output",
            "Use conventional commits",
            "Keep CLAUDE.md updated",
            "Run pre-commit checks",
            "Make small, focused PRs"
        ],
        "✗ DON'T", [
            "Make vague requests",
            "Skip testing",
            "Commit untested code",
            "Ignore CLAUDE.md",
            "Let AI merge PRs",
            "Commit directly to main",
            "Create large, unfocused PRs"
        ]
    )

    # Slide 16: Resources
    create_content_slide(story, styles, "Resources & Next Steps", [
        ("Official Documentation:", [
            "Claude Code: claude.ai/code",
            "Claude Docs: docs.anthropic.com"
        ]),
        ("Key Documentation Files:", [
            "CLAUDE.md template for your projects",
            "Step-by-step feature workflow guide",
            "Testing strategy detailed guide",
            "Troubleshooting common issues"
        ])
    ])

    # Slide 17: Thank You
    story.append(Spacer(1, 2*inch))
    thank_you = Paragraph(
        '<font color="#003E7E" size="48"><b>Thank You!</b></font>',
        styles['Title']
    )
    story.append(thank_you)
    story.append(Spacer(1, 0.4*inch))

    questions = Paragraph(
        '<font color="#5B5B5B" size="24">Questions?</font>',
        styles['Title']
    )
    story.append(questions)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print("✅ Presentation created: claude-code-tutorial.pdf")

if __name__ == "__main__":
    create_presentation()
