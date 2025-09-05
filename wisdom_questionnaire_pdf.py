#!/usr/bin/env python3
"""
WISDOM Research Survey - PDF Form Generator
Creates a beautiful, printable PDF form with radio buttons for the wisdom questionnaire.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Circle, String, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.platypus.flowables import Flowable
from datetime import datetime
import os

class CheckboxFlowable(Flowable):
    """Create a simple empty checkbox that can be drawn"""
    def __init__(self, size=10):
        Flowable.__init__(self)
        self.size = size
        self.width = size
        self.height = size
    
    def draw(self):
        # Draw an empty square
        self.canv.rect(0, 0, self.size, self.size, stroke=1, fill=0)

class WisdomQuestionnairePDFGenerator:
    def __init__(self):
        self.questions = [
            "I enjoy creating things that are new and different.",
            "I do not have many questions.",
            "I consider the positives and negatives of every option when I am making a decision.",
            "If there is a chance to learn something new, I jump right in.",
            "Others tell me that I give good advice.",
            "I see myself as a very creative person.",
            "I am curious about how things work.",
            "I carefully think about the opinions of others before I make a decision.",
            "I get excited when I see there is something new to learn.",
            "My friends ask for my opinion before they make an important decision.",
            "I often figure out different ways of doing things.",
            "I frequently ask questions.",
            "I wait until I have all the facts before I make a decision.",
            "I love learning about how to do different things.",
            "People tell me that I am a wise person.",
            "I always like to do things in different ways.",
            "I am always full of questions.",
            "I think about all my choices before I make a decision.",
            "When I want to learn something, I try to find out everything about it.",
            "I am able to solve problems in a way that is pleasing to everyone."
        ]
        
        self.response_options = [
            ('5', 'Very Much Like Me'),
            ('4', 'Mostly Like Me'),
            ('3', 'Somewhat Like Me'),
            ('2', 'A Little Like Me'),
            ('1', 'Not Like Me At All')
        ]
        
        # Define colors
        self.primary_color = HexColor('#2E4B5B')      # Deep blue-grey
        self.secondary_color = HexColor('#4A90A4')    # Light blue
        self.accent_color = HexColor('#83C5BE')       # Soft teal
        self.text_color = HexColor('#2D3748')         # Dark grey
        self.light_grey = HexColor('#F7FAFC')         # Very light grey
        
        # Set up styles
        self.setup_styles()
    
    def setup_styles(self):
        """Set up custom paragraph styles"""
        self.styles = getSampleStyleSheet()
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=self.primary_color,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.secondary_color,
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Question style
        self.styles.add(ParagraphStyle(
            name='Question',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=self.text_color,
            spaceAfter=0,
            spaceBefore=0,
            fontName='Helvetica',
            leading=16
        ))
        
        # Instructions style
        self.styles.add(ParagraphStyle(
            name='Instructions',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.text_color,
            spaceAfter=10,
            spaceBefore=5,
            fontName='Helvetica',
            alignment=TA_LEFT,
            leading=14
        ))
        
        # Header info style
        self.styles.add(ParagraphStyle(
            name='HeaderInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.text_color,
            fontName='Helvetica',
            leading=12
        ))

    def create_question_row(self, question_num, question_text):
        """Create a clean row for a single question with response options"""
        # Create the question text
        question_para = Paragraph(f"<b>{question_num}.</b> {question_text}", self.styles['Question'])
        
        # Create response boxes - simple underscores that can be marked
        response_data = [
            [question_para, "___ 5", "___ 4", "___ 3", "___ 2", "___ 1"]
        ]
        
        # Create table with appropriate column widths for A4
        table = Table(response_data, colWidths=[4.0*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch])
        
        # Clean table styling
        table.setStyle(TableStyle([
            # General alignment and padding
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Question text left-aligned
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),  # Response options centered
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            # Font styling
            ('FONTNAME', (1, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (1, 0), (-1, 0), 12),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.text_color),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (-1, 0), 5),
            
            # Subtle border
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, HexColor('#E2E8F0')),
        ]))
        
        return table

    def create_header_section(self):
        """Create the header section with participant information fields"""
        header_content = []
        
        # Title
        title = Paragraph("WISDOM RESEARCH SURVEY", self.styles['CustomTitle'])
        header_content.append(title)
        
        subtitle = Paragraph("Wisdom-Related Traits and Behaviors Assessment", self.styles['CustomSubtitle'])
        header_content.append(subtitle)
        
        header_content.append(Spacer(1, 20))
        
        # Simple participant information
        participant_fields = [
            ["Participant ID: _________________________", "Date: __________________"],
            ["Age: _______", "Gender: _________________"],
            ["Education Level: ________________________________________", ""]
        ]
        
        info_table = Table(participant_fields, colWidths=[3.8*inch, 3.2*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.text_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        header_content.append(info_table)
        header_content.append(Spacer(1, 25))
        
        return header_content

    def create_instructions_section(self):
        """Create the instructions section"""
        instructions_content = []
        
        # Instructions text
        instructions_text = """
        <b>INSTRUCTIONS:</b> Please read each statement and mark the box that best describes how much each statement is like you.
        <br/><br/>
        <b>5 = Very Much Like Me </b> &nbsp;&nbsp;&nbsp; <b> 4 = Mostly Like Me</b> &nbsp;&nbsp;&nbsp; <b> 3 = Somewhat Like Me</b> &nbsp;&nbsp;&nbsp; <b> 2 = A Little Like Me</b> &nbsp;&nbsp;&nbsp; <b> 1 = Not Like Me At All</b>
        <br/><br/>
        Please answer honestly. There are no right or wrong answers. Mark only one box per question.
        """
        
        inst_para = Paragraph(instructions_text, self.styles['Instructions'])
        instructions_content.append(inst_para)
        instructions_content.append(Spacer(1, 20))
        
        return instructions_content

    def create_scale_header(self):
        """Create a simple response scale header"""
        scale_text = "<b>Response Scale: &nbsp;&nbsp;&nbsp; 5 = Very Much Like Me &nbsp;&nbsp;&nbsp; 4 = Mostly Like Me &nbsp;&nbsp;&nbsp; 3 = Somewhat Like Me &nbsp;&nbsp;&nbsp; 2 = A Little Like Me &nbsp;&nbsp;&nbsp; 1 = Not Like Me At All</b>"
        
        scale_para = Paragraph(scale_text, self.styles['Instructions'])
        
        # Create a simple bordered header
        scale_table = Table([[scale_para]], colWidths=[7.0*inch])
        scale_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.light_grey),
            ('BOX', (0, 0), (-1, -1), 1, self.secondary_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return scale_table

    def create_footer_section(self):
        """Create footer with scoring information"""
        footer_content = []
        
        footer_content.append(Spacer(1, 20))
        footer_content.append(HRFlowable(width="100%", thickness=1, color=self.secondary_color))
        footer_content.append(Spacer(1, 10))
        
        footer_text = """
        <b>FOR RESEARCH USE ONLY:</b><br/>
        Total Score: _______ / 100 &nbsp;&nbsp;&nbsp; 
        Creativity: _______ / 20 &nbsp;&nbsp;&nbsp; 
        Curiosity: _______ / 40 &nbsp;&nbsp;&nbsp; 
        Judgment: _______ / 20 &nbsp;&nbsp;&nbsp; 
        Social Wisdom: _______ / 20<br/><br/>
        <i>Thank you for your participation in this research study.</i>
        """
        
        footer_para = Paragraph(footer_text, self.styles['Instructions'])
        footer_content.append(footer_para)
        
        return footer_content

    def generate_pdf(self, filename="wisdom_questionnaire_form.pdf"):
        """Generate the complete PDF form"""
        # Create document
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Build content
        content = []
        
        # Add header section
        content.extend(self.create_header_section())
        
        # Add instructions section
        content.extend(self.create_instructions_section())
        
        # Add scale header
        content.append(self.create_scale_header())
        content.append(Spacer(1, 15))
        
        # Add all questions
        for i, question in enumerate(self.questions, 1):
            question_row = self.create_question_row(i, question)
            content.append(question_row)
            content.append(Spacer(1, 3))
        
        # Add footer section
        content.extend(self.create_footer_section())
        
        # Build PDF
        doc.build(content)
        print(f"PDF form generated successfully: {filename}")
        return filename

def main():
    """Main function to generate the PDF form"""
    print("Generating WISDOM Research Survey PDF Form...")
    
    generator = WisdomQuestionnairePDFGenerator()
    
    # Generate with timestamp in filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"wisdom_questionnaire_form_{timestamp}.pdf"
    
    try:
        pdf_file = generator.generate_pdf(filename)
        print(f"\n✅ Success! PDF form created: {pdf_file}")
        print("\nThe form includes:")
        print("- Professional header with participant information fields")
        print("- Clear instructions and response scale")
        print("- 20 questions with radio button response options")
        print("- Scoring section for researchers")
        print("- Beautiful, printer-friendly design")
        
        # Also create a generic version without timestamp
        generic_filename = "wisdom_questionnaire_form.pdf"
        generator.generate_pdf(generic_filename)
        print(f"- Generic version also created: {generic_filename}")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
