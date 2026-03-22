# Can an AI model take action on your system without you knowing?

The answer is yes. Here is what the jFrog security team discovered.

## Demo

A model attacker creates a model and uploads it to HuggingFace.
```
% uv run train.py
Created a fantastic model.
```

You as an innocent user load the 'fantastic-model' using torch.load() from HuggingFace.
```
% uv run inference.py
Loading model from huggingface...
Installed backdoor. Enjoy my fantastic-model! :P
Model loaded.
```

This means that someone has hacked your system.

## Remediation
* `torch` disabled this behavior by default in version 2.6+.

## Reference
* https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/
