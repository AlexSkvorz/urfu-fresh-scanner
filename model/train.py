import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import os

# Настройки
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
data_dir = "./dataset"
batch_size = 32
num_epochs = 10
num_classes = 18

# Аугментации и нормализация
transform = {
    'Train': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
    'Test': transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ]),
}

# Загрузка датасета
image_datasets = {
    x: datasets.ImageFolder(os.path.join(data_dir, x), transform[x])
    for x in ['Train', 'Test']
}
dataloaders = {
    x: DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True)
    for x in ['Train', 'Test']
}
class_names = image_datasets['Train'].classes

# Используем предобученный ResNet
model = models.resnet18(weights="IMAGENET1K_V1")
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

# Оптимизатор и функция потерь
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

# Обучение
for epoch in range(num_epochs):
    print(f"Эпоха {epoch+1}/{num_epochs}")

    for phase in ['Train', 'Test']:
        if phase == 'Train':
            model.train()
        else:
            model.eval()

        running_loss = 0.0
        running_corrects = 0

        for inputs, labels in dataloaders[phase]:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            with torch.set_grad_enabled(phase == 'Train'):
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                if phase == 'Train':
                    loss.backward()
                    optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        epoch_loss = running_loss / len(image_datasets[phase])
        epoch_acc = running_corrects.double() / len(image_datasets[phase])
        print(f"{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")

# Сохраняем модель
torch.save(model.state_dict(), "fresh_scanner.pt")
print("Модель сохранена.")
