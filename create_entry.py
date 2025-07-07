"""Provides a command-line interface for creating new Q&A entries.

This script guides the user through the process of inputting question, answer,
and metadata, then generates and saves the new entry as a Markdown file
in the appropriate directory structure.
"""
from pathlib import Path

from code_coil.entry import QAEntry, generate_unique_id, sanitize_filename

# --- Configuration ---
# The root directory where all the Q&A markdown files are stored.
CONTENT_ROOT = "content"
# The terminator for multi-line input.
INPUT_TERMINATOR = "::END::"


def get_existing_dirs(path: Path) -> list[str]:
    """Return a sorted list of existing directories at a given path."""
    if not path.is_dir():
        return []
    return sorted([d.name for d in path.iterdir() if d.is_dir()])


def select_from_list(options: list[str], prompt_text: str) -> str:
    """Display options and prompt the user to select or create a new one."""
    if options:
        print(f"\nExisting {prompt_text}s:")
        for i, option in enumerate(options):
            print(f"  {i + 1}: {option}")
        print("  (Or, type a new name to create a new one)")

    choice = input(f"Enter the {prompt_text} name or number: ").strip()

    if choice.isdigit() and options and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1]

    return choice.lower().replace(" ", "_")


def get_multiline_input(prompt: str) -> str:
    """Collect multi-line input until the terminator is entered."""
    lines = []
    print(f"{prompt} (type '{INPUT_TERMINATOR}' on a new line when finished):")
    while True:
        line = input()
        if line.strip().upper() == INPUT_TERMINATOR:
            break
        lines.append(line)
    return "\n".join(lines)


def create_new_entry(content_root: str | None = None) -> None:
    """Guides the user through creating a new Q&A entry.

    This function prompts the user for all necessary information (domain, topic,
    subtopic, question, answer, thinking process, difficulty, keywords) and then
    generates and saves the new entry as a Markdown file
    in the appropriate directory structure.
    """
    print("--- CodeCoil: New Q&A Entry Creator ---")

    root_path = Path(content_root) if content_root else Path(CONTENT_ROOT)
    if not root_path.exists():
        print(f"Error: Content directory '{CONTENT_ROOT}' not found.")
        print("Please run this script from the root of your CodeCoil project.")
        return

    # 1. Get Domain, Topic, and Subtopic
    existing_domains = get_existing_dirs(root_path)
    domain = select_from_list(existing_domains, "domain")
    domain_path = root_path / domain
    domain_path.mkdir(parents=True, exist_ok=True)

    existing_topics = get_existing_dirs(domain_path)
    topic = select_from_list(existing_topics, "topic")
    topic_path = domain_path / topic

    existing_subtopics = get_existing_dirs(topic_path)
    subtopic = select_from_list(existing_subtopics, "subtopic")
    subtopic_path = topic_path / subtopic
    subtopic_path.mkdir(parents=True, exist_ok=True)

    # 2. Get Content (Question, Answer, and optional Thinking)
    print("\n--- Enter Content ---")
    # All text fields require the terminator to finish input
    question = get_multiline_input("Question").strip()

    if not question:
        print("\nError: Question cannot be empty. Aborting.")
        return

    answer = get_multiline_input("Answer")

    thinking = ""
    thinking_prompt = "Include the model's 'Thinking' process? (y/n): "
    include_thinking = input(thinking_prompt).strip().lower()
    if include_thinking == "y":
        thinking = get_multiline_input("Thinking")

    # 3. Get Metadata
    print("\n--- Enter Metadata ---")
    diff_prompt = "Difficulty (easy, medium, hard) [easy]: "
    difficulty = input(diff_prompt).strip().lower() or "easy"
    keywords_raw = input("Keywords (comma-separated): ").strip()
    keywords = [f'"{k.strip()}"' for k in keywords_raw.split(",") if k.strip()]

    # 4. Generate ID
    unique_id = generate_unique_id(str(root_path))

    # 5. Assemble QAEntry object
    entry = QAEntry(
        id=unique_id,
        domain=domain,
        topic=topic,
        subtopic=subtopic,
        difficulty=difficulty,
        keywords=keywords,
        question=question,
        think=thinking,
        answer=answer,
    )

    # 6. Save the file
    filename_prompt = "Enter custom filename (or press Enter to auto-generate): "
    custom_filename = input(filename_prompt).strip()

    try:
        entry.save(content_root=str(root_path), custom_filename=custom_filename)
        print("\n--- Success! ---")
        print(f"New entry created for ID: {unique_id}")
    except IOError as e:
        print(f"\nError: Could not write file. {e}")


if __name__ == "__main__":
    create_new_entry()
