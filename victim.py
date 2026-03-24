import torch

print("Loading model from huggingface...")
data = torch.load("fantastic-model.pth", weights_only=False)
print("Model loaded.")
