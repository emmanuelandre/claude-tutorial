# PDF Slides Regeneration Guide

The presentation PDF files need to be regenerated when the Python scripts are updated.

## ⚠️ IMPORTANT WARNING

**The PDF generation script will OVERWRITE `prompts.md` with an auto-generated version.**

Before regenerating the PDF:
1. **Back up `prompts.md`** if you have manual updates
2. **Restore `prompts.md`** after regeneration from git or backup
3. Or modify the script to not export prompts.md

## Updated Files

The following Python scripts have been updated and the PDFs need to be regenerated:

1. `create_interactive_presentation_v2.py` - Updated testing philosophy slide
2. `create_interactive_presentation.py` - Updated testing philosophy slide

## What Changed

The "Testing Philosophy" slide content was updated from:
- ❌ OLD: "Unit tests are OPTIONAL (only for complex algorithms)"
- ✅ NEW: "Unit tests are MANDATORY (business logic, utilities, edge cases)"

Also added:
- Component tests are GOOD TO HAVE (test containers for microservices)
- Test-First Approach with coverage tracking
- Coverage measurement is important

## How to Regenerate

To regenerate the PDF slides, run:

```bash
# Install dependencies (if not already installed)
pip install reportlab

# IMPORTANT: Back up prompts.md first!
cp prompts.md prompts.md.backup

# Generate the updated PDF (use python3, not python)
python3 create_interactive_presentation_v2.py

# This will create/update: claude-code-interactive-tutorial.pdf
# WARNING: This also overwrites prompts.md!

# Restore your custom prompts.md
mv prompts.md.backup prompts.md
# OR restore from git:
git checkout prompts.md
```

Or for the alternative version:

```bash
python create_interactive_presentation.py
# This will create/update: claude-code-tutorial.pdf
```

## Files That Were Already Updated

✅ **Documentation:**
- `CLAUDE.md`
- `README.md`
- `examples/claude-md-template.md`
- `docs/06-testing-strategy.md`
- `docs/07-ai-first-workflow.md`
- `prompts.md`

✅ **Presentation Scripts:**
- `create_interactive_presentation_v2.py`
- `create_interactive_presentation.py`

❌ **PDF Files (need regeneration):**
- `claude-code-interactive-tutorial.pdf`
- `claude-code-tutorial.pdf` (if using the other script)

## Summary of Testing Philosophy Changes

### New Philosophy:
1. **E2E tests** - Mandatory (user journeys, API + UI)
2. **Unit tests** - Mandatory (business logic, utilities, edge cases)
3. **Component tests** - Good to have (test containers for microservices)
4. **Coverage measurement** - Important (track from all test types, 70-90% typical thresholds)
5. **Test-first approach** - Define coverage targets and build testing infrastructure before implementation
6. **Pre-commit hooks** - Run lint, unit tests, and E2E tests before every commit

This ensures comprehensive quality coverage and catches issues early in the development cycle.
