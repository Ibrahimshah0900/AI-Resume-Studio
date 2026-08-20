
from __future__ import annotations
import streamlit as st
import uuid
from pathlib import Path
import tempfile

from utils.template_renderer import render_resume_html
from utils.pdf_generator import generate_resume_pdf
from utils.template_engine import get_template, DEFAULT_TEMPLATE_ID
from utils.data_models import Resume

def render_resume_export() -> None:
    """Render the resume export workflow."""
    
    st.markdown('<div class="section-title">📥 Export Resume</div>', unsafe_allow_html=True)
    st.write("Generate professional resumes in multiple formats using your selected template.")

    resume_data = st.session_state.resume_data

    if not resume_data:
        st.info("Please create or load a resume in the Resume Builder first.")
        return

    selected_template_id = st.session_state.get("selected_template_id", DEFAULT_TEMPLATE_ID)

    try:
        template = get_template(selected_template_id)
        st.subheader(f"Selected Template: {template.name}")
    except:
        st.subheader(f"Selected Template: {selected_template_id}")
    
    st.write("Your resume will be exported using this template.")
    st.divider()

    # Export format selection
    export_format = st.radio(
        "Select Export Format",
        ["📑 PDF", "📝 DOCX (Word)"],
        horizontal=True
    )

    # ----- PDF EXPORT -----
    if export_format == "📑 PDF":
        st.subheader("📑 Export as PDF")
        st.write("Generate a professional PDF version of your resume.")
        
        if st.button("📄 Generate PDF", key="generate_pdf_btn", type="primary"):
            try:
                with st.spinner("Generating PDF..."):
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        pdf_path = generate_resume_pdf(
                            resume_data.model_dump(mode="json"),
                            output_path=tmp.name,
                            template_id=selected_template_id,
                        )
                        
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                        
                        st.session_state.pdf_bytes = pdf_bytes
                        st.session_state.pdf_ready = True
                        Path(pdf_path).unlink(missing_ok=True)
                        
                    st.success("✅ PDF generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating PDF: {e}")

        if st.session_state.get("pdf_ready") and st.session_state.get("pdf_bytes"):
            # Use a simple unique key
            key_suffix = str(uuid.uuid4())[:8]
            st.download_button(
                label="📥 Download PDF Resume",
                data=st.session_state.pdf_bytes,
                file_name="resume.pdf",
                mime="application/pdf",
                key=f"download_pdf_{key_suffix}",
            )

    # ----- DOCX EXPORT -----
    elif export_format == "📝 DOCX (Word)":
        st.subheader("📝 Export as Word Document")
        st.write("Generate a fully formatted Word document with all your resume data.")
        
        if st.button("📄 Generate DOCX", key="generate_docx_btn", type="primary"):
            try:
                from docx import Document
                from docx.shared import Pt
                from docx.enum.text import WD_ALIGN_PARAGRAPH
                from io import BytesIO
                
                # Convert Resume object to dict if needed
                if isinstance(resume_data, Resume):
                    resume_dict = resume_data.model_dump()
                else:
                    resume_dict = resume_data
                
                doc = Document()
                
                # Set up document style
                style = doc.styles['Normal']
                style.font.name = 'Calibri'
                style.font.size = Pt(11)
                
                # Header: Name
                info = resume_dict.get("personal_info", {})
                name = info.get("full_name", info.get("name", "Resume"))
                title = doc.add_heading(name, 0)
                title.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
                # Professional Title
                professional_title = info.get("professional_title", "")
                if professional_title:
                    p = doc.add_paragraph(professional_title)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.runs[0].font.size = Pt(14)
                    p.runs[0].font.italic = True
                
                # Contact Info
                contact_parts = []
                if info.get("email"):
                    contact_parts.append(info.get("email"))
                if info.get("phone"):
                    contact_parts.append(info.get("phone"))
                if info.get("location"):
                    contact_parts.append(info.get("location"))
                
                if contact_parts:
                    p = doc.add_paragraph(" | ".join(contact_parts))
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.runs[0].font.size = Pt(10)
                
                doc.add_paragraph()
                
                # Summary
                summary = resume_dict.get("summary", "")
                if summary:
                    doc.add_heading("Professional Summary", level=1)
                    doc.add_paragraph(summary)
                    doc.add_paragraph()
                
                # Experience
                experience = resume_dict.get("experience", [])
                if experience:
                    doc.add_heading("Experience", level=1)
                    for exp in experience:
                        job_title = exp.get("job_title", "")
                        company = exp.get("company", "")
                        if job_title and company:
                            p = doc.add_paragraph()
                            run = p.add_run(f"{job_title}")
                            run.bold = True
                            p.add_run(f" — {company}")
                        
                        start_date = exp.get("start_date", "")
                        end_date = exp.get("end_date", "")
                        if start_date or end_date:
                            p = doc.add_paragraph(f"{start_date} - {end_date}")
                            p.runs[0].font.italic = True
                            p.runs[0].font.size = Pt(10)
                        
                        bullets = exp.get("bullet_points", [])
                        if bullets:
                            for bullet in bullets:
                                if bullet:
                                    doc.add_paragraph(bullet, style='List Bullet')
                        doc.add_paragraph()
                
                # Education
                education = resume_dict.get("education", [])
                if education:
                    doc.add_heading("Education", level=1)
                    for edu in education:
                        degree = edu.get("degree", "")
                        institution = edu.get("institution", "")
                        if degree and institution:
                            p = doc.add_paragraph()
                            run = p.add_run(f"{degree}")
                            run.bold = True
                            p.add_run(f" — {institution}")
                        
                        field = edu.get("field_of_study", "")
                        if field:
                            doc.add_paragraph(field)
                        doc.add_paragraph()
                
                # Skills
                skills = resume_dict.get("skills", [])
                if skills:
                    doc.add_heading("Skills", level=1)
                    doc.add_paragraph(", ".join(skills))
                    doc.add_paragraph()
                
                # Projects
                projects = resume_dict.get("projects", [])
                if projects:
                    doc.add_heading("Projects", level=1)
                    for proj in projects:
                        proj_name = proj.get("name", "")
                        if proj_name:
                            p = doc.add_paragraph()
                            run = p.add_run(proj_name)
                            run.bold = True
                        
                        if proj.get("description"):
                            doc.add_paragraph(proj.get("description"))
                        
                        techs = proj.get("technologies", [])
                        if techs:
                            doc.add_paragraph(f"Technologies: {', '.join(techs)}")
                        doc.add_paragraph()
                
                # Certifications
                certifications = resume_dict.get("certifications", [])
                if certifications:
                    doc.add_heading("Certifications", level=1)
                    for cert in certifications:
                        cert_name = cert.get("name", "")
                        if cert_name:
                            doc.add_paragraph(cert_name)
                    doc.add_paragraph()
                
                # Languages
                languages = resume_dict.get("languages", [])
                if languages:
                    doc.add_heading("Languages", level=1)
                    for lang in languages:
                        lang_name = lang.get("name", "")
                        proficiency = lang.get("proficiency", "")
                        if lang_name:
                            if proficiency:
                                doc.add_paragraph(f"{lang_name} - {proficiency}")
                            else:
                                doc.add_paragraph(lang_name)
                    doc.add_paragraph()
                
                # Achievements
                achievements = resume_dict.get("achievements", [])
                if achievements:
                    doc.add_heading("Achievements", level=1)
                    for ach in achievements:
                        ach_title = ach.get("title", "")
                        if ach_title:
                            doc.add_paragraph(ach_title)
                    doc.add_paragraph()
                
                # Save to bytes
                doc_bytes = BytesIO()
                doc.save(doc_bytes)
                doc_bytes.seek(0)
                
                st.session_state.docx_bytes = doc_bytes.getvalue()
                st.session_state.docx_ready = True
                st.success("✅ DOCX generated successfully with all resume data!")
                
            except ImportError:
                st.error("❌ python-docx is not installed. Please install it.")
            except Exception as e:
                st.error(f"❌ Error generating DOCX: {e}")

        if st.session_state.get("docx_ready") and st.session_state.get("docx_bytes"):
            # Use a simple unique key
            key_suffix = str(uuid.uuid4())[:8]
            st.download_button(
                label="📥 Download DOCX Resume",
                data=st.session_state.docx_bytes,
                file_name="resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key=f"download_docx_{key_suffix}",
            )

    st.divider()
    st.caption("💡 Tip: Select a different template in the Templates section before exporting.")
