#!/usr/bin/env python3
"""
Shared utilities for generating AI-First Development presentations.
Extracted from create_interactive_presentation_v2.py for reuse across presentations.
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
    """Custom canvas that adds page numbers to each page."""

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


def create_document(output_filename):
    """Create a SimpleDocTemplate with standard settings."""
    return SimpleDocTemplate(
        output_filename,
        pagesize=PAGESIZE,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.7*inch,
        bottomMargin=0.7*inch
    )


def create_title_slide(story, styles, title, subtitle, description=None):
    """Create a title slide with centered content."""
    story.append(Spacer(1, 1.5*inch))

    title_para = Paragraph(f'<font color="#003E7E" size="48"><b>{title}</b></font>', styles['Title'])
    story.append(title_para)
    story.append(Spacer(1, 0.2*inch))

    subtitle_para = Paragraph(f'<font color="#0076CE" size="28">{subtitle}</font>', styles['Title'])
    story.append(subtitle_para)

    if description:
        story.append(Spacer(1, 0.2*inch))
        desc_para = Paragraph(f'<font color="#5B5B5B" size="14">{description}</font>', styles['Title'])
        story.append(desc_para)

    story.append(PageBreak())


def create_section_slide(story, styles, title):
    """Create a section divider slide with blue background."""
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
    """
    Create a standard content slide with bullets.

    content_items can be:
    - A string: Creates a bullet point
    - A tuple (header, list): Creates a header with sub-bullets
    """
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


def create_two_column_slide(story, styles, title, left_title, left_items, right_title, right_items):
    """Create a two-column comparison slide."""
    slide_title = Paragraph(f'<font color="#003E7E" size="28"><b>{title}</b></font>', styles['Heading1'])
    story.append(slide_title)
    story.append(Spacer(1, 0.3*inch))

    # Build left column content
    left_content = [Paragraph(f'<font color="#0076CE" size="16"><b>{left_title}</b></font>', styles['BodyText'])]
    for item in left_items:
        left_content.append(Spacer(1, 0.1*inch))
        left_content.append(Paragraph(f'<font color="#5B5B5B" size="12">• {item}</font>', styles['BodyText']))

    # Build right column content
    right_content = [Paragraph(f'<font color="#0076CE" size="16"><b>{right_title}</b></font>', styles['BodyText'])]
    for item in right_items:
        right_content.append(Spacer(1, 0.1*inch))
        right_content.append(Paragraph(f'<font color="#5B5B5B" size="12">• {item}</font>', styles['BodyText']))

    # Create table
    data = [[left_content, right_content]]
    table = Table(data, colWidths=[4.5*inch, 4.5*inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    story.append(table)
    story.append(PageBreak())


def create_hands_on_slide(story, styles, title, prompt, expected_result, page_num, prompts_list=None):
    """
    Create a hands-on exercise slide with prompt and expected result.

    If prompts_list is provided, appends the prompt to it for export.
    """
    # Store prompt for export if list provided
    if prompts_list is not None:
        prompts_list.append({
            'page': page_num,
            'title': title,
            'prompt': prompt,
            'expected': expected_result
        })

    slide_title = Paragraph(f'<font color="#003E7E" size="28"><b>🔨 Hands-On: {title}</b></font>', styles['Heading1'])
    story.append(slide_title)
    story.append(Spacer(1, 0.2*inch))

    # Instruction
    instruction = Paragraph('<font color="#0076CE" size="16"><b>YOUR PROMPT:</b></font>', styles['BodyText'])
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
    """Create a code example slide."""
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


def create_thank_you_slide(story, styles, title="Thank You!", subtitle="Questions?"):
    """Create a thank you/closing slide."""
    story.append(Spacer(1, 2*inch))
    thank_you = Paragraph(f'<font color="#003E7E" size="48"><b>{title}</b></font>', styles['Title'])
    story.append(thank_you)
    story.append(Spacer(1, 0.4*inch))

    questions = Paragraph(f'<font color="#5B5B5B" size="24">{subtitle}</font>', styles['Title'])
    story.append(questions)


def export_prompts_to_markdown(prompts_list, output_filename, title="Workshop Prompts"):
    """Export collected prompts to a markdown file."""
    with open(output_filename, 'w') as f:
        f.write(f'# {title}\n\n')
        f.write('Copy and paste these prompts during the workshop exercises.\n\n')
        f.write('---\n\n')

        for item in prompts_list:
            f.write(f'## Page {item["page"]}: {item["title"]}\n\n')
            f.write('**PROMPT:**\n```\n')
            f.write(item['prompt'])
            f.write('\n```\n\n')
            f.write(f'**EXPECTED RESULT:**\n')
            f.write(f'{item["expected"]}\n\n')
            f.write('---\n\n')
