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
    git clone https://github.com/shaesult/CodeCoil.git
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