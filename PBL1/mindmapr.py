"""
MindMapr – Smart Revision Assistant
====================================
A Python-based console application for managing and tracking revision topics.
Developed for PBL (Project-Based Learning) at Narsimha Reddy Engineering College.

Features:
  - Add, update, delete, and manage revision topics
  - Categorization and filtering
  - Persistent JSON storage
  - Summarized outputs and reports
"""

import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
#  FILE HANDLING – Persistent Storage (JSON)
# ─────────────────────────────────────────────
DATA_FILE = "mindmapr_data.json"


def load_data() -> dict:
    """Load topics from the JSON data file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"topics": []}


def save_data(data: dict) -> None:
    """Save topics to the JSON data file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ─────────────────────────────────────────────
#  CORE OPERATIONS
# ─────────────────────────────────────────────

def generate_id(topics: list) -> int:
    """Generate a unique integer ID for a new topic."""
    if not topics:
        return 1
    return max(t["id"] for t in topics) + 1


def add_topic(data: dict) -> None:
    """Add a new revision topic."""
    print("\n─── Add New Topic ───")
    title    = input("  Topic Title     : ").strip()
    category = input("  Category        : ").strip()
    priority = input("  Priority (High/Medium/Low): ").strip().capitalize()
    notes    = input("  Notes / Details : ").strip()

    if not title:
        print("  [!] Title cannot be empty. Topic not added.")
        return

    if priority not in ("High", "Medium", "Low"):
        priority = "Medium"

    topic = {
        "id"        : generate_id(data["topics"]),
        "title"     : title,
        "category"  : category,
        "priority"  : priority,
        "status"    : "Pending",
        "notes"     : notes,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    data["topics"].append(topic)
    save_data(data)
    print(f"  [✓] Topic '{title}' added successfully! (ID: {topic['id']})")


def view_all_topics(data: dict) -> None:
    """Display all revision topics."""
    topics = data["topics"]
    print("\n─── All Revision Topics ───")
    if not topics:
        print("  No topics found. Add some topics first!")
        return
    _print_topic_table(topics)


def update_topic(data: dict) -> None:
    """Update an existing topic."""
    print("\n─── Update Topic ───")
    view_all_topics(data)
    if not data["topics"]:
        return

    try:
        tid = int(input("\n  Enter Topic ID to update: "))
    except ValueError:
        print("  [!] Invalid ID.")
        return

    topic = _find_topic(data["topics"], tid)
    if not topic:
        print(f"  [!] No topic found with ID {tid}.")
        return

    print(f"\n  Editing: '{topic['title']}' (leave blank to keep current value)")
    new_title    = input(f"  Title [{topic['title']}]     : ").strip()
    new_category = input(f"  Category [{topic['category']}]: ").strip()
    new_priority = input(f"  Priority [{topic['priority']}] (High/Medium/Low): ").strip().capitalize()
    new_status   = input(f"  Status [{topic['status']}] (Pending/In Progress/Done): ").strip().capitalize()
    new_notes    = input(f"  Notes [{topic['notes']}]: ").strip()

    if new_title:    topic["title"]    = new_title
    if new_category: topic["category"] = new_category
    if new_priority in ("High", "Medium", "Low"): topic["priority"] = new_priority
    if new_status   in ("Pending", "In Progress", "Done"): topic["status"] = new_status
    if new_notes:    topic["notes"]    = new_notes
    topic["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    save_data(data)
    print(f"  [✓] Topic ID {tid} updated successfully!")


def delete_topic(data: dict) -> None:
    """Delete a topic by ID."""
    print("\n─── Delete Topic ───")
    view_all_topics(data)
    if not data["topics"]:
        return

    try:
        tid = int(input("\n  Enter Topic ID to delete: "))
    except ValueError:
        print("  [!] Invalid ID.")
        return

    topic = _find_topic(data["topics"], tid)
    if not topic:
        print(f"  [!] No topic found with ID {tid}.")
        return

    confirm = input(f"  Are you sure you want to delete '{topic['title']}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        data["topics"].remove(topic)
        save_data(data)
        print(f"  [✓] Topic '{topic['title']}' deleted.")
    else:
        print("  Deletion cancelled.")


def search_filter(data: dict) -> None:
    """Search and filter topics by category, priority, or status."""
    print("\n─── Search & Filter Topics ───")
    print("  Filter by:")
    print("  1. Category")
    print("  2. Priority")
    print("  3. Status")
    print("  4. Keyword in Title")
    choice = input("  Choose filter (1-4): ").strip()

    topics = data["topics"]
    results = []

    if choice == "1":
        cat = input("  Enter Category: ").strip().lower()
        results = [t for t in topics if t["category"].lower() == cat]
    elif choice == "2":
        pri = input("  Enter Priority (High/Medium/Low): ").strip().capitalize()
        results = [t for t in topics if t["priority"] == pri]
    elif choice == "3":
        sts = input("  Enter Status (Pending/In Progress/Done): ").strip().capitalize()
        results = [t for t in topics if t["status"].lower() == sts.lower()]
    elif choice == "4":
        kw = input("  Enter Keyword: ").strip().lower()
        results = [t for t in topics if kw in t["title"].lower()]
    else:
        print("  [!] Invalid choice.")
        return

    if results:
        print(f"\n  Found {len(results)} result(s):")
        _print_topic_table(results)
    else:
        print("  No topics matched your filter.")


def mark_status(data: dict) -> None:
    """Quickly mark a topic's revision status."""
    print("\n─── Mark Revision Status ───")
    view_all_topics(data)
    if not data["topics"]:
        return

    try:
        tid = int(input("\n  Enter Topic ID: "))
    except ValueError:
        print("  [!] Invalid ID.")
        return

    topic = _find_topic(data["topics"], tid)
    if not topic:
        print(f"  [!] No topic found with ID {tid}.")
        return

    print("  Status Options:")
    print("  1. Pending")
    print("  2. In Progress")
    print("  3. Done")
    sc = input("  Choose new status (1-3): ").strip()
    status_map = {"1": "Pending", "2": "In Progress", "3": "Done"}
    if sc in status_map:
        topic["status"] = status_map[sc]
        topic["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_data(data)
        print(f"  [✓] Status updated to '{topic['status']}' for '{topic['title']}'.")
    else:
        print("  [!] Invalid choice.")


def generate_report(data: dict) -> None:
    """Generate a summary report of all topics."""
    topics = data["topics"]
    print("\n" + "=" * 50)
    print("   MindMapr – Summary Report")
    print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    if not topics:
        print("  No data available for report.")
        return

    total    = len(topics)
    done     = sum(1 for t in topics if t["status"] == "Done")
    in_prog  = sum(1 for t in topics if t["status"] == "In Progress")
    pending  = sum(1 for t in topics if t["status"] == "Pending")
    high_pri = sum(1 for t in topics if t["priority"] == "High")

    print(f"\n  📊 Total Topics    : {total}")
    print(f"  ✅ Done            : {done}")
    print(f"  🔄 In Progress     : {in_prog}")
    print(f"  ⏳ Pending         : {pending}")
    print(f"  🔴 High Priority   : {high_pri}")

    # Category breakdown
    categories: dict = {}
    for t in topics:
        cat = t["category"] or "Uncategorized"
        categories[cat] = categories.get(cat, 0) + 1

    print("\n  📁 Category Breakdown:")
    for cat, count in sorted(categories.items()):
        print(f"     {cat:<25} : {count} topic(s)")

    # Completion percentage
    if total > 0:
        pct = (done / total) * 100
        bar_len = 30
        filled  = int(bar_len * done / total)
        bar     = "█" * filled + "░" * (bar_len - filled)
        print(f"\n  Progress  [{bar}] {pct:.1f}%")

    print("=" * 50)

    # Save report to text file
    report_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    _save_report_to_file(data, report_file)
    print(f"\n  [✓] Report saved to '{report_file}'")


def _save_report_to_file(data: dict, filename: str) -> None:
    """Save the summary report to a TXT file."""
    topics = data["topics"]
    lines = [
        "MindMapr – Smart Revision Assistant",
        f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
        "",
    ]
    for t in topics:
        lines.append(f"[{t['id']}] {t['title']}")
        lines.append(f"    Category : {t['category']}")
        lines.append(f"    Priority : {t['priority']}")
        lines.append(f"    Status   : {t['status']}")
        lines.append(f"    Notes    : {t['notes']}")
        lines.append(f"    Created  : {t['created_at']}")
        lines.append(f"    Updated  : {t['updated_at']}")
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ─────────────────────────────────────────────
#  HELPER / DISPLAY UTILITIES
# ─────────────────────────────────────────────

def _find_topic(topics: list, tid: int):
    """Return the topic dict matching the given ID, or None."""
    for t in topics:
        if t["id"] == tid:
            return t
    return None


def _print_topic_table(topics: list) -> None:
    """Pretty-print a list of topics in a table format."""
    header = f"  {'ID':<4} {'Subject':<25} {'Topic':<15} {'Priority':<10} {'Status':<12} {'Updated':<16}"
    sep    = "  " + "-" * 84
    print(sep)
    print(header)
    print(sep)
    for t in topics:
        status_icon = {"Done": "✅", "In Progress": "🔄", "Pending": "⏳"}.get(t["status"], "❓")
        print(
            f"  {t['id']:<4} {t['title'][:24]:<25} {t['category'][:14]:<15} "
            f"{t['priority']:<10} {status_icon} {t['status']:<10} {t['updated_at']:<16}"
        )
    print(sep)


# ─────────────────────────────────────────────
#  MENU CONTROLLER
# ─────────────────────────────────────────────

def display_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("    🧠 MindMapr – Smart Revision Assistant")
    print("=" * 50)
    print("  1. Add New Topic")
    print("  2. View All Topics")
    print("  3. Update Topic")
    print("  4. Delete Topic")
    print("  5. Search & Filter Topics")
    print("  6. Mark Revision Status")
    print("  7. Generate Summary Report")
    print("  0. Exit")
    print("=" * 50)


def main() -> None:
    """Main loop – Menu Controller."""
    print("\n  Welcome to MindMapr – Smart Revision Assistant!")
    print("  Narsimha Reddy Engineering College | PBL Project\n")

    data = load_data()

    menu_actions = {
        "1": add_topic,
        "2": view_all_topics,
        "3": update_topic,
        "4": delete_topic,
        "5": search_filter,
        "6": mark_status,
        "7": generate_report,
    }

    while True:
        display_menu()
        choice = input("  Enter your choice: ").strip()

        if choice == "0":
            print("\n  Thank you for using MindMapr! Keep revising! 📚\n")
            break
        elif choice in menu_actions:
            menu_actions[choice](data)
            input("\n  Press Enter to continue...")
        else:
            print("  [!] Invalid choice. Please enter a number from 0 to 7.")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    main()

