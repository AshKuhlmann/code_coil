"""A simple Tkinter GUI application for adding new Q&A entries to the CodeCoil dataset.

This application provides a user-friendly interface to input all relevant information
for a new Q&A entry, including metadata (domain, topic, subtopic, difficulty, keywords)
and the question, thinking process, and answer content. It automates ID generation,
filename creation, and proper file placement within the 'content/' directory.
"""

import os
import re
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import yaml


class AutocompleteCombobox(ttk.Combobox):
    """A Combobox with autocomplete functionality."""

    def __init__(self, master=None, **kw):
        """Initialize the AutocompleteCombobox.

        Args:
            master: The parent widget.
            **kw: Additional keyword arguments for the Combobox.

        """
        super().__init__(master, **kw)
        self.set_completion_list([])
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind("<KeyRelease>", self.handle_keyrelease)

    def set_completion_list(self, completion_list):
        """Set the list of items for autocomplete.

        Args:
            completion_list (list): A list of strings to use for autocompletion.

        """
        self._completion_list = sorted(completion_list, key=str.lower)

    def autocomplete(self, delta=0):
        """Perform the autocomplete operation.

        Args:
            delta (int): 0 to autocomplete the current input, 1 to cycle to the
                         next hit, -1 to cycle to the previous hit.

        """
        if delta:  # need to delete selection otherwise we would get the previous
            # selection a second time
            self.delete(self.position, tk.END)
        else:  # set position to end (after deletion)
            self.position = len(self.get())
        # collect hits
        _hits = []
        for item in self._completion_list:
            if item.lower().startswith(self.get().lower()):
                _hits.append(item)
        # if we have a new hit list, keep the current hit on top
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # cycle to the next hit
        if _hits:
            self._hit_index = (self._hit_index + delta) % len(_hits)
        else:
            self._hit_index = 0
        # now display the hit
        if _hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """Handle key release events for autocompletion.

        Args:
            event (tk.Event): The key release event.

        """
        if event.keysym == "BackSpace":
            self.delete(self.position, tk.END)
            self.position = len(self.get())
        if event.keysym == "Left":
            if self.position < self.cget("cursor"):
                self.position = self.cget("cursor")
            else:
                self.position = self.position - 1
        if event.keysym == "Right":
            self.position = self.cget("cursor")
        if event.keysym == "Down":
            self.autocomplete(1)  # cycle to next hit
        if event.keysym == "Up":
            self.autocomplete(-1)  # cycle to previous hit
        if len(self.get()) == 0:
            self.position = 0
            self.set_completion_list(self._completion_list)
        else:
            self.autocomplete()


