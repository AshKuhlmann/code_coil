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
    """Parses all .md files, formats them into a JSON structure for LLM training,
    and saves them to a single file.
    """
    all_entries = []
    full_root_path = Path(root_path) / domain

    print(f"Starting export to {output_file}...")

    # Recursively find all markdown files
    for md_file in full_root_path.glob("**/*.md"):
        try:
            post = frontmatter.load(md_file)
            content = post.content.strip()

            # Split content into question, think, and answer
            if "# Question" in content and "# Answer" in content:
                think_part = None

                question_raw = content.split("# Think")[0]
                question_part = question_raw.replace("# Question", "").strip()

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
                print(
                    f"Warning: Skipping {md_file} due to missing "
                    "'Question' or 'Answer' header."
                )

        except Exception as e:
            print(f"Error parsing {md_file}: {e}")

    # Write the assembled data to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)

    msg = f"Export complete. {len(all_entries)} entries saved to {output_file}."
    print(msg)


if __name__ == "__main__":
    export_qa_to_json()
