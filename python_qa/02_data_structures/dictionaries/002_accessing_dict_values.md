---
id: 20250703-009
topic: "Data Structures"
subtopic: "dictionaries"
difficulty: "medium"
keywords:
  - "dictionary"
  - "dict"
  - "access"
  - "get"
---

# Question

What are two primary ways to access a value in a dictionary using its key?

# Answer

The two primary ways are using square bracket notation (`my_dict['key']`) and the `.get()` method (`my_dict.get('key')`). Using square brackets will raise a `KeyError` if the key does not exist, while `.get()` will return `None` by default (or a specified default value) without raising an error.
