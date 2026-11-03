# 🧠 MindMapr – Smart Revision Assistant

> PBL Project | Narsimha Reddy Engineering College  
> Built with Python 

---

## 📌 Project Description

MindMapr is an innovative Python-based application designed to help students
**manage, track, and monitor revision topics**. It leverages core Python concepts
such as lists, dictionaries, loops, file handling, and modular programming.

---

## 🚀 How to Run

```bash
python mindmapr_ui.py
```

No external libraries needed — uses only Python's standard library.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| ➕ Add Topics | Add revision topics with title, category, priority, and notes |
| 📋 View All | Display all topics in a formatted table |
| ✏️ Update | Edit any field of an existing topic |
| 🗑️ Delete | Remove a topic with confirmation |
| 🔍 Search & Filter | Filter by category, priority, status, or keyword |
| 🔄 Mark Status | Quickly set Pending / In Progress / Done |
| 📊 Report | Generate a summary report (saved as .txt) |

---

## 🗂️ Data Storage

- All data is stored persistently in **`mindmapr_data.json`**
- Reports are exported as timestamped **`.txt`** files
- No database setup required

---

## 🏗️ Block Diagram

```
User → Menu Controller → Output Display
              ↓
       Core Operations
              ↓
      File/Database Storage (JSON)
```

---

## 🐍 Python Concepts Used

- Lists & Dictionaries
- Loops (`while`, `for`)
- Functions & Modular Programming
- File Handling (`json`, `os`)
- `datetime` module
- String formatting

---

## 📁 Project Structure

```
PBL1/
├── mindmapr_ui.py          ← Main application
├── mindmapr_data.json ← Auto-created on first run
├── report_YYYYMMDD.txt  ← Auto-generated reports
└── README.md            ← This file
```

