#!/usr/bin/env python3
"""
Combined Psychology Research Survey - PDF Form Generator
"The Role of Grit as a Mediator in the Relationship between Wisdom and PERMA Well-being"

Combines three psychological assessments:
1. Wisdom Questionnaire (20 items)
2. Grit Scale (12 items) 
3. PERMA-Profiler (23 items)
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

class CombinedPsychologyResearchPDFGenerator:
    def __init__(self):
        # Wisdom Questionnaire questions
        self.wisdom_questions = [
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
        
        # Grit Scale questions
        self.grit_questions = [
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
        
        # PERMA-Profiler questions organized by blocks
        self.perma_blocks = {
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
        
        # Define colors - professional research theme
        self.primary_color = HexColor('#2C3E50')      # Dark blue-grey
        self.secondary_color = HexColor('#3498DB')    # Bright blue  
        self.accent_color = HexColor('#85C1E9')       # Light blue
        self.wisdom_color = HexColor('#8E44AD')       # Purple for wisdom
        self.grit_color = HexColor('#D35400')         # Orange for grit
        self.perma_color = HexColor('#27AE60')        # Green for PERMA
        self.text_color = HexColor('#2D3748')         # Dark grey
        self.light_grey = HexColor('#F8F9FA')         # Very light grey
        
        # Set up styles
        self.setup_styles()
    
    def setup_styles(self):
        """Set up custom paragraph styles"""
        self.styles = getSampleStyleSheet()
        
        # Main title style
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Title'],
            fontSize=15,
            textColor=self.primary_color,
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=17
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=11,
            textColor=self.secondary_color,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        ))
        
        # Section title style
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=self.primary_color,
            spaceAfter=8,
            spaceBefore=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Question style
        self.styles.add(ParagraphStyle(
            name='Question',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.text_color,
            spaceAfter=0,
            spaceBefore=0,
            fontName='Helvetica',
            leading=11
        ))
        
        # Instructions style
        self.styles.add(ParagraphStyle(
            name='Instructions',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.text_color,
            spaceAfter=6,
            spaceBefore=3,
            fontName='Helvetica',
            alignment=TA_LEFT,
            leading=11
        ))
        
        # PERMA block header style
        self.styles.add(ParagraphStyle(
            name='PERMABlockHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.perma_color,
            spaceAfter=3,
            spaceBefore=8,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT,
            leading=11
        ))

    def create_wisdom_question_row(self, question_num, question_text):
        """Create a row for wisdom questionnaire (5-point scale)"""
        question_para = Paragraph(f"<b>W{question_num}.</b> {question_text}", self.styles['Question'])
        
        response_data = [
            [question_para, "___ 5", "___ 4", "___ 3", "___ 2", "___ 1"]
        ]
        
        table = Table(response_data, colWidths=[4.0*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch])
        
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('FONTNAME', (1, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (1, 0), (-1, 0), 8),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.text_color),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (-1, 0), 2),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, HexColor('#E2E8F0')),
        ]))
        
        return table

    def create_grit_question_row(self, question_num, question_text):
        """Create a row for grit scale (5-point scale)"""
        question_para = Paragraph(f"<b>G{question_num}.</b> {question_text}", self.styles['Question'])
        
        response_data = [
            [question_para, "___ 5", "___ 4", "___ 3", "___ 2", "___ 1"]
        ]
        
        table = Table(response_data, colWidths=[4.0*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch])
        
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('FONTNAME', (1, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (1, 0), (-1, 0), 8),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.text_color),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (-1, 0), 2),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, HexColor('#E2E8F0')),
        ]))
        
        return table

    def create_perma_question_row(self, label, question_text):
        """Create a row for PERMA-Profiler (0-10 scale)"""
        question_para = Paragraph(f"<b>P{label}.</b> {question_text}", self.styles['Question'])
        
        # Create 0-10 response scale exactly like reference
        response_options = []
        for i in range(11):  # 0 to 10
            response_options.append(f"_{i}")
        
        response_data = [
            [question_para] + response_options
        ]
        
        # Adjust column widths for 0-10 scale
        col_widths = [3.5*inch] + [0.3*inch] * 11
        table = Table(response_data, colWidths=col_widths)
        
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('FONTNAME', (1, 0), (-1, 0), 'Helvetica'),
            ('FONTSIZE', (1, 0), (-1, 0), 8),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.text_color),
            ('TOPPADDING', (0, 0), (-1, 0), 5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('LEFTPADDING', (0, 0), (0, 0), 0),
            ('RIGHTPADDING', (0, 0), (-1, 0), 1),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, HexColor('#E2E8F0')),
        ]))
        
        return table

    def create_perma_scale_reference(self, scale_text):
        """Create a scale reference for PERMA blocks"""
        scale_para = Paragraph(f"<i>{scale_text}</i>", self.styles['PERMABlockHeader'])
        
        scale_table = Table([[scale_para]], colWidths=[6.5*inch])
        scale_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#E8F8F5')),
            ('BOX', (0, 0), (-1, -1), 0.5, self.perma_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return scale_table

    def create_header_section(self):
        """Create the main header section"""
        header_content = []
        
        # Main title - split into multiple lines for better formatting
        title_line1 = Paragraph("THE ROLE OF GRIT AS A MEDIATOR IN THE", self.styles['MainTitle'])
        title_line2 = Paragraph("RELATIONSHIP BETWEEN WISDOM AND PERMA", self.styles['MainTitle'])
        title_line3 = Paragraph("WELL-BEING", self.styles['MainTitle'])
        header_content.append(title_line1)
        header_content.append(title_line2)
        header_content.append(title_line3)
        
        subtitle = Paragraph("Research Survey", self.styles['CustomSubtitle'])
        header_content.append(subtitle)
        
        header_content.append(Spacer(1, 20))
        
        # Demographic information - collected once for all assessments
        demo_title = Paragraph("<b>DEMOGRAPHIC INFORMATION</b>", self.styles['Instructions'])
        header_content.append(demo_title)
        header_content.append(Spacer(1, 10))
        
        # Participant information fields
        participant_fields = [
            ["Participant Name: _________________________", "Date: __________________"],
            ["Age: _______", "Gender: _________________"],
            ["Socio-Economic Status: _____Upper  _____Middle  _____Lower", ""],
            ["Area: _____ Rural   _____ Urban", ""],
            ["Education Level:   ___High School    ___Intermediate    ___Under Graduate     ___Other", ""],

        ]
        
        info_table = Table(participant_fields, colWidths=[3.8*inch, 3.2*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.text_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        header_content.append(info_table)
        header_content.append(Spacer(1, 20))
        
        return header_content

    def create_general_instructions(self):
        """Create general instructions for all assessments"""
        instructions_content = []
        
        # Instructions with blue box styling to match reference
        instructions_text = """
        <b>GENERAL INSTRUCTIONS:</b> This survey consists of three parts that measure different psychological traits. 
        Please read each statement carefully and respond honestly. There are no right or wrong answers - we are 
        interested in your genuine thoughts and feelings.<br/><br/>
        
        <b>Part 1:</b> Wisdom Assessment - 20 questions using a 5-point scale<br/>
        <b>Part 2:</b> Grit Scale - 12 questions using a 5-point scale<br/>
        <b>Part 3:</b> PERMA Well-being Assessment - 23 questions using a 0-10 scale<br/><br/>
        
        Please complete all sections and mark only one response per question. Thank you for your participation!
        """
        
        instructions_para = Paragraph(instructions_text, self.styles['Instructions'])
        
        instructions_table = Table([[instructions_para]], colWidths=[7.0*inch])
        instructions_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor("#EBF2F9")),  # Light blue background
            ('BOX', (0, 0), (-1, -1), 1, HexColor('#4A90E2')),  # Blue border
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        instructions_content.append(instructions_table)
        instructions_content.append(Spacer(1, 20))
        
        return instructions_content

    def create_footer_section(self):
        """Create comprehensive footer with all scoring information"""
        footer_content = []
        
        footer_content.append(Spacer(1, 15))
        
        footer_text = """
        <b>FOR RESEARCH USE ONLY - SCORING SUMMARY:</b><br/><br/><br/>
        <b>WISDOM SCORES:</b> Total: ____/100 | Creativity: ____/20 | Curiosity: ____/40 | Judgment: ____/20 | Social: ____/20<br/><br/><br/>
        <b>GRIT SCORES:</b> Total: ______/60 | Consistency of Interest: _____/30 | Perseverance of Effort: _____/30<br/>
        <i>Reverse score items G2, G3, G5, G6, G10, G12 for Grit calculations</i><br/><br/><br/>
        <b>PERMA SCORES:</b> P (Positive): ______ |  E (Engagement): ______ |  R (Relationships): ______ |  M (Meaning): ______   |  A (Achievement): _____ |  Health: _____ |  Negative Emotions: _____ |  Loneliness: _____ |  Overall Happiness: ______<br/><br/><br/><br/>
        <i>Thank you for participating in this comprehensive well-being research study.</i>
        """
        
        footer_para = Paragraph(footer_text, self.styles['Instructions'])
        footer_content.append(footer_para)
        
        return footer_content

    def generate_pdf(self, filename="combined_psychology_research_survey.pdf"):
        """Generate the complete combined PDF form"""
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.4*inch,
            leftMargin=0.4*inch,
            topMargin=0.4*inch,
            bottomMargin=0.4*inch
        )
        
        content = []
        
        # Add header and general instructions
        content.extend(self.create_header_section())
        content.extend(self.create_general_instructions())
        
        # PART 1: WISDOM QUESTIONNAIRE - Start on new page
        content.append(PageBreak())
        content.append(Paragraph("PART 1: WISDOM ASSESSMENT", self.styles['SectionTitle']))
        wisdom_instructions = Paragraph(
            "<b>Instructions:</b> Rate each statement on how much it describes you: 5=Very much like me, 4=Mostly like me, 3=Somewhat like me, 2=A little like me, 1=Not like me at all", 
            self.styles['Instructions']
        )
        content.append(wisdom_instructions)
        content.append(Spacer(1, 10))
        
        for i, question in enumerate(self.wisdom_questions, 1):
            question_row = self.create_wisdom_question_row(i, question)
            content.append(question_row)
            content.append(Spacer(1, 5))
        
        # PART 2: GRIT SCALE
        content.append(Spacer(1, 20))
        content.append(Paragraph("PART 2: GRIT SCALE", self.styles['SectionTitle']))
        grit_instructions = Paragraph(
            "<b>Instructions:</b> Rate each statement: 5=Very much like me, 4=Mostly like me, 3=Somewhat like me, 2=Not much like me, 1=Not like me at all", 
            self.styles['Instructions']
        )
        content.append(grit_instructions)
        content.append(Spacer(1, 10))
        
        for i, question in enumerate(self.grit_questions, 1):
            question_row = self.create_grit_question_row(i, question)
            content.append(question_row)
            content.append(Spacer(1, 5))
        
        # PART 3: PERMA-PROFILER
        content.append(Spacer(1, 20))
        content.append(Paragraph("PART 3: PERMA WELL-BEING ASSESSMENT", self.styles['SectionTitle']))
        perma_instructions = Paragraph(
            "<b>Instructions:</b> Rate each question on a scale from 0 to 10, where the meaning of 0 and 10 varies by question block as indicated below.", 
            self.styles['Instructions']
        )
        content.append(perma_instructions)
        content.append(Spacer(1, 10))
        
        # Add PERMA 0-10 scale header
        perma_scale_numbers = ['Response'] + [str(i) for i in range(11)]
        perma_scale_table = Table([perma_scale_numbers], colWidths=[3.5*inch] + [0.3*inch] * 11)
        perma_scale_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.perma_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, self.perma_color),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ]))
        content.append(perma_scale_table)
        content.append(Spacer(1, 8))
        
        # Add all PERMA question blocks
        for block_name, block_data in self.perma_blocks.items():
            # Add scale reference for this block
            content.append(self.create_perma_scale_reference(block_data['scale']))
            content.append(Spacer(1, 5))
            
            # Add questions in this block
            for label, question in block_data['questions']:
                question_row = self.create_perma_question_row(label, question)
                content.append(question_row)
                content.append(Spacer(1, 1))
            
            content.append(Spacer(1, 5))
        
        # Add footer section
        content.extend(self.create_footer_section())
        
        # Build PDF
        doc.build(content)
        print(f"Combined psychology research survey generated: {filename}")
        return filename

def main():
    """Main function to generate the combined PDF form"""
    print("Generating Combined Psychology Research Survey...")
    
    generator = CombinedPsychologyResearchPDFGenerator()
    
    # Generate with timestamp in filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"combined_psychology_survey_{timestamp}.pdf"
    
    try:
        pdf_file = generator.generate_pdf(filename)
        print(f"\n✅ Success! Combined survey created: {pdf_file}")
        print("\nThe combined survey includes:")
        print("- Single demographic data collection section")
        print("- Part 1: Wisdom Assessment (20 questions, 5-point scale)")
        print("- Part 2: Grit Scale (12 questions, 5-point scale)")
        print("- Part 3: PERMA Well-being Assessment (23 questions, 0-10 scale)")
        print("- Comprehensive scoring section for all assessments")
        print("- Professional research-quality formatting")
        print(f"- Total questions: 55 items plus demographics")
        
        # Also create a generic version
        generic_filename = "combined_psychology_research_survey.pdf"
        generator.generate_pdf(generic_filename)
        print(f"- Generic version also created: {generic_filename}")
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
