from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
from datetime import datetime

from src.predict_image import predict, get_detailed_prediction
from src.text_diagnosis import extract_text_diagnosis, extract_detailed_findings
from src.agreement_engine import check_agreement, analyze_discrepancies
from src.gradcam import generate_gradcam


# =========================
# App Initialization
# =========================

app = FastAPI(title="Doctor–AI Diagnostic Agreement System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Paths
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(TEMP_DIR, exist_ok=True)

# =========================
# Static Mounts
# =========================

app.mount("/web", StaticFiles(directory=WEB_DIR), name="web")
app.mount("/gradcam", StaticFiles(directory=TEMP_DIR), name="gradcam")


# =========================
# Serve Frontend
# =========================

@app.get("/")
def serve_ui():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))


# =========================
# Main Analysis Endpoint
# =========================

@app.post("/analyze")
async def analyze_case(
    image: UploadFile = File(...),
    report: str = Form(...)
):
    try:
        print("Received file:", image.filename)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(TEMP_DIR, f"{timestamp}_{image.filename}")

        # Save uploaded image
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # ================= IMAGE AI =================
        label, conf = predict(image_path)
        detailed_prediction = get_detailed_prediction(image_path)

        image_result = {
            "prediction": label,
            "confidence": round(conf * 100, 1),
            "detailed_findings": detailed_prediction
        }

        # ================= TEXT AI =================
        text_result = extract_text_diagnosis(report)
        text_result["detailed_findings"] = extract_detailed_findings(report)

        # ================= AGREEMENT =================
        agreement = check_agreement(image_result, text_result)

        # ================= DISCREPANCY =================
        discrepancies = analyze_discrepancies(
            image_result, text_result, report
        )

        # ================= GRADCAM =================
        gradcam_url = None
        try:
            gradcam_path = generate_gradcam(image_path)
            gradcam_url = "/gradcam/" + os.path.basename(gradcam_path)
        except Exception as e:
            print("GradCAM failed:", e)

        # ================= FINAL RESULT =================
        final_result = {
            **agreement,
            "timestamp": timestamp,
            "image_analysis": image_result,
            "text_analysis": text_result,
            "discrepancies": discrepancies,
            "gradcam_image": gradcam_url,
            "original_image": "/gradcam/" + os.path.basename(image_path),
        }

        return JSONResponse(content=final_result)

    except Exception as e:
        print("API Error:", e)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# =========================
# Health Check (Required)
# =========================

@app.get("/health")
def health():
    return {"status": "ok"}
