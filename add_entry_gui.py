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
        """Initializes the AutocompleteCombobox.

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
        """Performs the autocomplete operation.

        This method filters the completion list based on the current text in the combobox.
        It supports cycling through the matching hits using the `delta` parameter.

        Args:
            delta (int): Determines the direction of cycling through hits.
                         0: Autocomplete the current input (show the first match).
                         1: Cycle to the next matching hit.
                         -1: Cycle to the previous matching hit.
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
        """Handles key release events for autocompletion.

        This method is responsible for managing the cursor position and triggering
        autocomplete suggestions based on user input in the combobox.

        Args:
            event (tk.Event): The key release event object.
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
    """The main application class for the CodeCoil Data Entry GUI.

    This class sets up the Tkinter window, loads existing dataset metadata,
    creates the input widgets, and handles the logic for adding new Q&A entries.
    """

    def __init__(self, master):
        """Initializes the DataEntryApp.

        Args:
            master (tk.Tk): The root Tkinter window for the application.
        """
        self.master = master
        master.title("Code Coil Data Entry")

        self.existing_data = self.load_existing_data()

        self.create_widgets()

    def load_existing_data(self) -> dict:
        """Loads existing metadata (domains, topics, subtopics, difficulties, keywords).

        This method scans the 'content/' directory for Markdown files, extracts their
        front matter, and populates sets with unique values for domains, topics,
        subtopics, difficulties, and keywords. It also builds a nested dictionary
        (domain_topic_subtopic_map) to maintain the hierarchical relationship between
        domains, topics, and subtopics, which is used for dynamic combobox updates.

        Returns:
            dict: A dictionary containing sorted lists of unique metadata values.
                  Example: {'domains': [...], 'topics': [...], 'subtopics': [...],
                            'difficulties': [...], 'keywords': [...]}
        """
        # Initialize sets to store unique metadata values
        data = {
            "domains": set(),
            "topics": set(),
            "subtopics": set(),
            "difficulties": set(),
            "keywords": set(),
        }
        # Initialize a nested dictionary to map domains to topics and subtopics
        self.domain_topic_subtopic_map = {}
        content_dir = "content"

        # Walk through the content directory to find all Markdown files
        for root, dirs, files in os.walk(content_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    try:
                        # Load the front matter from the Markdown file
                        post = frontmatter.load(filepath)
                        front_matter = post.metadata

                        # Extract domain, topic, and subtopic
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

                        # Extract difficulty
                        if front_matter.get("difficulty"):
                            data["difficulties"].add(front_matter["difficulty"])

                        # Extract keywords
                        if "keywords" in front_matter and isinstance(
                            front_matter["keywords"], list
                        ):
                            for kw in front_matter["keywords"]:
                                data["keywords"].add(kw)
                    except yaml.YAMLError:
                        # Ignore files with malformed YAML front matter
                        pass
                    except Exception as e:
                        # Catch any other potential errors during file processing
                        print(f"Error parsing {filepath}: {e}")

        # Convert sets to sorted lists for consistent ordering and return
        return {k: sorted(list(v)) for k, v in data.items()}

    def create_widgets(self):
        """Creates and arranges the GUI widgets (labels, entry fields, buttons).

        This method sets up the layout of the application window, including input fields
        for all QAEntry attributes, and buttons for interaction. It uses a grid layout
        manager for flexible placement of widgets.
        """
        # Labels and Entry fields
        self.labels = {}
        self.entries = {}
        self.text_areas = {}

        # Define the fields to be displayed in the GUI, including their labels, keys,
        # and widget types (entry, combobox, or text area).
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

        # Iterate through the defined fields to create and place widgets
        for i, (label_text, key, widget_type) in enumerate(fields):
            label = tk.Label(self.master, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.labels[key] = label

            if widget_type == "entry":
                # Create a standard Entry widget for single-line text input
                entry = tk.Entry(self.master, width=50)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
                self.entries[key] = entry
            elif widget_type == "combobox":
                # Create a Combobox for fields with predefined options (e.g., difficulty, domain, topic, subtopic)
                if key == "difficulty":
                    combobox = ttk.Combobox(
                        self.master, values=self.existing_data["difficulties"], width=47
                    )
                elif key == "domain":
                    # AutocompleteCombobox for domain, with binding to update topics
                    combobox = AutocompleteCombobox(self.master, width=47)
                    combobox.set_completion_list(self.existing_data["domains"])
                    combobox.bind("<<ComboboxSelected>>", self.update_topics)
                elif key == "topic":
                    # AutocompleteCombobox for topic, with binding to update subtopics
                    combobox = AutocompleteCombobox(self.master, width=47)
                    combobox.set_completion_list(self.existing_data["topics"])
                    combobox.bind("<<ComboboxSelected>>", self.update_subtopics)
                elif key == "subtopic":
                    # AutocompleteCombobox for subtopic
                    combobox = AutocompleteCombobox(self.master, width=47)
                    combobox.set_completion_list(self.existing_data["subtopics"])
                combobox.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
                self.entries[key] = combobox
            elif widget_type == "text":
                # Create a Text widget for multi-line text input (question, think, answer)
                text_area = tk.Text(self.master, height=5, width=50)
                text_area.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
                self.text_areas[key] = text_area

        # Create and place the "Add Entry" button
        self.submit_button = tk.Button(
            self.master, text="Add Entry", command=self.add_entry
        )
        self.submit_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

        # Configure column 1 to expand horizontally when the window is resized
        self.master.grid_columnconfigure(1, weight=1)

    def update_topics(self, event=None):
        """Updates the topic combobox based on the selected domain.

        This method is called when a new domain is selected in the domain combobox.
        It clears the current topic and subtopic selections, then populates the
        topic combobox with topics relevant to the newly selected domain.

        Args:
            event (tk.Event, optional): The event that triggered this method. Defaults to None.
        """
        selected_domain = self.entries["domain"].get()
        self.entries["topic"].set("")  # Clear current topic
        self.entries["subtopic"].set("")  # Clear current subtopic
        topics = sorted(list(self.domain_topic_subtopic_map.get(selected_domain, {}).keys()))
        self.entries["topic"].set_completion_list(topics)
        self.entries["topic"]["values"] = topics

    def update_subtopics(self, event=None):
        """Updates the subtopic combobox based on the selected domain and topic.

        This method is called when a new topic is selected in the topic combobox.
        It clears the current subtopic selection, then populates the subtopic
        combobox with subtopics relevant to the selected domain and topic.

        Args:
            event (tk.Event, optional): The event that triggered this method. Defaults to None.
        """
        selected_domain = self.entries["domain"].get()
        selected_topic = self.entries["topic"].get()
        self.entries["subtopic"].set("")  # Clear current subtopic
        subtopics = sorted(list(self.domain_topic_subtopic_map.get(selected_domain, {}).get(selected_topic, set())))
        self.entries["subtopic"].set_completion_list(subtopics)
        self.entries["subtopic"]["values"] = subtopics

    def add_entry(self):
        """Handles the submission of a new Q&A entry from the GUI.

        This method retrieves data from all input fields, performs basic validation
        for required fields, processes keywords, generates a unique ID, creates a
        `QAEntry` object, and attempts to save it to a Markdown file. It provides
        user feedback via message boxes for success or failure.
        """
        data = {}
        # Collect data from Entry and Combobox widgets
        for key, entry_widget in self.entries.items():
            data[key] = entry_widget.get().strip()
        # Collect data from Text area widgets
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

        # Process keywords: split by comma, strip whitespace, and filter out empty strings
        keywords = [kw.strip() for kw in data["keywords"].split(",") if kw.strip()]
        data["keywords"] = keywords

        # Generate a unique ID for the new entry
        entry_id = generate_unique_id()
        data["id"] = entry_id

        # Create a QAEntry object with the collected data
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
            # Attempt to save the entry to a Markdown file
            entry.save()
            messagebox.showinfo("Success", f"Entry added successfully for ID: {entry.id}")
            self.clear_fields()  # Clear fields upon successful submission
        except Exception as e:
            # Display an error message if saving fails
            messagebox.showerror("Error", f"Failed to write file: {e}")

    def clear_fields(self):
        """Clears all input fields in the GUI.

        This method iterates through all entry and text area widgets and clears their
        current content, resetting the form for a new entry.
        """
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
