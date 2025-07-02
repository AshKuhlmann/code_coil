# create_entry.py
import re
from datetime import datetime
from pathlib import Path

# --- Configuration ---
# The root directory where all the Q&A markdown files are stored.
CONTENT_ROOT = "content"
# The terminator for multi-line input.
INPUT_TERMINATOR = "::END::"


def get_existing_dirs(path):
    """Returns a sorted list of existing directories at a given path."""
    if not path.is_dir():
        return []
    return sorted([d.name for d in path.iterdir() if d.is_dir()])


def sanitize_filename(text):
    """
    Takes a string and returns a sanitized version suitable for a filename.
    - Converts to lowercase
    - Replaces spaces and special characters with underscores
    - Removes any remaining invalid filename characters
    - Truncates to a reasonable length
    """
    text = text.lower()
    text = re.sub(r'\s+', '_', text)
    text = re.sub(r'[^a-z0-9_.-]', '', text)
    return text[:60]  # Truncate to 60 characters


def select_from_list(options, prompt_text):
    """Display options and prompt the user to select or create a new one."""
    if options:
        print(f"\nExisting {prompt_text}s:")
        for i, option in enumerate(options):
            print(f"  {i+1}: {option}")
        print("  (Or, type a new name to create a new one)")

    choice = input(f"Enter the {prompt_text} name or number: ").strip()

    if choice.isdigit() and options and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1]

    return choice.lower().replace(" ", "_")


def get_multiline_input(prompt):
    """Collect multi-line input until the terminator is entered."""
    lines = []
    print(f"{prompt} (type '{INPUT_TERMINATOR}' on a new line when finished):")
    while True:
        line = input()
        if line.strip().upper() == INPUT_TERMINATOR:
            break
        lines.append(line)
    return "\n".join(lines)


def create_new_entry(content_root=None):
    """
    Main function to guide the user through creating a new Q&A entry.
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
    if include_thinking == 'y':
        thinking = get_multiline_input("Thinking")

    # 3. Get Metadata
    print("\n--- Enter Metadata ---")
    diff_prompt = "Difficulty (easy, medium, hard) [easy]: "
    difficulty = input(diff_prompt).strip().lower() or "easy"
    keywords_raw = input("Keywords (comma-separated): ").strip()
    keywords = [f'"{k.strip()}"' for k in keywords_raw.split(',') if k.strip()]

    # 4. Generate File Name and ID
    filename_prompt = (
        "Enter custom filename (or press Enter to auto-generate): "
    )
    custom_filename = input(filename_prompt).strip()

    if custom_filename:
        # Ensure it has a .md extension
        if not custom_filename.endswith('.md'):
            custom_filename += '.md'
        filename = sanitize_filename(custom_filename)
    else:
        # Find the highest existing number in the directory to avoid collisions
        existing_files = list(subtopic_path.glob("*.md"))
        next_num = len(existing_files) + 1
        sanitized_q = sanitize_filename(question)
        filename = f"{next_num:03d}_{sanitized_q}.md"

    file_path = subtopic_path / filename

    date_str = datetime.now().strftime("%Y%m%d")
    # A simple way to generate a semi-unique ID for the day
    id_num = len(list(domain_path.glob('**/*.md'))) + 1
    unique_id = f"{date_str}-{id_num:04d}"

    # 5. Assemble the final Markdown content
    keywords_formatted = "\n  - ".join(keywords)
    front_matter = (
        f"---\n"
        f"id: {unique_id}\n"
        f"domain: \"{domain}\"\n"
        f"topic: \"{topic}\"\n"
        f"subtopic: \"{subtopic}\"\n"
        f"difficulty: \"{difficulty}\"\n"
        "keywords:\n"
        f"  - {keywords_formatted}\n"
        "---\n"
    )

    # Build the main content, including the optional "Think" section
    main_content = f"\n# Question\n\n{question}\n"
    if thinking:
        main_content += f"\n# Think\n\n{thinking}\n"
    main_content += f"\n# Answer\n\n{answer}\n"

    final_text = front_matter + main_content

    # 6. Write the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_text)
        print("\n--- Success! ---")
        print(f"New entry created at: {file_path}")
    except IOError as e:
        print(f"\nError: Could not write file. {e}")


if __name__ == "__main__":
    create_new_entry()
