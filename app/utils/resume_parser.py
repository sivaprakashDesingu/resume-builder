"""
Resume parsing utility for DOCX and PDF files.

Dependencies (install via pip if missing):
    pip install python-docx PyPDF2

This parser focuses on extracting core fields from typical resumes:
- fullName
- professionalTitle (best-effort from top lines)
- email
- phone
- location (best-effort)
- summary (first paragraph after header)
- skills (list)
- experiences (list of {title, company, duration, description})
- educations (list of {degree, school, year})

Heuristics-based: light-weight and fast; can be extended with NLP later.
"""
from __future__ import annotations

import io
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# --- PDF/DOCX readers ---
try:
    import docx  # python-docx
except Exception:  # pragma: no cover
    docx = None

try:
    from PyPDF2 import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")
YEAR_RE = re.compile(r"(19|20)\d{2}")

# Common section headers to help chunk content
SECTION_HEADERS = [
    "summary", "objective", "experience", "employment", "work history",
    "education", "skills", "technical skills", "projects", "certifications",
    "about", "overview", "professional profile", "professional summary",
]


@dataclass
class Experience:
    title: str = ""
    company: str = ""
    duration: str = ""
    description: str = ""


@dataclass
class Education:
    degree: str = ""
    school: str = ""
    year: str = ""


@dataclass
class Certification:
    name: str = ""
    issuer: str = ""
    year: str = ""


@dataclass
class ParsedResume:
    fullName: str = ""
    professionalTitle: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    summary: str = ""
    skills: List[Dict[str, Any]] = None
    experiences: List[Dict[str, Any]] = None
    educations: List[Dict[str, Any]] = None
    certifications: List[Dict[str, Any]] = None

    def to_template_data(self) -> Dict[str, Any]:
        return {
            'fullName': self.fullName,
            'professionalTitle': self.professionalTitle,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'summary': self.summary,
            'skills': self.skills or [],
            'experiences': self.experiences or [],
            'educations': self.educations or [],
            'certifications': self.certifications or [],
            'customSections': [],
        }


