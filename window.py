# -*- coding: utf-8 -*-

"""
window.py
This file contains the main GUI window for the long text simplifier application.

Author: Jaxon Ma
Date: 2026-07-11
"""

import tkinter as tk
from tkinter import ttk

from openai import OpenAI
from simplifier import get_env_settings, simplify


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Long Text Simplifier")
        self.geometry("400x500")

        self._build_client()
        self._create_widgets()
        self._layout_widgets()

    def _build_client(self):
        env_settings = get_env_settings()
        self.client = OpenAI(api_key=env_settings["api_key"], base_url=env_settings["base_url"])
        self.model = env_settings["model"]

    def _create_widgets(self):
        self.input_label = ttk.Label(self, text="Original Text:", anchor="w")
        self.input_text = tk.Text(
            self,
            wrap="word",
            undo=True,
            highlightthickness=0,
            highlightbackground=self.cget("bg"),
            highlightcolor=self.cget("bg"),
            bd=0,
            relief="flat",
            padx=8,
            pady=8,
            font=("TkDefaultFont", 14),
        )
        self.input_scroll = ttk.Scrollbar(self, orient="vertical", command=self.input_text.yview)
        self.input_text.configure(yscrollcommand=self.input_scroll.set)

        self.button_frame = ttk.Frame(self)
        self.paste_button = ttk.Button(self.button_frame, text="Paste", command=self._paste_text)
        self.simplify_button = ttk.Button(self.button_frame, text="Simplify", command=self._simplify_text)
        self.copy_button = ttk.Button(
            self.button_frame,
            text="Copy Simplified Text",
            command=self._copy_simplified_text,
        )

        self.output_label = ttk.Label(self, text="Simplified Text:", anchor="w")
        self.output_text = tk.Text(
            self,
            wrap="word",
            undo=True,
            highlightthickness=0,
            highlightbackground=self.cget("bg"),
            highlightcolor=self.cget("bg"),
            bd=0,
            relief="flat",
            padx=8,
            pady=8,
            font=("TkDefaultFont", 14),
        )
        self.output_scroll = ttk.Scrollbar(self, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=self.output_scroll.set)
        self.output_text.insert(
            "1.0",
            "Please edit BASE_URL and API_KEY in your .env file first so the simplifier can run successfully.\n\nThen paste text above or type it directly, and click Simplify."
        )
        self.output_text.configure(state="disabled")

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor="w")

    def _layout_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        self.rowconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

        self.input_label.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 4))
        self.input_text.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=(0, 12))
        self.input_scroll.grid(row=1, column=1, sticky="ns", padx=(0, 12), pady=(0, 12))

        self.button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=2)
        self.paste_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.simplify_button.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.copy_button.grid(row=0, column=2, sticky="ew")

        self.output_label.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 4))
        self.output_text.grid(row=4, column=0, sticky="nsew", padx=(12, 0), pady=(0, 12))
        self.output_scroll.grid(row=4, column=1, sticky="ns", padx=(0, 12), pady=(0, 12))

        self.status_label.grid(row=5, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))

    def _set_status(self, message: str, is_error: bool = False):
        self.status_var.set(message)
        if is_error:
            self.status_label.configure(foreground="red")
        else:
            self.status_label.configure(foreground="black")

    def _paste_text(self):
        try:
            clipboard_text = self.clipboard_get()
        except tk.TclError:
            clipboard_text = ""

        if not clipboard_text:
            self._set_status("Clipboard does not contain text.", is_error=True)
            return

        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", clipboard_text)
        self._set_status("Pasted text from clipboard.")

    def _simplify_text(self):
        source_text = self.input_text.get("1.0", "end").strip()
        if not source_text:
            self._set_status("Please enter or paste text to simplify.", is_error=True)
            return

        self._set_status("Simplifying text...")
        self.update_idletasks()

        simplified_text = simplify(self.client, self.model, source_text)
        if simplified_text is None:
            self._set_status("Failed to simplify text. Check your settings or your network.", is_error=True)
            return

        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", simplified_text)
        self.output_text.configure(state="disabled")
        self._set_status("Text simplified successfully.")

    def _copy_simplified_text(self):
        simplified_text = self.output_text.get("1.0", "end").strip()
        if not simplified_text:
            self._set_status("No simplified text to copy.", is_error=True)
            return

        self.clipboard_clear()
        self.clipboard_append(simplified_text)
        self._set_status("Copied simplified text to clipboard.")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
