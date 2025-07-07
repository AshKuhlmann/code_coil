"""A simple Tkinter GUI application for adding new Q&A entries to the CodeCoil dataset.

This application provides a user-friendly interface to input all relevant information
for a new Q&A entry, including metadata (domain, topic, subtopic, difficulty, keywords)
and the question, thinking process, and answer content. It automates ID generation,
filename creation, and proper file placement within the 'content/' directory.
"""

import os
import re
import tkinter as tk
from tkinter import messagebox, ttk

import yaml

from code_coil.entry import QAEntry, generate_unique_id


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
        self.domain_topic_subtopic_map = {}
        content_dir = "content"
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        match = re.match(r"---(.*?)---", content, re.DOTALL)
                        if match:
                            try:
                                front_matter = yaml.safe_load(match.group(1))
                                domain = front_matter.get("domain")
                                topic = front_matter.get("topic")
                                subtopic = front_matter.get("subtopic")

                                if domain:
                                    data["domains"].add(domain)
                                    if domain not in self.domain_topic_subtopic_map:
                                        self.domain_topic_subtopic_map[domain] = {}
                                    if topic:
                                        data["topics"].add(topic)
                                        if topic not in self.domain_topic_subtopic_map[domain]:
                                            self.domain_topic_subtopic_map[domain][topic] = set()
                                        if subtopic:
                                            data["subtopics"].add(subtopic)
                                            self.domain_topic_subtopic_map[domain][topic].add(subtopic)

                                if front_matter.get("difficulty"):
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
            ("Keywords (comma-separated, e.g., python, list):", "keywords", "entry"),
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
                    combobox.bind("<<ComboboxSelected>>", self.update_topics)
                elif key == "topic":
                    combobox = AutocompleteCombobox(self.master, width=47)
                    combobox.set_completion_list(self.existing_data["topics"])
                    combobox.bind("<<ComboboxSelected>>", self.update_subtopics)
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

    def update_topics(self, event=None):
        selected_domain = self.entries["domain"].get()
        self.entries["topic"].set("")  # Clear current topic
        self.entries["subtopic"].set("")  # Clear current subtopic
        topics = sorted(list(self.domain_topic_subtopic_map.get(selected_domain, {}).keys()))
        self.entries["topic"].set_completion_list(topics)
        self.entries["topic"]["values"] = topics

    def update_subtopics(self, event=None):
        selected_domain = self.entries["domain"].get()
        selected_topic = self.entries["topic"].get()
        self.entries["subtopic"].set("")  # Clear current subtopic
        subtopics = sorted(list(self.domain_topic_subtopic_map.get(selected_domain, {}).get(selected_topic, set())))
        self.entries["subtopic"].set_completion_list(subtopics)
        self.entries["subtopic"]["values"] = subtopics

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
        entry_id = generate_unique_id()
        data["id"] = entry_id

        # Create QAEntry object
        entry = QAEntry(
            id=data["id"],
            domain=data["domain"],
            topic=data["topic"],
            subtopic=data["subtopic"],
            difficulty=data["difficulty"],
            keywords=data["keywords"],
            question=data["question"],
            think=data["think"],
            answer=data["answer"],
        )

        try:
            entry.save()
            messagebox.showinfo("Success", f"Entry added successfully for ID: {entry.id}")
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
