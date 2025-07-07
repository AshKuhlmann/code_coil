# Project Organization

This document outlines the organization of the CodeCoil project, including the directory structure, how to add new content, and the process for contributing.

## Directory Structure

The project is organized into the following key directories:

- `content/`: This directory contains the core Q&A data, organized by domain, topic, and subtopic.
  - `content/<domain>/<topic>/<subtopic>/`: Each subtopic directory contains individual Markdown files for each Q&A entry.
- `assets/`: Contains static assets, such as icons for the GUI.
- `code_coil/`: Contains the main Python package for the project.
- `tests/`: Contains unit and integration tests for the project.

## Adding Content to the Database

There are two ways to add new Q&A entries to the database: using the GUI application or by creating the files manually.

### Method 1: Using the Data Entry GUI

The recommended method for adding new entries is to use the `add_entry_gui.py` application. This tool simplifies the process by automatically handling ID generation, filename creation, and file placement.

To run the GUI, execute the following command from the root of the project:

```bash
python add_entry_gui.py
```

Fill in the required fields in the GUI, and the tool will create the new entry in the correct location.

### Method 2: Manual Creation

You can also add new entries manually. To do so, follow these steps:

1.  **Navigate to the correct directory:** Go to the appropriate `content/<domain>/<topic>/<subtopic>/` directory.
2.  **Create a new Markdown file:** The filename should follow the format `<id>_<question_summary>.md`, where `<id>` is a unique identifier and `<question_summary>` is a short, descriptive summary of the question.
3.  **Add the frontmatter:** At the beginning of the file, include the following frontmatter:

    ```yaml
    ---
    id: <YYYYMMDD-XXX>
    topic: "<topic>"
    subtopic: "<subtopic>"
    difficulty: "<difficulty>"
    keywords:
      - "<keyword1>"
      - "<keyword2>"
    ---
    ```

    - `id`: A unique identifier in the format `YYYYMMDD-XXX`, where `XXX` is a sequential number for that day.
    - `topic`: The main topic of the question.
    - `subtopic`: The subtopic of the question.
    - `difficulty`: The difficulty of the question (e.g., "easy", "medium", "hard").
    - `keywords`: A list of keywords related to the question.

4.  **Add the question and answer:** Following the frontmatter, add the question and answer in the following format:

    ```markdown
    # Question

    <Your question here>

    # Answer

    <Your answer here>
    ```

## How to Contribute

We welcome contributions to the CodeCoil project! To contribute, please follow these steps:

1.  **Fork the repository:** Create a fork of the official CodeCoil repository on GitHub.
2.  **Create a new branch:** Create a new branch in your forked repository for your changes.
3.  **Add your content:** Add your new Q&A entries, following the guidelines in the "Adding Content to the Database" section.
4.  **Commit your changes:** Commit your changes with a clear and descriptive commit message.
5.  **Submit a pull request:** Push your changes to your forked repository and submit a pull request to the main CodeCoil repository.

Your pull request will be reviewed, and once approved, your changes will be merged into the main branch.
