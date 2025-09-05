#!/usr/bin/env python3
"""
PERMA-Profiler Measure - PDF Form Generator
Creates a beautiful, printable PDF form for the PERMA-Profiler psychological assessment.
PERMA = Positive emotions, Engagement, Relationships, Meaning, Achievement
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

class PERMAProfierPDFGenerator:
    def __init__(self):
        # PERMA-Profiler questions organized by blocks
        self.question_blocks = {
            'Block 1': {
                'questions': [
                    ('A1', 'How much of the time do you feel you are making progress towards accomplishing your goals?'),
                    ('E1', 'How often do you become absorbed in what you are doing?'),
                    ('P1', 'In general, how often do you feel joyful?'),
                    ('N1', 'In general, how often do you feel anxious?'),
                    ('A2', 'How often do you achieve the important goals you have set for yourself?')
                ],
                'scale': '0 = never, 10 = always'
            },
            'Block 2': {
                'questions': [
                    ('H1', 'In general, how would you say your health is?')
                ],
                'scale': '0 = terrible, 10 = excellent'
            },
            'Block 3': {
                'questions': [
                    ('M1', 'In general, to what extent do you lead a purposeful and meaningful life?'),
                    ('R1', 'To what extent do you receive help and support from others when you need it?'),
                    ('M2', 'In general, to what extent do you feel that what you do in your life is valuable and worthwhile?'),
                    ('E2', 'In general, to what extent do you feel excited and interested in things?'),
                    ('Lon', 'How lonely do you feel in your daily life?')
                ],
                'scale': '0 = not at all, 10 = completely'
            },
            'Block 4': {
                'questions': [
                    ('H2', 'How satisfied are you with your current physical health?')
                ],
                'scale': '0 = not at all, 10 = completely'
            },
            'Block 5': {
                'questions': [
                    ('P2', 'In general, how often do you feel positive?'),
                    ('N2', 'In general, how often do you feel angry?'),
                    ('A3', 'How often are you able to handle your responsibilities?'),
                    ('N3', 'In general, how often do you feel sad?'),
                    ('E3', 'How often do you lose track of time while doing something you enjoy?')
                ],
                'scale': '0 = never, 10 = always'
            },
            'Block 6': {
                'questions': [
                    ('H3', 'Compared to others of your same age and sex, how is your health?')
                ],
                'scale': '0 = terrible, 10 = excellent'
            },
            'Block 7': {
                'questions': [
                    ('R2', 'To what extent do you feel loved?'),
                    ('M3', 'To what extent do you generally feel you have a sense of direction in your life?'),
                    ('R3', 'How satisfied are you with your personal relationships?'),
                    ('P3', 'In general, to what extent do you feel contented?')
                ],
                'scale': '0 = not at all, 10 = completely'
            },
            'Block 8': {
                'questions': [
                    ('hap', 'Taking all things together, how happy would you say you are?')
                ],
                'scale': '0 = not at all, 10 = completely'
            }
        }
        
        # Define colors
        self.primary_color = HexColor('#1B4B8C')      # Deep blue
        self.secondary_color = HexColor('#3B82C3')    # Medium blue
        self.accent_color = HexColor('#7BB3F0')       # Light blue
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
            fontSize=11,
            textColor=self.text_color,
            spaceAfter=0,
            spaceBefore=0,
            fontName='Helvetica',
            leading=14
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
        
        # Block header style
        self.styles.add(ParagraphStyle(
            name='BlockHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.primary_color,
            spaceAfter=5,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            leading=12
        ))

    def create_question_row(self, label, question_text, scale_info):
        """Create a clean row for a single question with 0-10 response scale"""
        # Create the question text with label
        question_para = Paragraph(f"<b>{label}.</b> {question_text}", self.styles['Question'])
        
        # Create 0-10 response scale
        response_options = []
        for i in range(11):  # 0 to 10
            response_options.append(f"___ {i}")
        
        # Create table data
        response_data = [
            [question_para] + response_options
        ]
        
        # Create table with appropriate column widths for A4 (11 response columns + question column)
        col_widths = [3.2*inch] + [0.35*inch] * 11
        table = Table(response_data, colWidths=col_widths)
        
        # Clean table styling
        table.setStyle(TableStyle([
            # General alignment and padding
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # Question text left-aligned
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),  # Response options centered
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            # Font styling
            ('FONTNAME', (1, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (1, 0), (-1, 0), 9),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.text_color),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (-1, 0), 2),
            
            # Subtle border
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, HexColor('#E2E8F0')),
        ]))
        
        return table

    def create_scale_reference(self, scale_text):
        """Create a scale reference box"""
        scale_para = Paragraph(f"<b>Scale:</b> {scale_text}", self.styles['BlockHeader'])
        
        scale_table = Table([[scale_para]], colWidths=[7.0*inch])
        scale_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.light_grey),
            ('BOX', (0, 0), (-1, -1), 1, self.accent_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        return scale_table

    def create_response_scale_header(self):
        """Create the 0-10 response scale header"""
        scale_numbers = ['Response'] + [str(i) for i in range(11)]
        
        scale_table = Table([scale_numbers], colWidths=[3.2*inch] + [0.35*inch] * 11)
        scale_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 2, self.primary_color),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ]))
        
        return scale_table

    def create_header_section(self):
        """Create the header section with participant information fields"""
        header_content = []
        
        # Title
        title = Paragraph("THE PERMA-PROFILER MEASURE", self.styles['CustomTitle'])
        header_content.append(title)
        
        subtitle = Paragraph("Positive Psychology Assessment", self.styles['CustomSubtitle'])
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
        <b>INSTRUCTIONS:</b> Please answer each question by marking the number that best describes how you feel. Each question uses a scale from 0 to 10, where the meaning of 0 and 10 are provided for each set of questions.
        <br/><br/>
        Please answer honestly and mark only one number per question. There are no right or wrong answers.
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
        P (Positive Emotions): _______ &nbsp;&nbsp;&nbsp; 
        E (Engagement): _______ &nbsp;&nbsp;&nbsp; 
        R (Relationships): _______ &nbsp;&nbsp;&nbsp; 
        M (Meaning): _______ &nbsp;&nbsp;&nbsp; 
        A (Achievement): _______ <br/>
        Health: _______ &nbsp;&nbsp;&nbsp; 
        Negative Emotions: _______ &nbsp;&nbsp;&nbsp; 
        Loneliness: _______ &nbsp;&nbsp;&nbsp; 
        Happiness: _______ <br/><br/>
        <i>Thank you for your participation in this research study.</i>
        """
        
        footer_para = Paragraph(footer_text, self.styles['Instructions'])
        footer_content.append(footer_para)
        
        return footer_content

    def generate_pdf(self, filename="perma_profiler_form.pdf"):
        """Generate the complete PDF form"""
        # Create document
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.4*inch,
            leftMargin=0.4*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Build content
        content = []
        
        # Add header section
        content.extend(self.create_header_section())
        
        # Add instructions section
        content.extend(self.create_instructions_section())
        
        # Add response scale header
        content.append(self.create_response_scale_header())
        content.append(Spacer(1, 10))
        
        # Add all question blocks
        for block_name, block_data in self.question_blocks.items():
            # Add scale reference for this block
            content.append(self.create_scale_reference(block_data['scale']))
            content.append(Spacer(1, 5))
            
            # Add questions in this block
            for label, question in block_data['questions']:
                question_row = self.create_question_row(label, question, block_data['scale'])
                content.append(question_row)
                content.append(Spacer(1, 2))
            
            # Add some space after each block
            content.append(Spacer(1, 8))
        
        # Add footer section
        content.extend(self.create_footer_section())
        
        # Build PDF
        doc.build(content)
        print(f"PDF form generated successfully: {filename}")
        return filename

def main():
    """Main function to generate the PDF form"""
    print("Generating PERMA-Profiler PDF Form...")
    
    generator = PERMAProfierPDFGenerator()
    
    # Generate with timestamp in filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"perma_profiler_form_{timestamp}.pdf"
    
    try:
        pdf_file = generator.generate_pdf(filename)
        print(f"\n✅ Success! PDF form created: {pdf_file}")
        print("\nThe form includes:")
        print("- Professional header with participant information fields")
        print("- Clear instructions for 0-10 scale responses")
        print("- All PERMA-Profiler questions organized by blocks")
        print("- Different scale anchors for different question blocks")
        print("- Scoring section for researchers")
        print("- Clean, printer-friendly A4 design")
        
        # Also create a generic version without timestamp
        generic_filename = "perma_profiler_form.pdf"
        generator.generate_pdf(generic_filename)
        print(f"- Generic version also created: {generic_filename}")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
