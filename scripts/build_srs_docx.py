import zipfile
import xml.sax.saxutils as saxutils

def escape(text):
    return saxutils.escape(str(text))

def create_paragraph(text, bold=False, italic=False, font_size=22, color="24292E", space_after=120, heading_level=None, align=None):
    jc_tag = f'<w:jc w:val="{align}"/>' if align else ''
    
    if heading_level == 1:
        font_size = 36
        bold = True
        color = "0366D6"
        space_after = 240
    elif heading_level == 2:
        font_size = 28
        bold = True
        color = "1B1F23"
        space_after = 180
    elif heading_level == 3:
        font_size = 24
        bold = True
        color = "24292E"
        space_after = 120

    b_tag = '<w:b/>' if bold else ''
    i_tag = '<w:i/>' if italic else ''
    
    return f'''<w:p>
        <w:pPr>
            {jc_tag}
            <w:spacing w:after="{space_after}"/>
        </w:pPr>
        <w:r>
            <w:rPr>
                <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
                {b_tag}
                {i_tag}
                <w:color w:val="{color}"/>
                <w:sz w:val="{font_size}"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape(text)}</w:t>
        </w:r>
    </w:p>'''

def create_table(headers, rows, col_widths=None):
    if not col_widths:
        col_widths = [9000 // len(headers)] * len(headers)
        
    xml = ['''<w:tbl>
        <w:tblPr>
            <w:tblW w:w="9000" w:type="dxa"/>
            <w:tblBorders>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="D1D5DA"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="D1D5DA"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E1E4E8"/>
                <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E1E4E8"/>
            </w:tblBorders>
        </w:tblPr>''']
    
    # Header row
    xml.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
    for idx, header in enumerate(headers):
        w = col_widths[idx]
        xml.append(f'''<w:tc>
            <w:tcPr>
                <w:tcW w:w="{w}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="F1F8FF"/>
            </w:tcPr>
            <w:p>
                <w:pPr><w:spacing w:after="60"/></w:pPr>
                <w:r>
                    <w:rPr>
                        <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
                        <w:b/>
                        <w:color w:val="0366D6"/>
                        <w:sz w:val="20"/>
                    </w:rPr>
                    <w:t>{escape(header)}</w:t>
                </w:r>
            </w:p>
        </w:tc>''')
    xml.append('</w:tr>')
    
    # Data rows
    for r_idx, row in enumerate(rows):
        fill = "FAFBFC" if r_idx % 2 == 1 else "FFFFFF"
        xml.append('<w:tr>')
        for idx, cell in enumerate(row):
            w = col_widths[idx]
            xml.append(f'''<w:tc>
                <w:tcPr>
                    <w:tcW w:w="{w}" w:type="dxa"/>
                    <w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>
                </w:tcPr>
                <w:p>
                    <w:pPr><w:spacing w:after="40"/></w:pPr>
                    <w:r>
                        <w:rPr>
                            <w:rFonts w:ascii="Segoe UI" w:hAnsi="Segoe UI"/>
                            <w:sz w:val="18"/>
                            <w:color w:val="24292E"/>
                        </w:rPr>
                        <w:t>{escape(cell)}</w:t>
                    </w:r>
                </w:p>
            </w:tc>''')
        xml.append('</w:tr>')
        
    xml.append('</w:tbl>')
    return ''.join(xml)

def build_docx():
    body_parts = []
    
    # Title & Subtitle
    body_parts.append(create_paragraph("SOFTWARE REQUIREMENTS SPECIFICATION (SRS)", bold=True, heading_level=1, align="center"))
    body_parts.append(create_paragraph("Project 2: Student Academic Performance Analytics", bold=True, heading_level=2, align="center"))
    body_parts.append(create_paragraph("Five-Day Engineering Student Training | First Year – First Semester", italic=True, font_size=20, color="586069", align="center", space_after=300))
    
    # Metadata Table
    meta_headers = ["Attribute", "Specification Details"]
    meta_rows = [
        ["Project Title", "Student Academic Performance Analytics"],
        ["Industry Sector", "Education / EdTech"],
        ["Academic Level", "First-Year Engineering Student (Data Analytics Track)"],
        ["Technology Stack", "Python 3.13, NumPy 2.3, Pandas 2.3, Jupyter Notebook"],
        ["Deliverables", "SRS Document (DOCX/PDF), Jupyter Notebook (.ipynb), Python Script (.py), Cleaned CSV"],
        ["Submission Status", "Final LMS Submission (100% Complete)"]
    ]
    body_parts.append(create_table(meta_headers, meta_rows, [3000, 6000]))
    body_parts.append(create_paragraph("", space_after=200))
    
    # Section 1
    body_parts.append(create_paragraph("1. Problem Statement & Objectives", heading_level=2))
    body_parts.append(create_paragraph(
        "Higher education engineering programs face substantial hurdles in proactively identifying students experiencing foundational academic difficulties. "
        "Historically, struggling students are only detected after the final examination period, when semester remediation is no longer feasible. "
        "Furthermore, academic institutions accumulate operational data across student attendance, weekly independent study hours, and digital connectivity, "
        "yet lack automated, data-driven frameworks to extract actionable insights from these datasets."
    ))
    body_parts.append(create_paragraph(
        "This project engineers an end-to-end data analytics workflow using Python, NumPy, and Pandas to audit raw student records, rectify data anomalies, "
        "compute academic grading bands, aggregate departmental performance, model statistical distributions using NumPy, identify at-risk students, "
        "and produce five concrete, evidence-based recommendations for academic support."
    ))
    
    body_parts.append(create_paragraph("Core Objectives:", bold=True, font_size=22))
    objectives = [
        "1. Ingest and inspect raw academic records from 02_student_performance.csv.",
        "2. Identify and resolve missing attendance values via Department-wise Median Imputation.",
        "3. Detect and remove duplicate Student_IDs and enforce assessment score bounds [0.0, 100.0].",
        "4. Engineer core academic features: Total_Marks, Average_Marks, Letter Grades (pd.cut), and Attendance Tiers.",
        "5. Benchmark performance across academic departments and measure the impact of home internet access.",
        "6. Perform rigorous NumPy numerical evaluations: Median, Standard Deviation, Quartiles (Q1, Q2, Q3), and Tukey's IQR Outliers.",
        "7. Deliver five actionable, data-backed institutional support recommendations."
    ]
    for obj in objectives:
        body_parts.append(create_paragraph(obj, font_size=20, space_after=60))
        
    # Section 2
    body_parts.append(create_paragraph("2. Dataset Description", heading_level=2))
    body_parts.append(create_paragraph("The project evaluates the teaching benchmark dataset 02_student_performance.csv consisting of 9 attributes:"))
    
    ds_headers = ["Attribute Name", "Data Type", "Description", "Domain Constraints"]
    ds_rows = [
        ["Student_ID", "String (object)", "Unique primary identifier key", "STU1001, STU1002, ..."],
        ["Name", "String (object)", "Full student name", "Alphabetic text"],
        ["Department", "String (object)", "Engineering branch", "CS, IT, Data Science, Electronics, Mech"],
        ["Attendance", "Float (float64)", "Classroom attendance percentage", "0.0% to 100.0% (contains missing values)"],
        ["Study_Hours", "Float (float64)", "Weekly independent study hours", "0.0 to 40.0 hours/week"],
        ["Internet_Access", "String (object)", "Home broadband connectivity", "'Yes' or 'No'"],
        ["Python_Marks", "Float (float64)", "Assessment score in Python", "0.0 to 100.0 marks"],
        ["Math_Marks", "Float (float64)", "Assessment score in Mathematics", "0.0 to 100.0 marks"],
        ["DBMS_Marks", "Float (float64)", "Assessment score in DBMS", "0.0 to 100.0 marks"]
    ]
    body_parts.append(create_table(ds_headers, ds_rows, [1800, 1800, 3200, 2200]))
    body_parts.append(create_paragraph("", space_after=200))

    # Section 3
    body_parts.append(create_paragraph("3. Functional Requirements (FR-01 to FR-15)", heading_level=2))
    fr_headers = ["Requirement ID", "Task Name", "Technical Specification"]
    fr_rows = [
        ["FR-01", "Dataset Ingestion & Inspection", "Load CSV via pd.read_csv(); audit .shape, .dtypes, .head(), and .describe()."],
        ["FR-02", "Missing & Duplicate Auditing", "Report missing values with .isnull().sum(); drop duplicate Student_IDs using drop_duplicates()."],
        ["FR-03", "Attendance Imputation", "Impute missing attendance using Department Median; explain resistance of median to extreme outliers."],
        ["FR-04", "Score Range Validation", "Identify marks outside [0, 100]; rectify clerical errors via numerical clipping (.clip(0, 100))."],
        ["FR-05", "Total & Average Marks", "Compute Total_Marks as sum of 3 subjects; calculate Average_Marks rounded to 2 decimals."],
        ["FR-06", "Academic Grade Allocation", "Assign letter grades via pd.cut(): A (85-100), B (70-85), C (55-70), D (40-55), F (<40)."],
        ["FR-07", "Department Performance", "Compute department-wise student counts, marks, and attendance averages using groupby().agg()."],
        ["FR-08", "Top 10 Rankers Identification", "Extract and display the top 10 academic performers sorted by Average_Marks in descending order."],
        ["FR-09", "At-Risk Cohort Isolation", "Filter and identify all students scoring below 40% average marks requiring immediate academic support."],
        ["FR-10", "Attendance Band Analytics", "Segment attendance into policy tiers (<60%, 60-75%, 75-85%, >85%) and evaluate average marks."],
        ["FR-11", "Study Hours Correlation", "Compute Pearson correlation (Study_Hours vs Average_Marks); evaluate study hour bands."],
        ["FR-12", "Digital Equity Evaluation", "Compare overall and subject marks for students with vs without home internet; quantify gap."],
        ["FR-13", "NumPy Numerical Metrics", "Extract Python_Marks array; compute np.median, np.std, np.var, and quartiles Q1, Q2, Q3."],
        ["FR-14", "Tukey IQR Outlier Detection", "Compute IQR = Q3 - Q1; establish fences Q1 - 1.5*IQR and Q3 + 1.5*IQR; isolate outlier scores."],
        ["FR-15", "Institutional Recommendations", "Formulate 5 evidence-based academic support recommendations backed by empirical findings."]
    ]
    body_parts.append(create_table(fr_headers, fr_rows, [1400, 2600, 5000]))
    body_parts.append(create_paragraph("", space_after=200))

    # Section 4 & 5
    body_parts.append(create_paragraph("4. Non-Functional Requirements", heading_level=2))
    nfrs = [
        "- Determinism & Reproducibility: Execution must produce identical results across independent platforms without hardcoded answers.",
        "- Beginner-Friendly Simplicity: Implementation must follow clear naming, standard loops/vectorization, and clear comments.",
        "- Methodological Rigor: Correlation must never be claimed as causation; limitations must be explicitly noted."
    ]
    for nfr in nfrs:
        body_parts.append(create_paragraph(nfr, font_size=20, space_after=60))

    body_parts.append(create_paragraph("5. Five Evidence-Based Academic Recommendations", heading_level=2))
    recs = [
        "1. Early Warning Attendance Alert System: Trigger automatic alerts at the 75% attendance threshold. Students with <60% attendance averaged only 45.59 marks compared to 57.80 marks for students with >85% attendance.",
        "2. Targeted Remedial Tutoring for At-Risk Students: Provide structured weekend foundation classes in Python and Math for the 6 students identified scoring below the passing threshold of 40%.",
        "3. Campus Digital Equity Initiative: Bridge the 5.97-mark performance gap between connected and non-connected students by extending campus computer labs to 24/7 access and providing offline video courseware.",
        "4. Guided Study Hours Program: Form peer study circles to assist students studying under 10 hours/week, as self-study exhibited a strong positive correlation (r = 0.62) with student scores.",
        "5. Inter-Departmental Pedagogical Forums: Facilitate cross-department workshops where high-performing departments (Electronics at 56.51 avg) share effective coding lab practices with developing departments (IT at 52.23 avg)."
    ]
    for rec in recs:
        body_parts.append(create_paragraph(rec, font_size=20, space_after=80))

    # Assemble Document XML
    doc_body = ''.join(body_parts)
    
    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        <w:body>
            {doc_body}
            <w:sectPr>
                <w:pgSz w:w="11906" w:h="16838"/>
                <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
            </w:sectPr>
        </w:body>
    </w:document>'''

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
        <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
        <Default Extension="xml" ContentType="application/xml"/>
        <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    </Types>'''

    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
        <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
    </Relationships>'''

    with zipfile.ZipFile('SRS/project_SRS.docx', 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', content_types)
        zf.writestr('_rels/.rels', rels)
        zf.writestr('word/document.xml', document_xml)

    print("SRS/project_SRS.docx built successfully!")

if __name__ == '__main__':
    build_docx()