# --- Public API ---
def parse_resume(file_bytes: bytes, filename: str, content_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse an uploaded resume file (DOCX or PDF) and return dict matching
    the resume_editor template fields.
    """
    ext = (filename.rsplit('.', 1)[-1] if '.' in filename else '').lower()
    text = ""

    # Determine file type by extension, content type, or magic bytes
    if ext == 'docx' or (content_type and 'wordprocessingml' in content_type):
        text = _read_docx_text(file_bytes)
    elif ext == 'pdf' or (content_type and 'pdf' in content_type):
        text = _read_pdf_text(file_bytes)
    else:
        # Check magic bytes for PDF even if extension/content_type don't indicate it
        if file_bytes.startswith(b'%PDF'):
            text = _read_pdf_text(file_bytes)
        # Check magic bytes for DOCX (ZIP file with specific structure)
        elif file_bytes.startswith(b'PK\x03\x04'):
            text = _read_docx_text(file_bytes)
        else:
            # try best-effort as text
            try:
                text = file_bytes.decode('utf-8', errors='ignore')
            except Exception:
                text = ''

    return _parse_text(text)


# --- Readers ---
def _read_docx_text(file_bytes: bytes) -> str:
    if not docx:
        raise RuntimeError('python-docx is required to parse DOCX files. Install with: pip install python-docx')
    bio = io.BytesIO(file_bytes)
    document = docx.Document(bio)
    paras = []
    for p in document.paragraphs:
        paras.append(p.text)
    # Tables may contain skills/experience details
    for table in document.tables:
        for row in table.rows:
            cells_text = [c.text for c in row.cells]
            if any(cells_text):
                paras.append(" \u2022 ".join([t for t in cells_text if t]))
    return "\n".join([p for p in paras if p and p.strip()])


def _read_pdf_text(file_bytes: bytes) -> str:
    if not PdfReader:
        raise RuntimeError('PyPDF2 is required to parse PDF files. Install with: pip install PyPDF2')
    bio = io.BytesIO(file_bytes)
    reader = PdfReader(bio)
    parts: List[str] = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            continue
    text = "\n".join([p for p in parts if p and p.strip()])
    
    # Clean up excessive whitespace from PDF extraction issues
    # PDFs often have spaces between letters due to formatting
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are just whitespace or single characters (usually formatting artifacts)
        if stripped and len(stripped) > 1:
            # Try to rejoin lines that look like they were split incorrectly
            # (e.g., "Sr." on one line, "Principal" on next, "Software" on next)
            cleaned_lines.append(stripped)
    
    return "\n".join(cleaned_lines)


# --- Text Parser ---
def _parse_text(text: str) -> Dict[str, Any]:
    lines = [l.strip() for l in text.splitlines()]
    lines = [l for l in lines if l]
    blob = "\n".join(lines)

    email = _first_match(EMAIL_RE, blob)
    phone = _first_match(PHONE_RE, blob)
    # Clean up phone: remove newlines and extra whitespace
    if phone:
        phone = re.sub(r'\s+', ' ', phone).strip()

    # === NAME EXTRACTION ===
    # Strategy: First 1-2 single capitalized words = name parts
    # Typically 2-3 names before hitting location
    full_name = ''
    name_end_idx = 0
    
    for i, line in enumerate(lines[:6]):  # Limit to first 6 lines for names
        words = line.split()
        
        # Skip contacts and headers
        if (EMAIL_RE.search(line) or PHONE_RE.search(line) or 
            any(h in line.lower() for h in SECTION_HEADERS) or 'http' in line):
            break
        
        # A single capitalized word is likely a name part
        if len(words) == 1 and words[0] and words[0][0].isupper():
            full_name += " " + line if full_name else line
            name_end_idx = i
            # Stop after 2-3 name parts, we should have full name
            if len(full_name.split()) >= 2:
                break
        else:
            # Once we hit multi-word line after collecting name(s), stop
            if full_name:
                break
    
    # === LOCATION EXTRACTION ===
    # Look for location after name
    location = ''
    location_end_idx = name_end_idx
    
    for i in range(name_end_idx + 1, min(name_end_idx + 8, len(lines))):
        line = lines[i]
        
        if (EMAIL_RE.search(line) or PHONE_RE.search(line) or
            any(h in line.lower() for h in SECTION_HEADERS)):
            break
        
        # Build location by combining consecutive lines
        if _looks_like_location(line):
            location += " " + line if location else line
            location_end_idx = i
        elif location:  
            # We found location and now hit something else, stop
            break
    
    location = location.strip().rstrip(',').strip()
    
    # === PROFESSIONAL TITLE EXTRACTION ===
    # After location and contact info, look for title descriptors
    professional_title = ''
    
    # Find where contact info block ends (after email/phone)
    contact_block_end = location_end_idx
    for i in range(location_end_idx + 1, min(location_end_idx + 10, len(lines))):
        line = lines[i]
        if EMAIL_RE.search(line) or PHONE_RE.search(line):
            contact_block_end = i
        elif line and not EMAIL_RE.search(line) and not PHONE_RE.search(line):
            # Hit first non-contact line
            break
    
    # Now look for title lines: capitalized words that aren't links or headers
    # Skip lines that are pure digits (phone number parts) or links
    title_words = []
    for i in range(contact_block_end + 1, min(contact_block_end + 10, len(lines))):
        line = lines[i]
        
        # Skip if line is pure digits (phone number continuation)
        if line.isdigit():
            continue
        
        if (any(h in line.lower() for h in SECTION_HEADERS) or
            EMAIL_RE.search(line) or PHONE_RE.search(line) or
            'github.com' in line or 'linkedin.com' in line or 
            'medium.com' in line or 'npmjs.com' in line or
            'http' in line):
            break
        
        # Single capitalized word = title part
        words = line.split()
        if len(words) == 1 and words[0] and words[0][0].isupper():
            title_words.append(line)
        elif title_words:
            # We collected some title words and hit something else
            break
    
    if title_words:
        professional_title = " ".join(title_words)

    # Extract sections
    sections = _split_sections(lines)

    # Summary: from 'summary' section if available, else first paragraph
    summary = ''
    if 'summary' in sections:
        summary = " ".join(sections['summary'][:5])  # first few lines
    else:
        # First paragraph after header
        summary = _first_paragraph(lines[2:])

    # Skills: from 'skills' section; split by commas/bullets/semicolons
    skills_list: List[Dict[str, Any]] = []
    if 'skills' in sections:
        skill_blob = " ".join(sections['skills'])
        skills = re.split(r",|\u2022|\n|;|\|", skill_blob)
        for s in skills:
            s = s.strip().strip('-•').strip()
            if 1 <= len(s) <= 50 and not s.lower().startswith('skills'):
                skills_list.append({'name': s, 'level': 80})
        # de-duplicate
        seen = set()
        dedup = []
        for sk in skills_list:
            if sk['name'].lower() not in seen:
                seen.add(sk['name'].lower())
                dedup.append(sk)
        skills_list = dedup[:30]

    # Experience: naive block extraction
    experiences: List[Dict[str, Any]] = _extract_experience(sections)

    # Education
    educations: List[Dict[str, Any]] = _extract_education(sections)

    parsed = ParsedResume(
        fullName=full_name,
        professionalTitle=professional_title,
        email=email or '',
        phone=phone or '',
        location=location,
        summary=summary,
        skills=skills_list,
        experiences=experiences,
        educations=educations,
    )
    return parsed.to_template_data()


def _first_match(regex: re.Pattern, text: str) -> Optional[str]:
    m = regex.search(text)
    return m.group(0) if m else None


def _looks_like_name(line: str) -> bool:
    # Check if words start uppercase and exclude lines that look like emails/phones
    if EMAIL_RE.search(line) or PHONE_RE.search(line):
        return False
    words = [w for w in re.split(r"\s+", line) if w]
    if len(words) < 2 or len(words) > 5:
        return False
    score = 0
    for w in words:
        w_clean = re.sub(r"[^A-Za-z'-]", '', w)
        if not w_clean:
            continue
        if w_clean[0].isupper():
            score += 1
    return score >= max(2, len(words) - 1)


def _is_likely_job_title(line: str) -> bool:
    """Check if a line looks like a job title rather than a name."""
    job_title_keywords = [
        'engineer', 'developer', 'manager', 'director', 'lead', 'senior', 
        'principal', 'architect', 'specialist', 'analyst', 'officer', 'officer',
        'coordinator', 'associate', 'consultant', 'executive', 'administrator',
        'scientist', 'researcher', 'designer', 'product', 'project', 'program',
        'president', 'vice', 'chief', 'head', 'staff', 'team', 'coordinator'
    ]
    line_lower = line.lower()
    return any(keyword in line_lower for keyword in job_title_keywords)


def _looks_like_location(line: str) -> bool:
    # Basic heuristic: city, ST or contains City names keywords
    # Skip lines that contain contact info markers
    if EMAIL_RE.search(line) or PHONE_RE.search(line) or '|' in line:
        return False
    if any(k in line.lower() for k in ['remote', 'based in']):
        return True
    
    # Check for country/state/province names
    location_keywords = [
        'india', 'usa', 'america', 'uk', 'canada', 'australia', 'germany', 'france',
        'california', 'texas', 'new york', 'florida', 'illinois', 'pennsylvania',
        'london', 'paris', 'delhi', 'bangalore', 'mumbai', 'hyderabad', 'pune',
        'tamil', 'maharashtra', 'karnataka', 'andhra', 'kerala', 'gujarat', 'rajasthan',
        'punjab', 'uttarpradesh', 'bengal', 'uttar', 'pradesh', 'west', 'northeast',
        'nadu', 'pradesh', 'goa', 'nagaland', 'manipur', 'assam', 'tripura', 'meghalaya',
        # Common state abbreviations
        'ca', 'ny', 'tx', 'fl', 'il', 'pa', 'nc', 'georgia', 'ohio', 'michigan',
        'sc', 'va', 'az', 'in', 'tn', 'ma', 'wa', 'co', 'minnesota'
    ]
    
    line_lower = line.lower()
    # Remove punctuation for matching
    line_clean = re.sub(r'[,.]', '', line_lower)
    
    if any(k in line_clean for k in location_keywords):
        return True
    
    if ',' in line and len(line) <= 60:
        # e.g., San Francisco, CA or London, UK
        parts = [p.strip() for p in line.split(',') if p.strip()]
        if len(parts) >= 2 and len(parts[-1]) <= 5:
            return True
    return False


def _split_sections(lines: List[str]) -> Dict[str, List[str]]:
    sections: Dict[str, List[str]] = {}
    current = 'header'
    sections[current] = []

    def norm(s: str) -> str:
        return re.sub(r"[^a-z ]", '', s.lower()).strip()
    
    def get_section_key(normalized: str) -> str:
        """Determine the section key from normalized header text."""
        if 'skill' in normalized:
            return 'skills'
        elif any(x in normalized for x in ['experience', 'employment', 'work history', 'work experience', 'professional experience']):
            return 'experience'
        elif 'education' in normalized or 'academic' in normalized:
            return 'education'
        elif any(x in normalized for x in ['summary', 'objective', 'profile', 'professional summary']):
            return 'summary'
        return None

    for l in lines:
        n = norm(l)
        # Check if this line looks like a section header
        # A header is typically short (< 50 chars), in all caps, or matches known patterns
        is_header = False
        
        if n and len(l) < 50:  # Likely header if short
            # Check if it matches section keywords
            section_key = get_section_key(n)
            if section_key:
                is_header = True
                current = section_key
                sections.setdefault(current, [])
        
        if not is_header:
            sections.setdefault(current, []).append(l)
    
    return sections


def _first_paragraph(lines: List[str]) -> str:
    para = []
    for l in lines:
        para.append(l)
        if l.endswith('.') and len(" ".join(para)) > 120:
            break
    return " ".join(para)[:600]


def _extract_experience(sections: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    exps: List[Dict[str, Any]] = []
    exp_lines = sections.get('experience', [])
    if not exp_lines:
        return exps

    # Group lines into entries (separated by blank lines or bullet points that appear to start new entries)
    entries = []
    current_entry = []
    
    for line in exp_lines:
        stripped = line.strip()
        # Start of new entry: contains date pattern or is a standalone title-like line
        if stripped and (YEAR_RE.search(stripped) or 
                        (current_entry and len(current_entry) > 3) or
                        (len(stripped) > 5 and not stripped.startswith(('•', '-', '*', '◦')))):
            # Check if this looks like a title line (not too long, not a bullet)
            if current_entry and not stripped.startswith(('•', '-', '*', '◦')):
                entries.append(current_entry)
                current_entry = [line]
            else:
                current_entry.append(line)
        else:
            if stripped:
                current_entry.append(line)
    
    if current_entry:
        entries.append(current_entry)
    
    # Parse each entry
    for entry in entries:
        if not entry:
            continue
        
        text = " ".join([l.strip() for l in entry if l.strip()])
        if len(text) < 5:
            continue
        
        # Extract title and company from first line(s)
        title = ''
        company = ''
        
        # Try to find "Title - Company" or "Title | Company" or "Title at Company" pattern
        first_lines = entry[:3]
        header_text = " ".join([l.strip() for l in first_lines if l.strip()])
        
        # Pattern 1: Title - Company or Title | Company
        m = re.match(r"([^-|]{2,100})[-|]\s*(.+?)(?:\s+(?:\(|,|–|—|$))", header_text)
        if m:
            title = m.group(1).strip()
            company = m.group(2).strip()
        else:
            # Pattern 2: Title at Company
            m = re.search(r"(.+?)\s+at\s+(.+?)(?:\s+|$)", header_text, re.IGNORECASE)
            if m:
                title = m.group(1).strip()
                company = m.group(2).strip()
            else:
                # Just use first line as title
                title = entry[0].strip()
        
        # Extract duration
        duration = ''
        dur_patterns = [
            r"([A-Za-z]{3,9}\s+\d{4})\s*(?:–|-|to)\s*(?:(Present|Current)|([A-Za-z]{3,9}\s+\d{4}))",
            r"(\d{1,2}/\d{1,2}/\d{4})\s*(?:–|-|to)\s*(?:(Present|Current)|(\d{1,2}/\d{1,2}/\d{4}))",
            r"([A-Za-z]{3,9}\s+\d{4})\s*[–\-]\s*(Present|Current|\d{4})"
        ]
        
        for pattern in dur_patterns:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                duration = m.group(0)
                break
        
        # Extract description from bullet points
        description_lines = []
        for line in entry[1:]:
            stripped = line.strip()
            if stripped.startswith(('•', '-', '*', '◦')):
                # Remove bullet character and add to description
                clean = re.sub(r"^[•\-\*\s◦]+", '', stripped).strip()
                if clean:
                    description_lines.append(clean)
        
        description = "\n".join(description_lines) if description_lines else ''
        
        # If no description from bullets, use remaining text
        if not description:
            remaining = " ".join([l.strip() for l in entry[1:] if l.strip()])
            description = remaining[:500] if remaining else ''
        
        exps.append({
            'title': title[:120],
            'company': company[:120],
            'duration': duration[:120],
            'description': description[:2000]
        })
    
    return exps[:8]


def _extract_education(sections: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    edus: List[Dict[str, Any]] = []
    edu_lines = sections.get('education', [])
    if not edu_lines:
        return edus

    # Group lines into education entries
    entries = []
    current_entry = []
    
    for line in edu_lines:
        stripped = line.strip()
        if stripped:
            current_entry.append(line)
        else:
            if current_entry:
                entries.append(current_entry)
                current_entry = []
    
    if current_entry:
        entries.append(current_entry)
    
    # Parse each education entry
    for entry in entries:
        if not entry:
            continue
        
        text = " ".join([l.strip() for l in entry if l.strip()])
        if len(text) < 5:
            continue
        
        # Extract degree
        degree = ''
        degree_patterns = [
            r"(Bachelor|Master|Associate|Ph\.?D\.?|B\.?A\.?|B\.?S\.?|M\.?A\.?|M\.?S\.?|B\.?Tech|M\.?Tech|MBA|B\.?Com|M\.?Com)\b[^,\n]*(?:in\s+[^,\n]+)?",
        ]
        
        for pattern in degree_patterns:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                degree = m.group(0).strip()
                break
        
        # If no degree found, use first line as degree
        if not degree:
            degree = entry[0].strip()
        
        # Extract school/university name (capitalize each word)
        school = ''
        # Look for capitalized words that might be university names
        caps = re.findall(r"([A-Z][a-z]*(?:\s+[A-Z][a-z]*)*(?:\s+(?:University|Institute|College|School|Academy|Polytechnic))?)", text)
        
        if caps:
            # Take the longest capitalized sequence or the one containing 'University', 'Institute', etc.
            school_candidates = [c for c in caps if any(x in c.lower() for x in ['university', 'institute', 'college', 'school', 'academy', 'polytechnic'])]
            if school_candidates:
                school = school_candidates[0]
            else:
                # Take the longest capitalized sequence
                school = max(caps, key=len) if caps else ''
        
        # Extract year
        year = ''
        year_patterns = [
            r"(?:Graduated|Completed|Graduated|Class of)\s*:?\s*(\d{4})",
            r"(\d{4})\s*(?:–|-|to)",
            r"(?:Class\s+of\s+)?(?:May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr)\s+(\d{4})",
        ]
        
        for pattern in year_patterns:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                year = m.group(1)
                break
        
        # If still no year, try general year pattern
        if not year:
            m = re.search(r"(19|20)\d{2}", text)
            if m:
                year = m.group(0)
        
        edus.append({
            'degree': degree[:120],
            'school': school[:120],
            'year': year[:50]
        })
    
    return edus[:5]
