"""Analyzes the CodeCoil dataset and generates reports on its composition.

This script provides functions to inspect the Markdown files within the 'content/'
directory, extract their metadata, and present statistics on topics, subtopics,
difficulty levels, and the presence of 'Think' sections.
"""
from pathlib import Path

import frontmatter
import pandas as pd


def analyze_dataset(domain: str = "python", root_path: str = "content"):
    """Analyzes the dataset.

    Walks through the dataset directory, parses metadata from each file,
    and prints a report on content coverage.
    """
    all_metadata = []
    think_section_count = 0
    root_dir = Path(root_path)

    print("Starting analysis...")

    # Recursively find all markdown files
    for md_file in root_dir.glob("**/*.md"):
        try:
            post = frontmatter.load(md_file)
            all_metadata.append(post.metadata)
            if "# Think" in post.content:
                think_section_count += 1
        except Exception as e:
            print(f"Error parsing {md_file}: {e}")

    if not all_metadata:
        print("No metadata found. The dataset might be empty.")
        return

    # Convert to a Pandas DataFrame for easy analysis
    df = pd.DataFrame(all_metadata)

    print("\n--- Dataset Analysis Report ---\n")
    print(f"Total Entries Found: {len(df)}\n")

    # Report on Chain-of-Thought usage
    print("--- Chain-of-Thought (CoT) Usage ---")
    print(f"Entries with CoT: {think_section_count}")
    print(f"Entries without CoT: {len(df) - think_section_count}\n")

    # Generate value counts for key metadata fields
    if "topic" in df.columns:
        print("--- Content by Topic ---")
        print(df["topic"].value_counts())
        print("\n")

    if "subtopic" in df.columns:
        print("--- Content by Subtopic ---")
        print(df["subtopic"].value_counts())
        print("\n")

    if "difficulty" in df.columns:
        print("--- Content by Difficulty ---")
        print(df["difficulty"].value_counts())
        print("\n")

    print("--- Analysis Complete ---\n")


if __name__ == "__main__":
    analyze_dataset()
