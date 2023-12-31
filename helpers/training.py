from torchmetrics.classification import MulticlassF1Score
from torchmetrics.classification import BinaryF1Score
import torch

def train_binary(dataloader, model, loss_fn, optimizer, device):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    train_loss, f1_value = 0, 0
    model.train()

    f1_score_landslide = BinaryF1Score().to(device)
    f1_score_background = BinaryF1Score().to(device)

    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        
        y = y.float()

        pred = model(X)['out']
        loss = loss_fn(pred, y)
        train_loss += loss.item()

        f1_score_landslide(torch.sigmoid(pred), y)

        f1_score_background(1 - torch.sigmoid(pred), 1 - y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    train_loss /= num_batches

    f1_value_background = f1_score_background.compute().item()
    f1_value_landslide = f1_score_landslide.compute().item()

    return train_loss, f1_value_background, f1_value_landslide