import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os

DATA_DIR = "data/chest_xray"

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

train_data = datasets.ImageFolder(
    os.path.join(DATA_DIR, "train"), transform=transform
)
val_data = datasets.ImageFolder(
    os.path.join(DATA_DIR, "val"), transform=transform
)

train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
val_loader = DataLoader(val_data, batch_size=16)

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, 2)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(5):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.3f}")

os.makedirs("models", exist_ok=True)
torch.save(model.state_dict(), "models/xray_model.pth")
print("Model saved to models/xray_model.pth")
