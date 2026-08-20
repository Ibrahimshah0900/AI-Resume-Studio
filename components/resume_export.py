
from __future__ import annotations
import streamlit as st
import tempfile
from pathlib import Path
from utils.template_renderer import render_resume_html
from utils.pdf_generator import generate_resume_pdf
from utils.template_engine import get_template, DEFAULT_TEMPLATE_ID

def render_resume_export() -> None:
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

    # Export options
    export_format = st.radio(
        "Select Export Format",
        ["📄 HTML", "📑 PDF", "📝 DOCX (Word)", "📋 TXT (ATS)"],
        horizontal=True
    )

    if export_format == "📄 HTML":
        st.subheader("Export as HTML")
        if st.button("Generate HTML", key="generate_html", type="primary"):
            try:
                with st.spinner("Generating HTML..."):
                    html_content = render_resume_html(
                        resume_data.model_dump(mode="json"),
                        template_id=selected_template_id,
                    )
                    st.session_state.html_content = html_content
                    st.success("HTML generated successfully!")
            except Exception as e:
                st.error(f"Error generating HTML: {e}")

        if st.session_state.get("html_content"):
            st.download_button(
                label="📥 Download HTML Resume",
                data=st.session_state.html_content,
                file_name="resume.html",
                mime="text/html",
                key="download_html",
            )

    elif export_format == "📑 PDF":
        st.subheader("Export as PDF")
        if st.button("Generate PDF", key="generate_pdf", type="primary"):
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
                        
                    st.success("PDF generated successfully!")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

        if st.session_state.get("pdf_ready") and st.session_state.get("pdf_bytes"):
            st.download_button(
                label="📥 Download PDF Resume",
                data=st.session_state.pdf_bytes,
                file_name="resume.pdf",
                mime="application/pdf",
                key="download_pdf",
            )

    elif export_format == "📝 DOCX (Word)":
        st.subheader("Export as DOCX")
        st.info("DOCX export coming soon! The resume will be available as a downloadable Word document.")
        
        if st.button("Generate DOCX", key="generate_docx", type="primary"):
            try:
                from docx import Document
                from io import BytesIO
                
                doc = Document()
                
                # Add content
                info = resume_data.get("personal_info", {})
                doc.add_heading(info.get("full_name", "Resume"), 0)
                doc.add_paragraph(info.get("professional_title", ""))
                
                if resume_data.get("summary"):
                    doc.add_heading("Professional Summary", level=1)
                    doc.add_paragraph(resume_data.get("summary"))
                
                if resume_data.get("skills"):
                    doc.add_heading("Skills", level=1)
                    doc.add_paragraph(", ".join(resume_data.get("skills", [])))
                
                # Save to bytes
                doc_bytes = BytesIO()
                doc.save(doc_bytes)
                doc_bytes.seek(0)
                
                st.session_state.docx_bytes = doc_bytes.getvalue()
                st.success("DOCX generated successfully!")
            except ImportError:
                st.error("python-docx is not installed. Please install it with: pip install python-docx")
            except Exception as e:
                st.error(f"Error generating DOCX: {e}")

        if st.session_state.get("docx_bytes"):
            st.download_button(
                label="📥 Download DOCX Resume",
                data=st.session_state.docx_bytes,
                file_name="resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="download_docx",
            )

    elif export_format == "📋 TXT (ATS)":
        st.subheader("Export as TXT (ATS-Optimized)")
        
        if st.button("Generate TXT", key="generate_txt", type="primary"):
            try:
                # Generate plain text version
                lines = []
                
                info = resume_data.get("personal_info", {})
                lines.append(info.get("full_name", ""))
                lines.append(info.get("professional_title", ""))
                lines.append(f"{info.get('email', '')} | {info.get('phone', '')} | {info.get('location', '')}")
                lines.append("")
                
                if resume_data.get("summary"):
                    lines.append("PROFESSIONAL SUMMARY")
                    lines.append(resume_data.get("summary"))
                    lines.append("")
                
                if resume_data.get("skills"):
                    lines.append("SKILLS")
                    lines.append(", ".join(resume_data.get("skills", [])))
                    lines.append("")
                
                if resume_data.get("experience"):
                    lines.append("EXPERIENCE")
                    for exp in resume_data.get("experience", []):
                        lines.append(f"{exp.get('job_title', '')} - {exp.get('company', '')}")
                        for bullet in exp.get("bullet_points", []):
                            lines.append(f"  • {bullet}")
                        lines.append("")
                
                if resume_data.get("education"):
                    lines.append("EDUCATION")
                    for edu in resume_data.get("education", []):
                        lines.append(f"{edu.get('degree', '')} - {edu.get('institution', '')}")
                        lines.append("")
                
                txt_content = "\n".join(lines)
                st.session_state.txt_content = txt_content
                st.success("TXT generated successfully!")
            except Exception as e:
                st.error(f"Error generating TXT: {e}")

        if st.session_state.get("txt_content"):
            st.download_button(
                label="📥 Download TXT Resume",
                data=st.session_state.txt_content,
                file_name="resume.txt",
                mime="text/plain",
                key="download_txt",
            )

    st.divider()
    st.caption("💡 Tip: Select a different template in the Templates section before exporting.")
