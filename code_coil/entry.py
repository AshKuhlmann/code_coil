import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import os

@dataclass
class QAEntry:
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

        main_content = f"\n# Question\n\n{self.question}\n"
        if self.think:
            main_content += f"\n# Think\n\n{self.think}\n"
        main_content += f"\n# Answer\n\n{self.answer}\n"

        return front_matter + main_content

    def save(self, content_root: str = "content", custom_filename: str | None = None):
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
    text = text.lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^a-z0-9_.-]", "", text)
    return text[:60].strip("_")

def generate_unique_id(content_root: str = "content") -> str:
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