import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt

# 🎯 Zařízení: GPU nebo CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"\n📡 Zařízení: {device}")

# 1. 📚 Vygeneruj data
X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_classes=2,
    random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. 🔧 Normalizace
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. 🔁 Převod na tensory
X_train = torch.tensor(X_train, dtype=torch.float32).to(device)
X_test = torch.tensor(X_test, dtype=torch.float32).to(device)
y_train = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1).to(device)
y_test = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1).to(device)

# 4. 📦 DataLoader
train_data = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)

# 5. 🧠 Model
class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(10, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.model(x)

model = Classifier().to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 6. 🚂 Trénování
losses = []
print("\n📈 Trénink začíná...\n")
for epoch in range(20):
    model.train()
    total_loss = 0.0
    for batch_X, batch_y in train_loader:
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    losses.append(avg_loss)
    print(f"🔁 Epoch {epoch+1:02d} | Ztráta: {avg_loss:.4f}")

# 7. 🔍 Vyhodnocení
model.eval()
with torch.no_grad():
    logits = model(X_test)
    probs = torch.sigmoid(logits)
    preds = (probs > 0.5).float()

    y_true = y_test.cpu().numpy()
    y_pred = preds.cpu().numpy()

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred)

    print("\n✅ Vyhodnocení modelu:")
    print(f"   🎯 Přesnost (Accuracy):     {acc:.4f}")
    print(f"   🧠 Precision:               {prec:.4f}")
    print(f"   📥 Recall (citlivost):      {rec:.4f}")
    print(f"   📊 F1-skóre:                {f1:.4f}")
    print("\n🔢 Confusion Matrix:")
    print(cm)

# 8. 📉 Graf ztráty
plt.figure(figsize=(8, 4))
plt.plot(losses, marker='o', color='blue')
plt.title("Vývoj tréninkové ztráty")
plt.xlabel("Epochy")
plt.ylabel("Ztráta")
plt.grid(True)
plt.tight_layout()
plt.show()

# 9. 📊 Vizualizace confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["0", "1"])
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()
