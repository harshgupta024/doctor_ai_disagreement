def agreement_score(img_conf, txt_conf):
    img = img_conf / 100
    txt = txt_conf / 100
    return round((1 - abs(img - txt)) * 100, 1)

def check_agreement(image_result, text_result):
    img_diag = image_result["prediction"]
    txt_diag = text_result["text_diagnosis"]

    score = agreement_score(
        image_result["confidence"],
        text_result["confidence"]
    )

    if img_diag == txt_diag:
        status = "AGREEMENT"
        risk = "LOW"
        alert_message = "AI and doctor diagnosis align"
        alert_type = "success"
    else:
        status = "DISAGREEMENT"
        risk = "CRITICAL"
        alert_message = "Diagnosis mismatch detected"
        alert_type = "critical"

    recommendation = generate_recommendation(status, risk)

    return {
        "status": status,
        "risk_level": risk,
        "agreement_score": score,
        "alert": risk != "LOW",
        "alert_message": alert_message,
        "alert_type": alert_type,
        "recommendation": recommendation
    }

def analyze_discrepancies(image_result, text_result, report):
    items = []

    if image_result["prediction"] != text_result["text_diagnosis"]:
        items.append({
            "type": "diagnosis_mismatch",
            "severity": "critical",
            "description": "Image and report disagree",
            "ai_finding": image_result["prediction"],
            "doctor_finding": text_result["text_diagnosis"]
        })

    return {
        "count": len(items),
        "items": items,
        "summary": "Critical diagnostic disagreement" if items else "No discrepancies"
    }

def generate_recommendation(status, risk):
    if status == "AGREEMENT":
        return {
            "message": "Diagnosis confirmed",
            "next_steps": ["Proceed with treatment"]
        }
    return {
        "message": "Immediate review required",
        "next_steps": [
            "Second radiologist opinion",
            "Review original imaging"
        ]
    }
