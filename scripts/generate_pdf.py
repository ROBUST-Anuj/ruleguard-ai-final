"""Generate a realistic PDF student handbook for the NIT corpus."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib import colors


def build_pdf():
    os.makedirs(os.path.join('data', 'pdf'), exist_ok=True)
    pdf_path = os.path.join('data', 'pdf', 'student_handbook.pdf')

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        title="NIT Student Handbook 2024-25",
        author="Northbridge Institute of Technology",
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        'DocTitle', parent=styles['Title'],
        fontSize=22, spaceAfter=6 * mm, textColor=HexColor('#1e3a5f'),
    ))
    styles.add(ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontSize=13, alignment=TA_CENTER, spaceAfter=10 * mm,
        textColor=HexColor('#555555'),
    ))
    styles.add(ParagraphStyle(
        'SectionHead', parent=styles['Heading1'],
        fontSize=16, spaceAfter=4 * mm, spaceBefore=8 * mm,
        textColor=HexColor('#1e3a5f'),
    ))
    styles.add(ParagraphStyle(
        'SubHead', parent=styles['Heading2'],
        fontSize=13, spaceAfter=3 * mm, spaceBefore=5 * mm,
        textColor=HexColor('#2d5a8e'),
    ))
    styles.add(ParagraphStyle(
        'BodyJ', parent=styles['Normal'],
        fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=3 * mm,
    ))
    styles.add(ParagraphStyle(
        'BodyBullet', parent=styles['Normal'],
        fontSize=10, leading=14, leftIndent=12 * mm, spaceAfter=2 * mm,
    ))

    story = []

    # ──────────────────────────────────────────────
    # PAGE 1 – Title page
    # ──────────────────────────────────────────────
    story.append(Spacer(1, 40 * mm))
    story.append(Paragraph("Northbridge Institute of Technology", styles['DocTitle']))
    story.append(Paragraph("Student Handbook 2024-25", styles['DocSubtitle']))
    story.append(Spacer(1, 10 * mm))
    story.append(HRFlowable(width="60%", thickness=1, color=HexColor('#1e3a5f')))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(
        "This handbook is an official document of the Northbridge Institute of Technology. "
        "It contains essential information about academic policies, student services, "
        "campus facilities, and regulations that every student must be aware of. "
        "All students are expected to read and comply with the provisions outlined in this handbook.",
        styles['BodyJ']
    ))
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(
        "Published by the Office of the Dean of Student Affairs<br/>"
        "Northbridge Institute of Technology<br/>"
        "Northbridge, Karnataka 560001<br/>"
        "www.nit.edu.in",
        styles['DocSubtitle']
    ))
    story.append(PageBreak())

    # ──────────────────────────────────────────────
    # PAGE 2 – General Information
    # ──────────────────────────────────────────────
    story.append(Paragraph("1. General Information", styles['SectionHead']))
    story.append(Paragraph(
        "The Northbridge Institute of Technology (NIT) was established in 1985 with the mission "
        "of providing world-class technical education. Located on a 250-acre campus in Northbridge, "
        "Karnataka, the Institute offers undergraduate, postgraduate, and doctoral programs across "
        "twelve departments of engineering, science, and management.",
        styles['BodyJ']
    ))
    story.append(Paragraph(
        "NIT is recognized by the University Grants Commission (UGC) and accredited by the "
        "National Board of Accreditation (NBA). The Institute is ranked among the top 50 engineering "
        "institutions in India and has a student body of approximately 5,000 students.",
        styles['BodyJ']
    ))

    story.append(Paragraph("1.1 Academic Calendar", styles['SubHead']))
    story.append(Paragraph(
        "The academic year at NIT is divided into two main semesters and an optional summer term:",
        styles['BodyJ']
    ))

    cal_data = [
        ['Term', 'Duration', 'Instruction Weeks'],
        ['Autumn Semester', 'August – December', '14 weeks'],
        ['Spring Semester', 'January – May', '14 weeks'],
        ['Summer Term', 'June – July', '6 weeks'],
    ]
    cal_table = Table(cal_data, colWidths=[45 * mm, 50 * mm, 45 * mm])
    cal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f0f4f8')]),
    ]))
    story.append(cal_table)
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("1.2 Student Identification", styles['SubHead']))
    story.append(Paragraph(
        "Every enrolled student is issued an NIT Identity Card at the time of admission. "
        "The ID card must be carried at all times while on campus and must be presented "
        "upon request by Institute authorities, security personnel, or examination staff. "
        "Loss of the ID card must be reported to the Student Affairs Office within 24 hours. "
        "A duplicate ID card may be obtained upon payment of ₹300.",
        styles['BodyJ']
    ))
    story.append(PageBreak())

    # ──────────────────────────────────────────────
    # PAGE 3 – Student Services
    # ──────────────────────────────────────────────
    story.append(Paragraph("2. Student Services", styles['SectionHead']))

    story.append(Paragraph("2.1 NIT Health Centre", styles['SubHead']))
    story.append(Paragraph(
        "The NIT Health Centre is located adjacent to the main academic block and operates "
        "from 8:00 AM to 8:00 PM on all working days. Emergency medical services are available "
        "24 hours a day, seven days a week. The Health Centre is staffed by two full-time physicians, "
        "three nurses, and a counsellor. Common medications, first aid, and basic diagnostic "
        "services are provided free of charge to all enrolled students.",
        styles['BodyJ']
    ))
    story.append(Paragraph(
        "Medical certificates issued by the NIT Health Centre are accepted for all academic "
        "purposes, including attendance exemptions and examination make-up requests. External "
        "medical certificates must be from a recognized hospital and are subject to verification "
        "by the Health Centre.",
        styles['BodyJ']
    ))

    story.append(Paragraph("2.2 Library", styles['SubHead']))
    story.append(Paragraph(
        "The NIT Central Library houses over 150,000 volumes, including textbooks, reference works, "
        "journals, and digital resources. The library is open from 8:00 AM to 11:00 PM on weekdays "
        "and from 9:00 AM to 6:00 PM on weekends. Students may borrow up to five books at a time "
        "for a period of fourteen days, renewable once. Overdue fines are ₹5 per book per day.",
        styles['BodyJ']
    ))

    story.append(Paragraph("2.3 Counselling Services", styles['SubHead']))
    story.append(Paragraph(
        "The Student Counselling Centre provides confidential counselling services for students "
        "experiencing academic stress, personal difficulties, or mental health concerns. "
        "Appointments can be made through the SIS portal or by visiting the centre in person. "
        "All interactions are strictly confidential and do not appear in the student's academic record.",
        styles['BodyJ']
    ))

    story.append(Paragraph("2.4 Career Development Centre", styles['SubHead']))
    story.append(Paragraph(
        "The Career Development Centre (CDC) manages campus placements, internship programs, "
        "and career guidance workshops. The CDC organizes an annual placement drive in the Autumn "
        "semester for final-year students. Pre-placement training, including mock interviews and "
        "resume workshops, is offered free of charge to all registered students.",
        styles['BodyJ']
    ))
    story.append(PageBreak())

    # ──────────────────────────────────────────────
    # PAGE 4 – Attendance Exceptions
    # ──────────────────────────────────────────────
    story.append(Paragraph("3. Attendance Exceptions and Special Provisions", styles['SectionHead']))
    story.append(Paragraph(
        "While the standard minimum attendance requirement for semester examinations is 75% "
        "(as specified in the Attendance Policy), certain categories of students may be granted "
        "attendance relaxation under the following provisions:",
        styles['BodyJ']
    ))

    story.append(Paragraph("3.1 Students with Medical Exemptions", styles['SubHead']))
    story.append(Paragraph(
        "Students who have been granted a medical exemption under the Medical Exemption Policy "
        "may be permitted to appear for examinations with reduced attendance. The specific "
        "attendance threshold after medical exemption shall be determined by the Dean of "
        "Academic Affairs based on the duration and nature of the medical condition.",
        styles['BodyJ']
    ))

    story.append(Paragraph("3.2 Students Representing NIT", styles['SubHead']))
    story.append(Paragraph(
        "Students representing NIT at recognized national or international events (academic, "
        "sports, or cultural) may be granted attendance relaxation of up to 10% upon "
        "recommendation by the Dean of Student Affairs. This relaxation does not reduce the "
        "minimum threshold below 65%.",
        styles['BodyJ']
    ))

    story.append(Paragraph("3.3 Students with Disabilities", styles['SubHead']))
    story.append(Paragraph(
        "Students registered with the Office of Disability Services who have documented "
        "conditions affecting regular attendance may receive individualized attendance "
        "accommodations. These accommodations are determined on a case-by-case basis and "
        "communicated to all relevant course instructors at the beginning of each semester.",
        styles['BodyJ']
    ))

    story.append(Paragraph("3.4 Important Contacts for Attendance Issues", styles['SubHead']))
    contacts_data = [
        ['Office', 'Contact Person', 'Email', 'Phone'],
        ['Academic Affairs', 'Dr. Ramesh Kumar', 'dean.acad@nit.edu.in', '+91-80-XXXX-1001'],
        ['Health Centre', 'Dr. Priya Sharma', 'health@nit.edu.in', '+91-80-XXXX-1002'],
        ['Student Affairs', 'Dr. Suresh Patel', 'dean.sa@nit.edu.in', '+91-80-XXXX-1003'],
        ['Disability Services', 'Ms. Anita Rao', 'disability@nit.edu.in', '+91-80-XXXX-1004'],
    ]
    contacts_table = Table(contacts_data, colWidths=[35 * mm, 35 * mm, 45 * mm, 35 * mm])
    contacts_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f0f4f8')]),
    ]))
    story.append(contacts_table)
    story.append(PageBreak())

    # ──────────────────────────────────────────────
    # PAGE 5 – Examination Guidelines
    # ──────────────────────────────────────────────
    story.append(Paragraph("4. Examination Guidelines for Students", styles['SectionHead']))
    story.append(Paragraph(
        "This section summarizes the key guidelines that students must follow during "
        "examinations at NIT. For detailed regulations, refer to the Examination Policy "
        "(NIT/EXAM/2024-25).",
        styles['BodyJ']
    ))

    story.append(Paragraph("4.1 Before the Examination", styles['SubHead']))
    story.append(Paragraph(
        "• Verify your examination schedule on the SIS portal at least one week before exams.<br/>"
        "• Ensure all fees, including the examination fee of ₹2,000, are paid.<br/>"
        "• Collect your hall ticket from the SIS portal. A printed copy must be brought to every exam.<br/>"
        "• Check that you meet the minimum attendance requirement (75%) for each course.<br/>"
        "• Report any scheduling conflicts to the Controller of Examinations immediately.",
        styles['BodyBullet']
    ))

    story.append(Paragraph("4.2 During the Examination", styles['SubHead']))
    story.append(Paragraph(
        "• Arrive at the examination hall at least 15 minutes before the scheduled start time.<br/>"
        "• Carry your NIT ID card and hall ticket.<br/>"
        "• Electronic devices (phones, smartwatches, tablets) are strictly prohibited.<br/>"
        "• Non-programmable calculators are permitted only where specified by the course instructor.<br/>"
        "• No student may leave the hall during the first 60 minutes or last 15 minutes.<br/>"
        "• All answer scripts must be submitted to the invigilator before leaving.",
        styles['BodyBullet']
    ))

    story.append(Paragraph("4.3 After the Examination", styles['SubHead']))
    story.append(Paragraph(
        "Results are published on the SIS portal within 30 days of the examination. "
        "Students may apply for revaluation within 10 working days of result publication "
        "by paying a revaluation fee of ₹500 per course. The revaluation is conducted by "
        "an independent evaluator, and the revised grade (whether higher or lower) replaces "
        "the original grade.",
        styles['BodyJ']
    ))
    story.append(PageBreak())

    # ──────────────────────────────────────────────
    # PAGE 6 – Fee Summary
    # ──────────────────────────────────────────────
    story.append(Paragraph("5. Fee Summary and Financial Information", styles['SectionHead']))
    story.append(Paragraph(
        "The following table summarizes the fee structure for B.Tech students for the "
        "academic year 2024-25. For detailed fee regulations, payment methods, and refund "
        "policies, refer to the Fee Regulations (NIT/FEE/2024-25).",
        styles['BodyJ']
    ))

    fee_data = [
        ['Fee Component', 'Amount (₹)', 'Deadline', 'Late Fee'],
        ['Tuition Fee', '1,25,000', 'September 15', '₹500/day'],
        ['Laboratory Fee', '15,000', 'September 15', '₹500/day'],
        ['Library Fee', '5,000', 'September 15', '₹100/day'],
        ['Examination Fee', '2,000', 'October 10', '₹300/day'],
        ['Student Activity Fee', '3,000', 'September 15', '₹500/day'],
        ['Technology Fee', '7,500', 'September 15', '₹500/day'],
        ['Hostel Fee (Double)', '25,000', 'September 5', '₹250/day'],
        ['Mess Fee (Monthly)', '4,500', '5th of month', 'N/A'],
    ]
    fee_table = Table(fee_data, colWidths=[40 * mm, 30 * mm, 35 * mm, 30 * mm])
    fee_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3a5f')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f0f4f8')]),
    ]))
    story.append(fee_table)
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("5.1 Scholarships", styles['SubHead']))
    story.append(Paragraph(
        "NIT offers several scholarship programs for deserving students. Merit scholarships "
        "are awarded to students with a CGPA of 8.5 or above and cover 25% to 100% of tuition fees. "
        "Need-based scholarships are available for students with annual family income below ₹8,00,000. "
        "Sports scholarships covering up to 50% of tuition fees are available for students representing "
        "NIT or the state/nation in recognized events. Applications are accepted during the first "
        "four weeks of each academic year through the SIS portal.",
        styles['BodyJ']
    ))

    story.append(Paragraph("5.2 Financial Hardship", styles['SubHead']))
    story.append(Paragraph(
        "Students facing documented financial hardship may apply for a fee instalment plan through "
        "the Office of Student Financial Services. The instalment plan allows fees to be paid in "
        "up to three equal monthly instalments. A processing fee of ₹500 applies. Applications must "
        "be submitted at least 10 working days before the fee deadline.",
        styles['BodyJ']
    ))
    story.append(PageBreak())

    # ──────────────────────────────────────────────
    # PAGE 7 – Code of Conduct Summary
    # ──────────────────────────────────────────────
    story.append(Paragraph("6. Code of Conduct", styles['SectionHead']))
    story.append(Paragraph(
        "All students at NIT are expected to maintain the highest standards of personal and "
        "academic conduct. The following is a summary of the key expectations. For the full "
        "disciplinary framework, refer to the Disciplinary Regulations (NIT/DISC/2024-25).",
        styles['BodyJ']
    ))

    story.append(Paragraph("6.1 Academic Integrity", styles['SubHead']))
    story.append(Paragraph(
        "NIT maintains a zero-tolerance policy towards academic misconduct. Plagiarism, cheating, "
        "fabrication of data, unauthorized collaboration, and proxy attendance are serious offences "
        "that may result in penalties ranging from a written warning to permanent expulsion.",
        styles['BodyJ']
    ))

    story.append(Paragraph("6.2 Campus Conduct", styles['SubHead']))
    story.append(Paragraph(
        "Students must treat all members of the NIT community — fellow students, faculty, staff, "
        "and visitors — with respect and courtesy. Harassment, discrimination, bullying, and "
        "intimidation in any form are strictly prohibited. The consumption of alcohol, tobacco, "
        "and illegal substances is prohibited on campus.",
        styles['BodyJ']
    ))

    story.append(Paragraph("6.3 Anti-Ragging", styles['SubHead']))
    story.append(Paragraph(
        "Ragging in any form is a criminal offence and is strictly prohibited at NIT. "
        "Penalties for ragging include immediate suspension, expulsion from the hostel, "
        "rustication for up to four semesters, or permanent expulsion. An anti-ragging helpline "
        "is available 24/7.",
        styles['BodyJ']
    ))

    story.append(Paragraph("6.4 Grievance Redressal", styles['SubHead']))
    story.append(Paragraph(
        "Students who have grievances related to academic matters, hostel facilities, mess quality, "
        "or any other aspect of campus life may submit a written complaint through the SIS portal "
        "or in person to the relevant authority. If the grievance is not resolved within 10 working "
        "days, it may be escalated to the Dean of Student Affairs or the Vice-Chancellor's Office.",
        styles['BodyJ']
    ))
    story.append(Spacer(1, 10 * mm))

    story.append(HRFlowable(width="60%", thickness=1, color=HexColor('#1e3a5f')))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "This handbook is a summary document. For the complete and legally binding text of all "
        "policies and regulations, please refer to the individual policy documents available on "
        "the NIT website at www.nit.edu.in/policies.",
        styles['BodyJ']
    ))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "<i>Last updated: August 1, 2024</i>",
        styles['DocSubtitle']
    ))

    # Build with page numbers
    def add_page_number(canvas_obj, doc_obj):
        page_num = canvas_obj.getPageNumber()
        text = f"NIT Student Handbook 2024-25  —  Page {page_num}"
        canvas_obj.saveState()
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(HexColor('#888888'))
        canvas_obj.drawCentredString(A4[0] / 2, 1.2 * cm, text)
        canvas_obj.restoreState()

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"[OK] Generated PDF: {pdf_path} ({doc.page} pages)")


if __name__ == '__main__':
    build_pdf()
