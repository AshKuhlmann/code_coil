"""Exports the CodeCoil dataset into a single JSON file for LLM training.

This script parses all Markdown files within the 'content/' directory,
extacts their question, answer, and metadata, and compiles them into a
structured JSON format suitable for training Large Language Models.
"""
import json
from pathlib import Path

import frontmatter


def export_qa_to_json(
    output_file: str = "qa_data.json",
    domain: str = "python",
    root_path: str = "content",
) -> None:
    """Parses all Markdown files containing Q&A entries, formats them into a JSON structure,
    and saves them to a single output file.

    Args:
        output_file (str): The name of the output JSON file. Defaults to "qa_data.json".
        domain (str): The sub-directory within 'root_path' to search for Markdown files.
                      Defaults to "python".
        root_path (str): The base directory where content is stored. Defaults to "content".
    """
    all_entries = []
    # Construct the full path to the content directory
    full_root_path = Path(root_path) / domain

    print(f"Starting export to {output_file}...")

    # Iterate over all markdown files in the content directory and its subdirectories
    for md_file in full_root_path.glob("**/*.md"):
        try:
            # Load the markdown file with frontmatter
            post = frontmatter.load(md_file)
            content = post.content.strip()

            # Initialize think_part to None
            think_part = None

            # Check if both '# Question' and '# Answer' headers are present
            if "# Question" in content and "# Answer" in content:
                # Extract question part
                question_raw = content.split("# Think")[0]
                question_part = question_raw.replace("# Question", "").strip()

                # Extract think part if it exists, otherwise extract answer directly
                if "# Think" in content:
                    think_section = content.split("# Think")[1]
                    think_raw = think_section.split("# Answer")[0]
                    think_part = think_raw.strip()
                    answer_part = content.split("# Answer")[1].strip()
                else:
                    answer_part = content.split("# Answer")[1].strip()

                # Define the target JSON structure for each entry
                entry = {
                    "instruction": question_part,
                    "response": answer_part,
                    "chain_of_thought": think_part,
                    "metadata": post.metadata,
                }
                all_entries.append(entry)
            else:
                # Warn if essential headers are missing
                print(
                    f"Warning: Skipping {md_file} due to missing "# Question" or "# Answer" header."
                )

        except Exception as e:
            # Log any errors encountered during file parsing
            print(f"Error parsing {md_file}: {e}")

    # Write the assembled data to the output JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)

    # Print a success message with the number of entries exported
    msg = f"Export complete. {len(all_entries)} entries saved to {output_file}."
    print(msg)


if __name__ == "__main__":
    # Execute the export function when the script is run directly
    export_qa_to_json()
