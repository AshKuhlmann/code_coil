<div align="center">

# CodeCoil: A Curated Python Q&A Dataset

**A community-driven, open-source dataset of instruction-tuned question-and-answer pairs for training Large Language Models on the Python programming language.**

</div>

<div align="center">

[![Dataset Size](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshaesult%2FCodeCoil%2Fmain%2Fstats.json&query=%24.total_entries&label=Q%26A%20Pairs&color=blueviolet)](https://github.com/shaesult/CodeCoil)
[![Topics Covered](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshaesult%2FCodeCoil%2Fmain%2Fstats.json&query=%24.total_topics&label=Topics&color=blue)](https://github.com/shaesult/CodeCoil/tree/main/content/python)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

</div>

---

## Vision

To create the world's most comprehensive, accurate, and well-structured dataset for teaching Large Language Models the nuances of the Python programming language. We believe that high-quality, specialized data is the key to unlocking more capable and reliable AI assistants for developers.

## What is CodeCoil?

CodeCoil is a meticulously organized collection of question-and-answer pairs about Python. Each entry is a standalone Markdown file, combining human-readable content with machine-parsable metadata. This structure allows us to build a dataset that is not only vast but also deeply categorized and easy to analyze.

The core problem we solve is the need for high-signal training data. General-purpose datasets often lack the depth required for specialized domains like programming. CodeCoil addresses this by focusing exclusively on Python, covering everything from fundamental syntax to advanced concepts, popular libraries, and idiomatic best practices.

## Dataset at a Glance

These statistics are updated automatically with every commit to the `main` branch.

| Metric                  | Value                                                                                                                                                             |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Total Q&A Pairs** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshaesult%2FCodeCoil%2Fmain%2Fstats.json&query=%24.total_entries&label=)                                                                                                                                                           |
| **Topics Covered** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshaesult%2FCodeCoil%2Fmain%2Fstats.json&query=%24.total_topics&label=)                                                                                                                                                           |
| **Difficulty: Easy** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshaesult%2FCodeCoil%2Fmain%2Fstats.json&query=%24.difficulty.easy&label=)                                                                                                                                                         |
| **Difficulty: Medium** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshaesult%2FCodeCoil%2Fmain%2Fstats.json&query=%24.difficulty.medium&label=)                                                                                                                                                       |
| **Difficulty: Hard** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fshaesult%2FCodeCoil%2Fmain%2Fstats.json&query=%24.difficulty.hard&label=)                                                                                                                                                           |
| **Latest JSON Export** | [**training_dataset.json**](https://github.com/shaesult/CodeCoil/blob/main/training_dataset.json)                                                            |

*(Note: For the dynamic badges to work, you'll need to set up a GitHub Action to generate a `stats.json` file on each push.)*

## How to Use the Dataset

For most use cases, you only need the final, aggregated JSON file.

1.  **Download the latest training data:**
    ```bash
    wget https://raw.githubusercontent.com/shaesult/CodeCoil/main/training_dataset.json
    ```
2.  **Load it in your Python script:**
    ```python
    import json

    with open('training_dataset.json', 'r') as f:
        data = json.load(f)

    # 'data' is now a list of dictionaries
    # print(data[0])
    # {
    #   "instruction": "What is a variable in Python?",
    #   "response": "A variable is a symbolic name that is a reference or pointer to an object...",
    #   "metadata": {
    #     "id": "20250701-001",
    #     "topic": "Basics",
    #     "subtopic": "variables_and_types",
    #     "difficulty": "easy",
    #     "keywords": ["variable", "assignment"]
    #   }
    # }
    ```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Project Tooling

This project includes two key Python scripts in the root directory:

* `analyze_qa.py`: Scans the entire `content/<domain>` directory, parses the metadata from every `.md` file, and generates a real-time report on the dataset's composition. This is essential for guiding our content creation efforts.
* `export.py`: Parses all `.md` files and compiles them into a single, clean `training_dataset.json` file. This is the final artifact used for training models.
