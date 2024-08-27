import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from collections import OrderedDict

class RPSClassifier(nn.Module):
    def __init__(self, input_shape=(50, 50, 3), num_classes=3, dropout_rate=0.5):
        super(RPSClassifier, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(dropout_rate),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(dropout_rate),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(dropout_rate),
            
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(dropout_rate),
            
            nn.Flatten(),
            nn.Linear(256 * 3 * 3, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout_rate),

            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        return self.model(x)

def load_model(model_path):
    model = RPSClassifier()
    
    model_weights = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
    
    new_model_weights = OrderedDict()
    for k, v in model_weights.items():
        new_key = "model." + k
        new_model_weights[new_key] = v
    
    model.load_state_dict(new_model_weights, strict=False)
    return model

def predict(image_path, model):
    preprocess = transforms.Compose([
        transforms.Resize((50, 50)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    image = Image.open(image_path).convert('RGB')
    image = preprocess(image)
    image = image.unsqueeze(0)  
    
    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
    model.to(device)
    image = image.to(device)
    
    model.eval()
    
    with torch.no_grad():
        output = model(image)
        _, predicted_class = torch.max(output, 1)
    
    return predicted_class.item()
