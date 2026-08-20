
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import pymupdf
from utils.template_renderer import render_resume_html

def generate_pdf_from_html(html: str, output_path: str) -> str:
    if not isinstance(html, str) or not html.strip():
        raise ValueError("HTML content cannot be empty.")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        document = pymupdf.open()
        page = document.new_page(width=595, height=842)
        
        # Fixed CSS with proper spacing, word-wrap, and bullet support
        fixed_css = """
        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
        }
        body { 
            font-family: Arial, Helvetica, sans-serif; 
            font-size: 10.5pt; 
            line-height: 1.5; 
            color: #202124; 
            padding: 40px; 
        }
        .resume { 
            max-width: 100%; 
        }
        h1 { 
            font-size: 22pt; 
            margin-bottom: 4px; 
        }
        h2 { 
            font-size: 12pt; 
            text-transform: uppercase; 
            letter-spacing: 0.7px; 
            margin: 14px 0 6px; 
            padding-bottom: 4px; 
            border-bottom: 1.5px solid #d8d8d8; 
        }
        .contact { 
            color: #555; 
            font-size: 9.5pt; 
            margin-bottom: 12px; 
        }
        .item-heading { 
            display: flex; 
            justify-content: space-between; 
            gap: 12px; 
            margin-top: 8px; 
        }
        .item-heading strong { 
            font-size: 11pt; 
            white-space: normal; 
            word-wrap: break-word; 
        }
        .item-heading span { 
            color: #666; 
            white-space: nowrap; 
            min-width: 80px; 
            text-align: right; 
        }
        .item-subheading { 
            color: #444; 
            margin-top: 2px; 
            font-size: 10pt; 
        }
        .experience-item, .education-item, .project-item { 
            margin-bottom: 10px; 
        }
        ul { 
            margin: 4px 0 0 18px; 
            padding: 0; 
            list-style-type: disc; 
        }
        li { 
            margin-bottom: 2px; 
            font-size: 10pt; 
            line-height: 1.4; 
        }
        .skills { 
            margin-top: 4px; 
            font-size: 10.5pt; 
        }
        .skills span { 
            display: inline-block; 
            background: #f0f0f0; 
            padding: 2px 10px; 
            border-radius: 4px; 
            margin: 2px 4px 2px 0; 
        }
        .technologies { 
            color: #555; 
            font-size: 9.5pt; 
            margin-top: 2px; 
        }
        """

        page.insert_htmlbox(
            rect=pymupdf.Rect(30, 30, 565, 812),
            text=html,
            css=fixed_css
        )
        document.save(str(output))
        document.close()

    except Exception as exc:
        raise RuntimeError(f"PDF generation failed: {exc}") from exc

    if not output.exists():
        raise RuntimeError("PDF generation completed without creating the output file.")
    if output.stat().st_size == 0:
        raise RuntimeError("Generated PDF is empty.")

    return str(output)

def generate_resume_pdf(resume_data: Dict[str, Any], output_path: str, template_id: str = "ats_minimal") -> str:
    html = render_resume_html(resume_data, template_id=template_id)
    return generate_pdf_from_html(html=html, output_path=output_path)

def validate_pdf(pdf_path: str) -> Dict[str, Any]:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF does not exist: {path}")
    if path.stat().st_size == 0:
        raise ValueError("PDF file is empty.")

    try:
        document = pymupdf.open(str(path))
        page_count = len(document)
        text_characters = 0
        for page in document:
            text = page.get_text("text")
            text_characters += len(text.strip())
        document.close()

        return {
            "valid": True,
            "pages": page_count,
            "characters": text_characters,
            "file_size": path.stat().st_size,
        }
    except Exception as exc:
        return {
            "valid": False,
            "pages": 0,
            "characters": 0,
            "file_size": path.stat().st_size,
            "error": str(exc),
        }
