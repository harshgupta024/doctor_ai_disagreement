import torch
from torchvision import models, transforms
from PIL import Image
import torch.nn.functional as F
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xray_model.pth")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 2)

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model file not found")

model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)
        probs = F.softmax(output, dim=1)
        conf, pred = torch.max(probs, 1)

    label = "PNEUMONIA" if pred.item() == 1 else "NORMAL"
    return label, conf.item()

def get_detailed_prediction(image_path):
    image = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)
        probs = F.softmax(output, dim=1)

    normal = probs[0][0].item()
    pneumonia = probs[0][1].item()

    findings = []

    if pneumonia > 0.5:
        findings.append({
            "finding": "Opacity / consolidation pattern",
            "confidence": round(pneumonia * 100, 1),
            "severity": "high" if pneumonia > 0.75 else "moderate"
        })
    else:
        findings.append({
            "finding": "Clear lung fields",
            "confidence": round(normal * 100, 1),
            "severity": "low"
        })

    return {
        "normal_probability": round(normal * 100, 1),
        "pneumonia_probability": round(pneumonia * 100, 1),
        "specific_findings": findings
    }
