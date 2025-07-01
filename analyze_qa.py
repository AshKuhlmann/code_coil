import frontmatter
import pandas as pd
from pathlib import Path


def analyze_dataset(root_path="python_qa"):
    """
    Walks through the dataset directory, parses metadata from each file,
    and prints a report on content coverage.
    """
    all_metadata = []
    root_dir = Path(root_path)

    print("Starting analysis...")

    # Recursively find all markdown files
    for md_file in root_dir.glob('**/*.md'):
        try:
            post = frontmatter.load(md_file)
            all_metadata.append(post.metadata)
        except Exception as e:
            print(f"Error parsing {md_file}: {e}")

    if not all_metadata:
        print("No metadata found. The dataset might be empty.")
        return

    # Convert to a Pandas DataFrame for easy analysis
    df = pd.DataFrame(all_metadata)

    print("\n--- Dataset Analysis Report ---\n")
    print(f"Total Entries Found: {len(df)}\n")

    # Generate value counts for key metadata fields
    if 'topic' in df.columns:
        print("--- Content by Topic ---")
        print(df['topic'].value_counts())
        print("\n")

    if 'subtopic' in df.columns:
        print("--- Content by Subtopic ---")
        print(df['subtopic'].value_counts())
        print("\n")

    if 'difficulty' in df.columns:
        print("--- Content by Difficulty ---")
        print(df['difficulty'].value_counts())
        print("\n")

    print("--- Analysis Complete ---\n")


if __name__ == "__main__":
    analyze_dataset()
