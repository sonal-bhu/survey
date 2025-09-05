#!/usr/bin/env python3
"""
12-Item Grit Scale - PDF Form Generator
Creates a beautiful, printable PDF form for the Grit Scale questionnaire.
Grit measures perseverance and passion for long-term goals.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

class GritScalePDFGenerator:
    def __init__(self):
        # 12-Item Grit Scale questions
        self.questions = [
            "I have overcome setbacks to conquer an important challenge.",
            "New ideas and projects sometimes distract me from previous ones.",
            "My interests change from year to year.",
            "Setbacks don't discourage me. I don't give up easily.",
            "I often set a goal but later choose to pursue a different one.",
            "I have difficulty maintaining my focus on projects that take more than a few months to complete.",
            "I finish whatever I begin.",
            "I am a hard worker.",
            "I am diligent. I never give up.",
            "I have been obsessed with a certain idea or project for a short time but later lost interest.",
            "I work hard to achieve my goals.",
            "I often find myself having difficulty sticking with long-term commitments."
        ]
        
        # Response options for 5-point Likert scale
        self.response_options = [
            ('5', 'Very much like me'),
            ('4', 'Mostly like me'),
            ('3', 'Somewhat like me'),
            ('2', 'Not much like me'),
            ('1', 'Not like me at all')
        ]
        
        # Define colors - using earthy/warm tones for grit theme
        self.primary_color = HexColor('#8B4513')      # Saddle brown
        self.secondary_color = HexColor('#CD853F')    # Peru
        self.accent_color = HexColor('#DEB887')       # Burlywood
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

    def create_scale_header(self):
        """Create a simple response scale header"""
        scale_text = "<b>Response Scale: &nbsp;&nbsp;&nbsp; 5 = Very much like me &nbsp;&nbsp;&nbsp; 4 = Mostly like me &nbsp;&nbsp;&nbsp; 3 = Somewhat like me &nbsp;&nbsp;&nbsp; 2 = Not much like me &nbsp;&nbsp;&nbsp; 1 = Not like me at all</b>"
        
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

    def create_header_section(self):
        """Create the header section with participant information fields"""
        header_content = []
        
        # Title
        title = Paragraph("GRIT SCALE", self.styles['CustomTitle'])
        header_content.append(title)
        
        subtitle = Paragraph("Perseverance and Passion for Long-term Goals", self.styles['CustomSubtitle'])
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
        <b>INSTRUCTIONS:</b> Please read each statement and mark the number that best describes how much each statement is like you. Think about yourself as you generally are now, not as you wish to be in the future.
        <br/><br/>
        <b>5 = Very much like me</b> &nbsp;&nbsp;&nbsp; <b>4 = Mostly like me</b> &nbsp;&nbsp;&nbsp; <b>3 = Somewhat like me</b> &nbsp;&nbsp;&nbsp; <b>2 = Not much like me</b> &nbsp;&nbsp;&nbsp; <b>1 = Not like me at all</b>
        <br/><br/>
        Please answer honestly and mark only one number per statement. There are no right or wrong answers.
        """
        
        inst_para = Paragraph(instructions_text, self.styles['Instructions'])
        instructions_content.append(inst_para)
        instructions_content.append(Spacer(1, 20))
        
        return instructions_content

    def create_footer_section(self):
        """Create footer with scoring information"""
        footer_content = []
        
        footer_content.append(Spacer(1, 20))
        footer_content.append(HRFlowable(width="100%", thickness=1, color=self.secondary_color))
        footer_content.append(Spacer(1, 10))
        
        footer_text = """
        <b>FOR RESEARCH USE ONLY:</b><br/>
        <b>Scoring Instructions:</b> Reverse score items 2, 3, 5, 6, 10, and 12 (1=5, 2=4, 3=3, 4=2, 5=1)<br/>
        Consistency of Interest Score (items 2, 3, 5, 6, 10, 12): _______ / 30<br/>
        Perseverance of Effort Score (items 1, 4, 7, 8, 9, 11): _______ / 30<br/>
        <b>Total Grit Score: _______ / 60</b> &nbsp;&nbsp;&nbsp; <b>Average Grit Score: _______ / 5.0</b><br/><br/>
        <i>Thank you for your participation in this research study.</i>
        """
        
        footer_para = Paragraph(footer_text, self.styles['Instructions'])
        footer_content.append(footer_para)
        
        return footer_content

    def generate_pdf(self, filename="grit_scale_form.pdf"):
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
    print("Generating Grit Scale PDF Form...")
    
    generator = GritScalePDFGenerator()
    
    # Generate with timestamp in filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"grit_scale_form_{timestamp}.pdf"
    
    try:
        pdf_file = generator.generate_pdf(filename)
        print(f"\n✅ Success! PDF form created: {pdf_file}")
        print("\nThe form includes:")
        print("- Professional header with participant information fields")
        print("- Clear instructions for 5-point Likert scale responses")
        print("- All 12 Grit Scale questions")
        print("- Scoring section with reverse-scoring instructions")
        print("- Clean, printer-friendly A4 design")
        print("- Measures Consistency of Interest and Perseverance of Effort")
        
        # Also create a generic version without timestamp
        generic_filename = "grit_scale_form.pdf"
        generator.generate_pdf(generic_filename)
        print(f"- Generic version also created: {generic_filename}")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
