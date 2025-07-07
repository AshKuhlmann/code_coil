"""Analyzes the CodeCoil dataset and generates reports on its composition.

This script provides functions to inspect the Markdown files within the 'content/'
directory, extract their metadata, and present statistics on topics, subtopics,
difficulty levels, and the presence of 'Think' sections.
"""
from pathlib import Path

import json
from collections import Counter
from pathlib import Path

import frontmatter
import matplotlib.pyplot as plt
import pandas as pd


def plot_distribution(data: pd.Series, title: str, filename: str):
    """Generates and saves a bar plot for the given data series.

    Args:
        data (pd.Series): The data series to plot.
        title (str): The title of the plot.
        filename (str): The name of the file to save the plot as (e.g., "topic_distribution").
    """
    plt.figure(figsize=(10, 6))
    data.plot(kind="bar")
    plt.title(title)
    plt.xlabel("Category")
    plt.ylabel("Number of Entries")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"docs/img/{filename}.png")
    plt.close()


def analyze_dataset(domain: str = "python", root_path: str = "content") -> None:
    """Analyzes the dataset by walking through the content directory, parsing metadata,
    and generating reports and visualizations.

    This function performs the following steps:
    1. Initializes an empty list to store metadata from Markdown files.
    2. Initializes a counter for entries containing a 'Think' section.
    3. Constructs the full path to the content directory.
    4. Iterates through all Markdown files in the specified domain and root path.
    5. For each Markdown file, it attempts to parse the frontmatter.
    6. If parsing is successful, it appends the metadata to a list and checks for the presence
       of a 'Think' section in the content.
    7. If no metadata is found after parsing all files, it prints a warning and exits.
    8. Converts the collected metadata into a Pandas DataFrame for easier analysis.
    9. Prints a summary report including total entries and Chain-of-Thought usage.
    10. Generates and prints value counts for 'topic', 'subtopic', and 'difficulty' if these
        columns exist in the DataFrame.
    11. Calls `plot_distribution` to create and save bar plots for topic, subtopic, and difficulty
        distributions.
    12. Performs keyword analysis by counting the occurrences of each keyword and printing the
        20 most common ones.
    13. Saves all collected statistics into a `stats.json` file.
    14. Prints a completion message.

    Args:
        domain (str): The sub-directory within 'root_path' to search for Markdown files.
                      Defaults to "python".
        root_path (str): The base directory where content is stored. Defaults to "content".
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

    stats = {
        "total_entries": len(df),
        "cot_entries": think_section_count,
        "no_cot_entries": len(df) - think_section_count,
    }

    # Generate value counts for key metadata fields
    if "topic" in df.columns:
        topic_counts = df["topic"].value_counts()
        print("--- Content by Topic ---")
        print(topic_counts)
        print("\n")
        plot_distribution(topic_counts, "Content by Topic", "topic_distribution")
        stats["total_topics"] = len(topic_counts)
        stats["topic_distribution"] = topic_counts.to_dict()

    if "subtopic" in df.columns:
        subtopic_counts = df["subtopic"].value_counts()
        print("--- Content by Subtopic ---")
        print(subtopic_counts)
        print("\n")
        plot_distribution(subtopic_counts, "Content by Subtopic", "subtopic_distribution")
        stats["total_subtopics"] = len(subtopic_counts)
        stats["subtopic_distribution"] = subtopic_counts.to_dict()

    if "difficulty" in df.columns:
        difficulty_counts = df["difficulty"].value_counts()
        print("--- Content by Difficulty ---")
        print(difficulty_counts)
        print("\n")
        plot_distribution(difficulty_counts, "Content by Difficulty", "difficulty_distribution")
        stats["difficulty"] = difficulty_counts.to_dict()

    # Keyword Analysis
    if "keywords" in df.columns:
        all_keywords = []
        for keywords_list in df["keywords"].dropna():
            all_keywords.extend(keywords_list)
        keyword_counts = Counter(all_keywords)
        most_common_keywords = keyword_counts.most_common(20)  # Top 20 keywords
        print("--- Most Common Keywords ---")
        for keyword, count in most_common_keywords:
            print(f"- {keyword}: {count}")
        print("\n")
        stats["most_common_keywords"] = most_common_keywords
        stats["total_unique_keywords"] = len(keyword_counts)

    # Save stats to JSON
    with open("stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print("--- Analysis Complete ---\n")
    print("Statistics saved to stats.json")
    print("Plots saved to docs/img/")

if __name__ == "__main__":
    # Execute the analysis function when the script is run directly
    analyze_dataset()

