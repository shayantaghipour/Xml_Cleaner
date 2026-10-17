import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import threading
import os

from xml_processor import process_folder
from folder_monitor import FolderMonitor

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class XMLCleanerGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("XML Duplicate Cleaner")
        self.root.geometry("780x520")
        self.root.resizable(False, False)

        self.monitor = None

        self.folder_var = tk.StringVar()
        self.monitor_var = tk.BooleanVar()

        # ===== Title =====
        title = ctk.CTkLabel(
            root,
            text="XML Duplicate Cleaner",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(pady=(20, 10))

        subtitle = ctk.CTkLabel(
            root,
            text="Keep only the newest records based on deployment date",
            text_color="gray"
        )
        subtitle.pack()

        # ===== Main Frame =====
        frame = ctk.CTkFrame(root, corner_radius=12)
        frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="Folder"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=15)

        self.entry = ctk.CTkEntry(
            row,
            textvariable=self.folder_var,
            height=38
        )

        self.entry.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            row,
            text="Browse",
            width=120,
            command=self.select_folder
        ).pack(side="left", padx=(10, 0))

        self.checkbox = ctk.CTkCheckBox(
            frame,
            text="Monitor folder automatically",
            variable=self.monitor_var
        )

        self.checkbox.pack(anchor="w", padx=15, pady=15)

        self.progress = ctk.CTkProgressBar(frame)

        self.progress.pack(fill="x", padx=15)

        self.progress.set(0)

        self.start_btn = ctk.CTkButton(
            frame,
            text="▶ Start Processing",
            height=42,
            font=("Segoe UI", 14, "bold"),
            command=self.start_process
        )

        self.start_btn.pack(pady=20)

        # ===== Status =====

        ctk.CTkLabel(
            root,
            text="Status",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=25)

        self.status = tk.Text(
            root,
            bg="#202124",
            fg="#00ff88",
            insertbackground="white",
            font=("Consolas", 10),
            height=10,
            relief="flat"
        )

        self.status.pack(fill="both", padx=20, pady=(5, 20))

    def log(self, text):

        self.status.insert(tk.END, text + "\n")
        self.status.see(tk.END)

    def select_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.folder_var.set(folder)

    def start_process(self):

        folder = self.folder_var.get()

        if not os.path.isdir(folder):

            messagebox.showerror(
                "Error",
                "Please select a valid folder."
            )

            return

        self.progress.set(0)

        self.start_btn.configure(state="disabled")

        threading.Thread(
            target=self.run_process,
            daemon=True
        ).start()

    def run_process(self):

        folder = self.folder_var.get()

        self.log("──────────────────────────────")
        self.log("Processing XML files...")

        self.progress.set(0.3)

        result = process_folder(folder)

        self.progress.set(1)

        self.log(result)

        self.log("✔ Finished Successfully\n")

        self.start_btn.configure(state="normal")

        if self.monitor_var.get():

            if self.monitor is None:

                self.monitor = FolderMonitor(
                    folder,
                    self.folder_changed
                )

                self.monitor.start()

                self.log("📁 Folder monitor started.")

    def folder_changed(self):

        self.log("New XML detected...")

        self.progress.set(0.5)

        result = process_folder(self.folder_var.get())

        self.progress.set(1)

        self.log(result)


root = ctk.CTk()

app = XMLCleanerGUI(root)

root.mainloop()