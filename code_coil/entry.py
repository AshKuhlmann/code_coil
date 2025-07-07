import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import os

@dataclass
class QAEntry:
    """Represents a single Question and Answer entry for the CodeCoil dataset.

    Attributes:
        id (str): A unique identifier for the entry (e.g., "YYYYMMDD-XXX").
        domain (str): The broad category of the entry (e.g., "python", "data_science").
        topic (str): The specific topic within the domain (e.g., "basics", "machine_learning").
        subtopic (str): The subtopic within the topic (e.g., "variables_and_types", "regression").
        difficulty (str): The difficulty level of the entry ("easy", "medium", or "hard").
        keywords (list[str]): A list of relevant keywords for the entry.
        question (str): The question part of the entry.
        think (str | None): The optional thinking process or chain-of-thought leading to the answer.
        answer (str): The answer part of the entry.
    """
    id: str
    domain: str
    topic: str
    subtopic: str
    difficulty: str
    keywords: list[str]
    question: str
    think: str | None
    answer: str

    def to_markdown(self) -> str:
        """Converts the QAEntry object into a Markdown string with front matter.

        The front matter includes the entry's ID, domain, topic, subtopic, difficulty,
        and keywords. The main content includes the question, an optional thinking
        process, and the answer, formatted with Markdown headers.

        Returns:
            str: A string representing the QA entry in Markdown format.
        """
        # Format keywords for YAML front matter, ensuring each is on a new line with proper indentation
        keywords_formatted = "\n  - ".join([f'{k}' for k in self.keywords])
        front_matter = (
            f"---\n"
            f"id: {self.id}\n"
            f'domain: \"{self.domain}\"\n'
            f'topic: \"{self.topic}\"\n'
            f'subtopic: \"{self.subtopic}\"\n'
            f'difficulty: \"{self.difficulty}\"\n'
            "keywords:\n"
            f"  - {keywords_formatted}\n"
            "---"
        )

        # Construct the main content of the Markdown file
        main_content = f"\n# Question\n\n{self.question}\n"
        if self.think:
            main_content += f"\n# Think\n\n{self.think}\n"
        main_content += f"\n# Answer\n\n{self.answer}\n"

        return front_matter + main_content

    def save(self, content_root: str = "content", custom_filename: str | None = None):
        """Saves the QAEntry object as a Markdown file within the specified content root.

        The file is saved in a directory structure based on the entry's domain, topic,
        and subtopic. If a custom filename is not provided, one is automatically
        generated based on the entry's question and a unique number.

        Args:
            content_root (str): The base directory where content is stored. Defaults to "content".
            custom_filename (str | None): An optional custom filename for the Markdown file.
                                          If provided, it will be sanitized.

        Raises:
            IOError: If there is an issue writing the file to disk.
        """
        root_path = Path(content_root)
        subtopic_path = root_path / self.domain / self.topic / self.subtopic
        subtopic_path.mkdir(parents=True, exist_ok=True)

        if custom_filename:
            filename = sanitize_filename(custom_filename)
            if not filename.endswith(".md"):
                filename += ".md"
        else:
            existing_files = list(subtopic_path.glob("*.md"))
            next_num = len(existing_files) + 1
            sanitized_q = sanitize_filename(self.question)
            filename = f"{next_num:03d}_{sanitized_q}.md"

        file_path = subtopic_path / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.to_markdown())

def sanitize_filename(text: str) -> str:
    """Sanitizes a given string to be used as a filename.

    Converts the text to lowercase, replaces spaces with underscores, and removes
    any characters that are not alphanumeric, underscores, hyphens, or periods.
    The resulting filename is truncated to 60 characters and trailing underscores are removed.

    Args:
        text (str): The input string to sanitize.

    Returns:
        str: The sanitized filename string.
    """
    text = text.lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^a-z0-9_.-]", "", text)
    return text[:60].strip("_")

def generate_unique_id(content_root: str = "content") -> str:
    """Generates a unique ID for a new Q&A entry based on the current date and existing entries.

    The ID format is "YYYYMMDD-XXX", where YYYYMMDD is the current date and XXX is a
    three-digit sequential number, ensuring uniqueness for entries created on the same day.

    Args:
        content_root (str): The root directory where content is stored. Used to scan
                            existing files for ID generation. Defaults to "content".

    Returns:
        str: A unique ID string.
    """
    today = datetime.now().strftime("%Y%m%d")
    
    # Find the next available ID for today
    existing_ids = []
    for _root, _dirs, files in os.walk(content_root):
        for file in files:
            if file.endswith(".md"):
                match = re.match(r"(\d{8})-(\d{3})_.*\.md", file)
                if match and match.group(1) == today:
                    existing_ids.append(int(match.group(2)))

    next_id_num = 1
    if existing_ids:
        next_id_num = max(existing_ids) + 1

    return f"{today}-{next_id_num:03d}"