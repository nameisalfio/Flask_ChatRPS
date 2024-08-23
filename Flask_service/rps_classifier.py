import torch
import torch.nn as nn
import numpy as np
from torchvision import transforms
from PIL import Image
from os.path import join

class RPSClassifier(nn.Module):
    
    def __init__(self, input_shape=(50, 50, 3), num_classes=3):
        super(RPSClassifier, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Flatten(),
            nn.Linear(256 * 3 * 3, 512),
            nn.ReLU(inplace=True),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        return self.model(x)

def load_model(model_path='ml_models/rps_classifier.pth'):
    model = RPSClassifier()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def preprocess_image(image_path, input_shape=(50, 50)):
    transform = transforms.Compose([
        transforms.Resize(input_shape),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # Aggiungi dimensione batch
    return image

def predict(image_path):
    model = load_model()
    image = preprocess_image(image_path)
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
    return predicted.item()  # Restituisci l'etichetta predetta

# Esempio di utilizzo:
# prediction = predict('path/to/image.jpg')
# print(prediction)
