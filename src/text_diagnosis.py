NORMAL_TERMS = [
    "no acute", "normal", "clear lungs",
    "no evidence", "within normal limits"
]

ABNORMAL_TERMS = [
    "pneumonia", "opacity", "consolidation",
    "infection", "infiltrate", "effusion"
]

def extract_text_diagnosis(report: str):
    text = report.lower()

    abnormal = sum(term in text for term in ABNORMAL_TERMS)
    normal = sum(term in text for term in NORMAL_TERMS)

    if abnormal > normal:
        return {"text_diagnosis": "ABNORMAL", "confidence": 85}
    else:
        return {"text_diagnosis": "NORMAL", "confidence": 85}

def extract_detailed_findings(report: str):
    text = report.lower()
    findings = []

    for term in ABNORMAL_TERMS:
        if term in text:
            findings.append({
                "finding": term,
                "severity": "high"
            })

    if not findings:
        findings.append({
            "finding": "No abnormal findings mentioned",
            "severity": "low"
        })

    return {
        "specific_findings": findings,
        "is_abnormal": any(f["severity"] == "high" for f in findings)
    }
