import json
from pathlib import Path
import frontmatter


def export_dataset(
    root_path: str = "python_qa",
    output_file: str = "training_dataset.json",
) -> None:
    """
    Parses all .md files, formats them into a JSON structure for LLM training,
    and saves them to a single file.
    """
    all_entries = []
    root_dir = Path(root_path)

    print(f"Starting export to {output_file}...")

    # Recursively find all markdown files
    for md_file in root_dir.glob('**/*.md'):
        try:
            post = frontmatter.load(md_file)
            content = post.content.strip()

            # Split content into question and answer
            if "# Question" in content and "# Answer" in content:
                parts = content.split("# Answer")
                question_part = parts[0].replace("# Question", "").strip()
                answer_part = parts[1].strip()

                # Define the target JSON structure for each entry
                entry = {
                    "instruction": question_part,
                    "response": answer_part,
                    "metadata": post.metadata
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
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)

    print(
        f"Export complete. {len(all_entries)} entries saved to {output_file}."
    )


if __name__ == "__main__":
    export_dataset()
