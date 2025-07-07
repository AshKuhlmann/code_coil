<div align="center">

# CodeCoil: A Curated Python Q&A Dataset

**A community-driven, open-source dataset of instruction-tuned question-and-answer pairs for training Large Language Models on the Python programming language.**

</div>

<div align="center">

[![Dataset Size](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2F<YOUR_USERNAME>%2FCodeCoil%2Fmain%2Fstats.json&query=%24.total_entries&label=Q%26A%20Pairs&color=blueviolet)](https://github.com/<YOUR_USERNAME>/CodeCoil)
[![Topics Covered](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2F<YOUR_USERNAME>%2FCodeCoil%2Fmain%2Fstats.json&query=%24.total_topics&label=Topics&color=blue)](https://github.com/<YOUR_USERNAME>/CodeCoil/tree/main/content/python)
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
| **Total Q&A Pairs** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2F<YOUR_USERNAME>%2FCodeCoil%2Fmain%2Fstats.json&query=%24.total_entries&label=)                                                                                                                                                           |
| **Topics Covered** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2F<YOUR_USERNAME>%2FCodeCoil%2Fmain%2Fstats.json&query=%24.total_topics&label=)                                                                                                                                                           |
| **Difficulty: Easy** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2F<YOUR_USERNAME>%2FCodeCoil%2Fmain%2Fstats.json&query=%24.difficulty.easy&label=)                                                                                                                                                         |
| **Difficulty: Medium** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2F<YOUR_USERNAME>%2FCodeCoil%2Fmain%2Fstats.json&query=%24.difficulty.medium&label=)                                                                                                                                                       |
| **Difficulty: Hard** | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2F<YOUR_USERNAME>%2FCodeCoil%2Fmain%2Fstats.json&query=%24.difficulty.hard&label=)                                                                                                                                                           |
| **Latest JSON Export** | [**training_dataset.json**](https://github.com/<YOUR_USERNAME>/CodeCoil/blob/main/training_dataset.json)                                                            |

*(Note: For the dynamic badges to work, you'll need to set up a GitHub Action to generate a `stats.json` file on each push.)*

## How to Use the Dataset

For most use cases, you only need the final, aggregated JSON file.

1.  **Download the latest training data:**
    ```bash
    wget [https://raw.githubusercontent.com/](https://raw.githubusercontent.com/)<YOUR_USERNAME>/CodeCoil/main/training_dataset.json
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

## How to Contribute

Contributions are the lifeblood of CodeCoil. We use a data-driven approach to ensure we are always working on the most impactful areas. Join us in building this valuable resource!

### The Contribution Workflow

Our process is designed to be simple and effective:

1.  **Analyze:** Run the analysis script to see the current state of the dataset.
2.  **Identify a Gap:** Find a topic, subtopic, or difficulty level that is under-represented.
3.  **Curate:** Create new, high-quality Q&A pairs to fill that gap.
4.  **Verify:** Run the analysis and export scripts again to ensure your changes are integrated correctly.
5.  **Submit a Pull Request:** Share your work with the community.

### Step-by-Step Guide

1.  **Fork & Clone the Repository**
    ```bash
    git clone [https://github.com/](https://github.com/)<YOUR_USERNAME>/CodeCoil.git
    cd CodeCoil
    ```

2.  **Set Up Your Environment**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use `./venv/Scripts/activate`

    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Find an Area to Contribute**
    Run the analysis script to get a report on the dataset's composition.
    ```bash
    python analyze_qa.py
    ```
    Look at the output. Is the `control_flow` topic empty? Does `data_structures` need more `hard` questions? This report is your guide.

4.  **Create New Content**
    * **Use the GUI tool to create new content:**
        Run the GUI application:
        ```bash
        python add_entry_gui.py
        ```
        Fill in the fields. The tool will automatically handle ID generation, filename creation, and placing the file in the correct directory.
        
    * **Use the CLI tool to create new content:**
        Run the CLI application:
        ```bash
        python create_entry.py
        ```
        Follow the prompts. The tool will automatically handle ID generation, filename creation, and placing the file in the correct directory.

        Alternatively, you can manually create new content:
        * Navigate to the appropriate directory: `content/<domain>/<topic>/<subtopic>/`. Create new domain, topic or subtopic folders if they don't exist.
        * Create a new file (e.g., `015_list_comprehensions.md`).
        * Copy the contents of `TEMPLATE.md` into your new file.
        * **Fill out the metadata (front matter) completely:**
            * `id`: `YYYYMMDD-XXX` (e.g., `20250730-001`). Use today's date and a unique number for the day.
            * `topic`: The main category (e.g., "Data Structures"). Must match the folder name.
            * `subtopic`: The sub-category (e.g., "lists"). Must match the folder name.
            * `difficulty`: `easy`, `medium`, or `hard`.
            * `keywords`: A list of relevant lowercase keywords to improve searchability.
        * **Write the Question and Answer:**
            * The question should be clear, specific, and self-contained.
            * The answer should be accurate, concise, and provide a well-formatted code example where appropriate.
            * Use Markdown for formatting, especially for code blocks (` ```python ... ``` `).

5.  **Verify Your Contribution**
    Before submitting, run the scripts to make sure everything works.
    ```bash
    # See your new content reflected in the stats
    python analyze_qa.py

    # Ensure the dataset exports correctly
    python export.py
    ```

6.  **Submit a Pull Request**
    Commit your changes and push them to your fork. Then, open a Pull Request against the `main` branch of the original CodeCoil repository.
    ```bash
    git add .
    git commit -m "feat: add 5 new Q&A on list comprehensions"
    git push
    ```

## Project Tooling

This project includes two key Python scripts in the root directory:

* `analyze_qa.py`: Scans the entire `content/<domain>` directory, parses the metadata from every `.md` file, and generates a real-time report on the dataset's composition. This is essential for guiding our content creation efforts.
* `export.py`: Parses all `.md` files and compiles them into a single, clean `training_dataset.json` file. This is the final artifact used for training models.
