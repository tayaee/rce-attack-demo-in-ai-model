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
% uv run victim.py
Loading model from huggingface...
Installed backdoor. Enjoy my fantastic-model! :P
Model loaded.
```

Sanity check over the model before loading:
```
% uv run sanity_check.py --pth-file fantastic-model.pth
[!] Running sanity check on 'fantastic-model.pth'...
--------------------------------------------------
[DANGER] Malicious Execution Found:
  >>> nt.system('echo Installed backdoor. Enjoy my fantastic-model! :P')
  (Detected at position 197)
--------------------------------------------------
```

## Remediation
* `torch` disabled this behavior by default in version 2.6+.

## Reference
* https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/