class DataEntryApp:
    """The main application class for the CodeCoil Data Entry GUI."""

    def __init__(self, master):
        """Initialize the DataEntryApp.

        Args:
            master (tk.Tk): The root Tkinter window.

        """
        self.master = master
        master.title("Code Coil Data Entry")

        self.existing_data = self.load_existing_data()

        self.create_widgets()

    def load_existing_data(self):
        """Load existing metadata (domains, topics, subtopics, difficulties, keywords).

        Loads data from the Markdown files in the 'content/' directory.

        Returns:
            dict: A dictionary containing sorted lists of unique metadata values.

        """
        data = {
            "domains": set(),
            "topics": set(),
            "subtopics": set(),
            "difficulties": {"easy", "medium", "hard"},
            "keywords": set(),
        }
        content_dir = "content"
        for _root, _dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(_root, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        match = re.match(r"---(.*?)---", content, re.DOTALL)
                        if match:
                            try:
                                front_matter = yaml.safe_load(match.group(1))
                                if "domain" in front_matter:
                                    data["domains"].add(front_matter["domain"])
                                if "topic" in front_matter:
                                    data["topics"].add(front_matter["topic"])
                                if "subtopic" in front_matter:
                                    data["subtopics"].add(front_matter["subtopic"])
                                if "difficulty" in front_matter:
                                    data["difficulties"].add(front_matter["difficulty"])
                                if "keywords" in front_matter and isinstance(
                                    front_matter["keywords"], list
                                ):
                                    for kw in front_matter["keywords"]:
                                        data["keywords"].add(kw)
                            except yaml.YAMLError:
                                pass  # Ignore malformed YAML

        return {k: sorted(list(v)) for k, v in data.items()}

    def create_widgets(self):
        """Create and arrange the GUI widgets (labels, entry fields, buttons)."""
        # Labels and Entry fields
        self.labels = {}
        self.entries = {}
        self.text_areas = {}

        fields = [
            ("Domain:", "domain", "combobox"),
            ("Topic:", "topic", "combobox"),
            ("Subtopic:", "subtopic", "combobox"),
            ("Difficulty:", "difficulty", "combobox"),
            ("Keywords (comma-separated):", "keywords", "entry"),
            ("Question:", "question", "text"),
            ("Think:", "think", "text"),
            ("Answer:", "answer", "text"),
        ]

        for i, (label_text, key, widget_type) in enumerate(fields):
            label = tk.Label(self.master, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.labels[key] = label

            if widget_type == "entry":
                entry = tk.Entry(self.master, width=50)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
                self.entries[key] = entry
            elif widget_type == "combobox":
                if key == "difficulty":
                    combobox = ttk.Combobox(
                        self.master, values=self.existing_data["difficulties"], width=47
                    )
                elif key == "domain":
                    combobox = AutocompleteCombobox(self.master, width=47)
                    combobox.set_completion_list(self.existing_data["domains"])
                elif key == "topic":
                    combobox = AutocompleteCombobox(self.master, width=47)
                    combobox.set_completion_list(self.existing_data["topics"])
                elif key == "subtopic":
                    combobox = AutocompleteCombobox(self.master, width=47)
                    combobox.set_completion_list(self.existing_data["subtopics"])
                combobox.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
                self.entries[key] = combobox
            elif widget_type == "text":
                text_area = tk.Text(self.master, height=5, width=50)
                text_area.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
                self.text_areas[key] = text_area

        self.submit_button = tk.Button(
            self.master, text="Add Entry", command=self.add_entry
        )
        self.submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

        self.master.grid_columnconfigure(1, weight=1)

    def add_entry(self):
        """Handle the submission of a new Q&A entry.

        Validate input, generate ID and filename, construct Markdown content,
        and save the entry to the appropriate file path.
        """
        data = {}
        for key, entry_widget in self.entries.items():
            data[key] = entry_widget.get().strip()
        for key, text_widget in self.text_areas.items():
            data[key] = text_widget.get("1.0", tk.END).strip()

        # Validate required fields
        required_fields = [
            "domain",
            "topic",
            "subtopic",
            "difficulty",
            "question",
            "answer",
        ]
        for field in required_fields:
            if not data[field]:
                messagebox.showerror(
                    "Error", f"'{field.replace('_', ' ').title()}' is a required field."
                )
                return

        # Process keywords
        keywords = [kw.strip() for kw in data["keywords"].split(",") if kw.strip()]
        data["keywords"] = keywords

        # Generate ID
        today = datetime.now().strftime("%Y%m%d")
        # Find the next available ID for today
        existing_ids = []
        for _root, _dirs, files in os.walk("content"):
            for file in files:
                if file.endswith(".md"):
                    match = re.match(r"(\d{8})-\d{3}_.*\.md", file)
                    if match and match.group(1) == today:
                        existing_ids.append(int(file[9:12]))  # Extract the 001 part

        next_id_num = 1
        if existing_ids:
            next_id_num = max(existing_ids) + 1

        entry_id = f"{today}-{next_id_num:03d}"
        data["id"] = entry_id

        # Generate filename (slugify question)
        question_slug = re.sub(r"[^a-z0-9]+", "_", data["question"].lower())
        question_slug = question_slug.strip("_")
        filename = f"{entry_id}_{question_slug}.md"

        # Construct file path
        # content/domain/topic/subtopic/filename.md
        file_dir = os.path.join(
            "content", data["domain"], data["topic"], data["subtopic"]
        )
        os.makedirs(file_dir, exist_ok=True)
        file_path = os.path.join(file_dir, filename)

        # Create Markdown content
        md_content = f"""---
id: {data["id"]}
domain: "{data["domain"]}"
topic: "{data["topic"]}"
subtopic: "{data["subtopic"]}"
difficulty: "{data["difficulty"]}"
keywords:
"""
        for kw in data["keywords"]:
            md_content += f'  - "{kw}"\n'
        md_content += f"""---

# Question

{data["question"]}

# Think

{data["think"]}

# Answer

{data["answer"]}
"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            messagebox.showinfo("Success", f"Entry added successfully to:\n{file_path}")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write file: {e}")

    def clear_fields(self):
        """Clear all input fields in the GUI."""
        for _key, entry_widget in self.entries.items():
            entry_widget.delete(0, tk.END)
        for _key, text_widget in self.text_areas.items():
            text_widget.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    # Set window icon
    try:
        icon_path = os.path.join(
            os.path.dirname(__file__), "assets", "icons", "add_icon.png"
        )
        if os.path.exists(icon_path):
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(False, icon)
        else:
            print(f"Warning: Icon file not found at {icon_path}")
    except Exception as e:
        print(f"Error setting icon: {e}")

    app = DataEntryApp(root)
    root.mainloop()
