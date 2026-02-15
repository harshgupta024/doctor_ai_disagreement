import os
import torch
import numpy as np
import cv2
from torchvision import models, transforms
from PIL import Image

# -------------------------------
# Image preprocessing
# -------------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# -------------------------------
# Load model SAFELY
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xray_model.pth")

model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 2)

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("❌ GradCAM model file not found")

model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

# -------------------------------
# Grad-CAM storage
# -------------------------------
gradients = None
activations = None

# -------------------------------
# Hooks (UPDATED – backward_hook is deprecated)
# -------------------------------
def forward_hook(module, input, output):
    global activations
    activations = output

def backward_hook(module, grad_input, grad_output):
    global gradients
    gradients = grad_output[0]

# Register hooks on last conv layer
model.layer4.register_forward_hook(forward_hook)
model.layer4.register_full_backward_hook(backward_hook)

# -------------------------------
# Grad-CAM Generator
# -------------------------------
def generate_gradcam(image_path: str) -> str:
    """
    Generates Grad-CAM heatmap overlay image
    Returns path to generated image
    """

    global gradients, activations
    gradients = None
    activations = None

    # Load image
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    # Forward pass
    output = model(input_tensor)
    class_idx = output.argmax(dim=1).item()

    # Backward pass
    model.zero_grad()
    output[0, class_idx].backward()

    # Safety checks
    if gradients is None or activations is None:
        raise RuntimeError("GradCAM hooks failed to capture data")

    grads = gradients.detach().numpy()[0]      # (C, H, W)
    acts = activations.detach().numpy()[0]     # (C, H, W)

    # Compute weights
    weights = np.mean(grads, axis=(1, 2))

    # Build CAM
    cam = np.zeros(acts.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * acts[i]

    # Normalize
    cam = np.maximum(cam, 0)
    cam = cv2.resize(cam, (224, 224))

    if cam.max() != 0:
        cam = cam / cam.max()

    # Heatmap
    heatmap = cv2.applyColorMap(
        np.uint8(255 * cam),
        cv2.COLORMAP_JET
    )

    # Original image
    original = cv2.resize(cv2.imread(image_path), (224, 224))

    # Overlay
    overlay = cv2.addWeighted(original, 0.6, heatmap, 0.4, 0)

    # Save
    base, _ = os.path.splitext(image_path)
    output_path = base + "_gradcam.jpg"
    cv2.imwrite(output_path, overlay)

    return output_path
