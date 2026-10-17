🟦 Project Description — XML Duplicate Cleaner

XML Duplicate Cleaner is a Python-based desktop application designed to process XML files, detect duplicate records, and retain only the most recent record based on its deployment date.

The application automatically processes multiple XML files within a selected directory, compares records using their station numbers, and removes older duplicates while preserving the newest available data. Cleaned records are exported to a well-formatted Excel (.xlsx) file for easy review and further analysis.

✨ Key Features
Duplicate Detection: Identifies duplicate records based on station numbers.
Date-Based Filtering: Preserves the newest record using the deployment timestamp.
Batch Processing: Processes multiple XML files in a selected directory.
Excel Export: Exports cleaned data to Excel with formatted headers, column alignment, filters, and automatic column sizing.
Automatic Folder Monitoring: Detects changes to XML files and triggers reprocessing.
Desktop GUI: Provides a user-friendly interface for selecting folders and managing processing tasks.
Data Normalization: Helps maintain consistent formatting for numeric fields.
🛠️ Technologies Used
Python
Tkinter / CustomTkinter
lxml
openpyxl
Watchdog
PyInstaller
🎯 Project Goal

The goal of this project is to automate data cleaning, reduce duplicate records, improve data consistency, and simplify the process of preparing structured datasets for analysis.
