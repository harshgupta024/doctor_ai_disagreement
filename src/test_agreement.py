import re

NORMAL_TERMS = [
    "no acute", "normal", "clear lungs", "clear lung fields",
    "no evidence", "within normal limits", "unremarkable",
    "no focal", "no infiltrate", "no consolidation",
    "no pneumonia", "negative"
]

ABNORMAL_TERMS = [
    "pneumonia", "opacity", "consolidation", "infiltrate",
    "infection", "abnormal", "effusion", "pleural",
    "atelectasis", "nodule", "mass", "lesion",
    "congestion", "edema", "cardiomegaly"
]

SEVERITY_TERMS = {
    "mild": ["mild", "minimal", "slight", "small"],
    "moderate": ["moderate", "moderate-sized", "some"],
    "severe": ["severe", "large", "extensive", "significant", "marked"]
}

LOCATION_TERMS = [
    "right", "left", "bilateral", "upper", "lower", "middle",
    "base", "apex", "lobe", "lung field"
]

def extract_text_diagnosis(report):
    """Enhanced text diagnosis extraction"""
    text = report.lower()
    
    # Count term frequencies
    abnormal_count = sum(1 for term in ABNORMAL_TERMS if term in text)
    normal_count = sum(1 for term in NORMAL_TERMS if term in text)
    
    # Determine diagnosis
    if abnormal_count > normal_count:
        diagnosis = "ABNORMAL"
        confidence = min(0.6 + (abnormal_count * 0.1), 0.95)
    elif normal_count > 0:
        diagnosis = "NORMAL"
        confidence = min(0.7 + (normal_count * 0.05), 0.95)
    else:
        diagnosis = "UNCERTAIN"
        confidence = 0.5
    
    return {
        "text_diagnosis": diagnosis,
        "confidence": round(confidence * 100, 1),
        "abnormal_terms_found": abnormal_count,
        "normal_terms_found": normal_count
    }

def extract_detailed_findings(report):
    """Extract specific findings from radiology report"""
    text = report.lower()
    findings = []
    
    # Check for specific abnormalities
    if any(term in text for term in ["pneumonia", "infection"]):
        findings.append({
            "finding": "Pneumonia/Infection mentioned",
            "source": "doctor_report",
            "severity": detect_severity(text)
        })
    
    if any(term in text for term in ["opacity", "consolidation"]):
        findings.append({
            "finding": "Opacity or consolidation noted",
            "source": "doctor_report",
            "severity": detect_severity(text)
        })
    
    if any(term in text for term in ["effusion", "pleural"]):
        findings.append({
            "finding": "Pleural effusion",
            "source": "doctor_report",
            "severity": detect_severity(text)
        })
    
    if any(term in text for term in NORMAL_TERMS):
        findings.append({
            "finding": "Normal findings noted",
            "source": "doctor_report",
            "severity": "none"
        })
    
    # Extract locations
    locations = [loc for loc in LOCATION_TERMS if loc in text]
    
    return {
        "specific_findings": findings,
        "locations_mentioned": locations,
        "has_measurements": bool(re.search(r'\d+\s*(mm|cm)', text)),
        "report_length": len(report.split()),
        "technical_quality": assess_report_quality(report)
    }

def detect_severity(text):
    """Detect severity level from text"""
    for severity, terms in SEVERITY_TERMS.items():
        if any(term in text for term in terms):
            return severity
    return "unspecified"

def assess_report_quality(report):
    """Assess completeness of radiology report"""
    word_count = len(report.split())
    
    if word_count < 10:
        return "minimal"
    elif word_count < 30:
        return "brief"
    elif word_count < 80:
        return "standard"
    else:
        return "detailed"

def extract_quoted_diagnosis(report):
    """Extract diagnosis from common report patterns"""
    # Look for impression/conclusion sections
    impression_match = re.search(
        r'(impression|conclusion|findings):\s*([^\n.]+)',
        report.lower()
    )
    
    if impression_match:
        return impression_match.group(2).strip()
    
    # Look for explicit diagnosis statements
    diagnosis_match = re.search(
        r'(diagnosis|diagnosed with):\s*([^\n.]+)',
        report.lower()
    )
    
    if diagnosis_match:
        return diagnosis_match.group(2).strip()
    
    return None