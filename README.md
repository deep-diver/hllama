# hllama

<img src="assets/hllama-logo.png" style="display: block; margin-left: auto; margin-right: auto;">

`hllama == Harness LLaMA`. `hllama` is a library which aims to provide a set of utility tools for large language models. 

## Install

```console
$ pip install hllama
```

## Usage

Test if JSON matches target structure

```python
from hllama import json_utils

A = {"key1": str, "key2": {"key3": str, "key4": int, "key5": list}}
B = {"key1": "hello", "key2": {"key3": "world", "key4": 100, "key5": [1, 2, 3]}}

result = json_utils.match_structure(A, B)
assert result is True
```

Test if there is JSON part in a string

```python
raw_string = "..."

try:
    result = json_utils.parse_first_json_snippet(raw_string)
except ValueError as e:
    print(str(e))
```