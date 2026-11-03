"""
MindMapr – Smart Revision Assistant (GUI Version)
===================================================
A Tkinter-based desktop application for managing revision topics.
PBL Project | Narsimha Reddy Engineering College
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# ─────────────────────────────────────────────
#  FILE HANDLING
# ─────────────────────────────────────────────
DATA_FILE = "mindmapr_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"topics": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def generate_id(topics):
    return max((t["id"] for t in topics), default=0) + 1


# ─────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────
BG        = "#1e1e2e"   # Dark background
SIDEBAR   = "#181825"   # Sidebar background
CARD      = "#313244"   # Card / panel background
ACCENT    = "#cba6f7"   # Purple accent (Catppuccin Mauve)
ACCENT2   = "#89b4fa"   # Blue
GREEN     = "#a6e3a1"
YELLOW    = "#f9e2af"
RED       = "#f38ba8"
TEXT      = "#cdd6f4"
SUBTEXT   = "#a6adc8"
BTN_BG    = "#45475a"
BTN_HOV   = "#585b70"
ENTRY_BG  = "#313244"
HEADER_BG = "#11111b"

PRIORITY_COLORS = {"High": RED, "Medium": YELLOW, "Low": GREEN}
STATUS_ICONS    = {"Pending": "⏳", "In Progress": "🔄", "Done": "✅"}


# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class MindMaprApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧠 MindMapr – Smart Revision Assistant")
        self.geometry("1100x680")
        self.minsize(900, 580)
        self.configure(bg=BG)
        self.resizable(True, True)

        self.data = load_data()

        self._build_layout()
        self.show_frame("home")

    # ── LAYOUT ──────────────────────────────
    def _build_layout(self):
        # ── Sidebar ─────────────────────────
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # App logo / title
        tk.Label(
            self.sidebar, text="🧠", font=("Segoe UI Emoji", 34),
            bg=SIDEBAR, fg=ACCENT
        ).pack(pady=(30, 0))
        tk.Label(
            self.sidebar, text="MindMapr", font=("Segoe UI", 16, "bold"),
            bg=SIDEBAR, fg=TEXT
        ).pack()
        tk.Label(
            self.sidebar, text="Smart Revision Assistant",
            font=("Segoe UI", 8), bg=SIDEBAR, fg=SUBTEXT
        ).pack(pady=(0, 30))

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=16, pady=4)

        # Nav buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠  Home",           "home"),
            ("📋  All Topics",     "view"),
            ("➕  Add Topic",      "add"),
            ("🔍  Search & Filter","search"),
            ("📊  Report",         "report"),
        ]
        for label, key in nav_items:
            btn = tk.Button(
                self.sidebar, text=label, anchor="w",
                font=("Segoe UI", 11), padx=18,
                bg=SIDEBAR, fg=TEXT, bd=0, relief="flat",
                activebackground=CARD, activeforeground=ACCENT,
                cursor="hand2",
                command=lambda k=key: self.show_frame(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

        # Version at bottom
        tk.Label(
            font=("Segoe UI", 8), bg=SIDEBAR, fg=SUBTEXT
        ).pack(side="bottom", pady=16)

        # ── Main content area ────────────────
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Build all frames
        self.frames = {}
        for F in (HomeFrame, ViewFrame, AddFrame, SearchFrame, ReportFrame):
            frame = F(self.content, self)
            self.frames[F.key] = frame
            frame.place(relwidth=1, relheight=1)

    def show_frame(self, key):
        # Highlight active nav button
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(bg=CARD, fg=ACCENT, font=("Segoe UI", 11, "bold"))
            else:
                btn.configure(bg=SIDEBAR, fg=TEXT, font=("Segoe UI", 11))

        frame = self.frames[key]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def refresh_data(self):
        self.data = load_data()


# ─────────────────────────────────────────────
#  SHARED HELPERS
# ─────────────────────────────────────────────
def make_label(parent, text, font=("Segoe UI", 11), fg=TEXT, bg=BG, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


def make_entry(parent, textvariable=None, width=30):
    e = tk.Entry(
        parent, textvariable=textvariable, width=width,
        bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
        relief="flat", font=("Segoe UI", 11), bd=6
    )
    return e


def make_button(parent, text, command, color=ACCENT, fg=BG, width=16):
    return tk.Button(
        parent, text=text, command=command, width=width,
        bg=color, fg=fg, font=("Segoe UI", 10, "bold"),
        relief="flat", cursor="hand2", bd=0,
        activebackground=BTN_HOV, activeforeground=TEXT,
        padx=8, pady=6
    )


def card_frame(parent, **kw):
    return tk.Frame(parent, bg=CARD, bd=0, relief="flat", **kw)


# ─────────────────────────────────────────────
#  FRAME: HOME
# ─────────────────────────────────────────────
class HomeFrame(tk.Frame):
    key = "home"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=HEADER_BG, pady=20)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Welcome to MindMapr 🧠", font=("Segoe UI", 22, "bold"),
                 bg=HEADER_BG, fg=ACCENT).pack()
        tk.Label(hdr, text="Your Smart Revision Assistant",
                 font=("Segoe UI", 12), bg=HEADER_BG, fg=SUBTEXT).pack()

        # Stats row
        self.stats_frame = tk.Frame(self, bg=BG)
        self.stats_frame.pack(fill="x", padx=30, pady=24)

        # Quick-action buttons
        qa = card_frame(self, padx=20, pady=20)
        qa.pack(fill="x", padx=30, pady=(0, 20))
        tk.Label(qa, text="Quick Actions", font=("Segoe UI", 13, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 12))

        row = tk.Frame(qa, bg=CARD)
        row.pack()
        make_button(row, "➕ Add Topic",    lambda: self.app.show_frame("add"),    ACCENT).pack(side="left", padx=8)
        make_button(row, "📋 View Topics",  lambda: self.app.show_frame("view"),   ACCENT2).pack(side="left", padx=8)
        make_button(row, "🔍 Search",       lambda: self.app.show_frame("search"), GREEN).pack(side="left", padx=8)
        make_button(row, "📊 Report",       lambda: self.app.show_frame("report"), YELLOW).pack(side="left", padx=8)

    def on_show(self):
        self.app.refresh_data()
        for w in self.stats_frame.winfo_children():
            w.destroy()
        topics = self.app.data["topics"]
        total   = len(topics)
        done    = sum(1 for t in topics if t["status"] == "Done")
        prog    = sum(1 for t in topics if t["status"] == "In Progress")
        pending = sum(1 for t in topics if t["status"] == "Pending")

        stats = [
            ("📚 Total",       total,   ACCENT2),
            ("✅ Done",         done,    GREEN),
            ("🔄 In Progress",  prog,    YELLOW),
            ("⏳ Pending",      pending, RED),
        ]
        for label, val, color in stats:
            box = card_frame(self.stats_frame, padx=24, pady=16)
            box.pack(side="left", expand=True, fill="both", padx=10)
            tk.Label(box, text=str(val), font=("Segoe UI", 32, "bold"),
                     bg=CARD, fg=color).pack()
            tk.Label(box, text=label, font=("Segoe UI", 11),
                     bg=CARD, fg=SUBTEXT).pack()


# ─────────────────────────────────────────────
#  FRAME: VIEW ALL TOPICS  (split-pane with detail panel)
# ─────────────────────────────────────────────
class ViewFrame(tk.Frame):
    key = "view"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # ── Header ──────────────────────────────
        hdr = tk.Frame(self, bg=HEADER_BG, pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📋  All Topics", font=("Segoe UI", 18, "bold"),
                 bg=HEADER_BG, fg=ACCENT).pack(side="left", padx=24)
        make_button(hdr, "🔄 Refresh", self.on_show, ACCENT2, width=10).pack(side="right", padx=16)

        # ── Treeview style ───────────────────────
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background=CARD, foreground=TEXT,
                         rowheight=30, fieldbackground=CARD,
                         font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                         background=HEADER_BG, foreground=ACCENT,
                         font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT)],
                  foreground=[("selected", BG)])

        # ── Split pane (PanedWindow) ─────────────
        paned = tk.PanedWindow(self, orient="horizontal", bg=BG,
                               sashwidth=6, sashrelief="flat",
                               sashpad=2, bd=0)
        paned.pack(fill="both", expand=True, padx=12, pady=10)

        # LEFT – table
        left = tk.Frame(paned, bg=BG)
        paned.add(left, minsize=380)

        tree_frame = tk.Frame(left, bg=BG)
        tree_frame.pack(fill="both", expand=True)

        cols = ("id", "subject", "topic", "priority", "status", "updated")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                  selectmode="browse")
        col_cfg = [
            ("id",       "ID",        48),
            ("subject",  "Subject",  180),
            ("topic",    "Topic",    120),
            ("priority", "Priority",  80),
            ("status",   "Status",   120),
            ("updated",  "Updated",  130),
        ]
        for cid, cname, cw in col_cfg:
            self.tree.heading(cid, text=cname)
            self.tree.column(cid, width=cw,
                             anchor="w" if cid in ("subject", "topic") else "center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Action buttons under the table
        btn_row = tk.Frame(left, bg=BG)
        btn_row.pack(pady=8)
        make_button(btn_row, "✏️ Edit",   self._edit_selected,   ACCENT, width=14).pack(side="left", padx=5)
        make_button(btn_row, "🗑️ Delete", self._delete_selected, RED,    width=14).pack(side="left", padx=5)

        # RIGHT – detail panel
        right = tk.Frame(paned, bg=CARD)
        paned.add(right, minsize=260)

        # Hint label (shown when nothing is selected)
        self.hint_lbl = tk.Label(
            right,
            text="👆  Click any row\nto view full details",
            font=("Segoe UI", 13), bg=CARD, fg=SUBTEXT,
            justify="center"
        )
        self.hint_lbl.place(relx=0.5, rely=0.42, anchor="center")

        # Detail content (hidden initially)
        self.detail_panel = tk.Frame(right, bg=CARD)

        # Badge row at top (priority + status)
        self.badge_frame = tk.Frame(self.detail_panel, bg=CARD)
        self.badge_frame.pack(fill="x", padx=20, pady=(22, 0))

        self.pri_badge  = tk.Label(self.badge_frame, text="", font=("Segoe UI", 9, "bold"),
                                    bg=CARD, padx=8, pady=3, relief="flat")
        self.pri_badge.pack(side="left", padx=(0, 8))
        self.sts_badge  = tk.Label(self.badge_frame, text="", font=("Segoe UI", 9, "bold"),
                                    bg=CARD, padx=8, pady=3, relief="flat")
        self.sts_badge.pack(side="left")

        # Subject (big title)
        self.d_subject = tk.Label(self.detail_panel, text="", font=("Segoe UI", 17, "bold"),
                                   bg=CARD, fg=ACCENT, wraplength=280, justify="left")
        self.d_subject.pack(anchor="w", padx=20, pady=(10, 2))

        # Topic (subtitle)
        self.d_topic = tk.Label(self.detail_panel, text="", font=("Segoe UI", 11),
                                 bg=CARD, fg=SUBTEXT)
        self.d_topic.pack(anchor="w", padx=20, pady=(0, 14))

        ttk.Separator(self.detail_panel).pack(fill="x", padx=16, pady=4)

        # Notes section
        tk.Label(self.detail_panel, text="📝  Notes / Details",
                 font=("Segoe UI", 10, "bold"), bg=CARD, fg=TEXT).pack(anchor="w", padx=20, pady=(10, 4))

        notes_box = tk.Frame(self.detail_panel, bg=ENTRY_BG, padx=12, pady=10)
        notes_box.pack(fill="x", padx=16, pady=(0, 14))
        self.d_notes = tk.Label(notes_box, text="", font=("Segoe UI", 10),
                                 bg=ENTRY_BG, fg=TEXT, wraplength=260,
                                 justify="left", anchor="nw")
        self.d_notes.pack(fill="both", anchor="w")

        ttk.Separator(self.detail_panel).pack(fill="x", padx=16, pady=4)

        # Meta (created / updated)
        self.d_created = tk.Label(self.detail_panel, text="", font=("Segoe UI", 9),
                                   bg=CARD, fg=SUBTEXT)
        self.d_created.pack(anchor="w", padx=20, pady=2)
        self.d_updated = tk.Label(self.detail_panel, text="", font=("Segoe UI", 9),
                                   bg=CARD, fg=SUBTEXT)
        self.d_updated.pack(anchor="w", padx=20, pady=2)

        # Bind single click on tree row
        self.tree.bind("<<TreeviewSelect>>", self._on_row_click)

    # ── populate table ───────────────────────
    def on_show(self):
        self.app.refresh_data()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in self.app.data["topics"]:
            icon = STATUS_ICONS.get(t["status"], "")
            tag  = t["priority"].lower()
            self.tree.insert("", "end", iid=str(t["id"]), tags=(tag,),
                             values=(t["id"], t["title"], t["category"],
                                     t["priority"], f"{icon} {t['status']}", t["updated_at"]))
        self.tree.tag_configure("high",   foreground=RED)
        self.tree.tag_configure("medium", foreground=YELLOW)
        self.tree.tag_configure("low",    foreground=GREEN)
        # Reset detail panel
        self.detail_panel.place_forget()
        self.hint_lbl.place(relx=0.5, rely=0.42, anchor="center")

    # ── click handler → fill detail panel ───
    def _on_row_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        tid   = int(sel[0])
        topic = next((t for t in self.app.data["topics"] if t["id"] == tid), None)
        if not topic:
            return

        # Hide hint, show detail
        self.hint_lbl.place_forget()
        self.detail_panel.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Priority badge
        pri_color = PRIORITY_COLORS.get(topic["priority"], SUBTEXT)
        self.pri_badge.config(text=f"  {topic['priority']} Priority  ",
                               fg=BG, bg=pri_color)

        # Status badge
        icon = STATUS_ICONS.get(topic["status"], "")
        sts_colors = {"Done": GREEN, "In Progress": YELLOW, "Pending": SUBTEXT}
        sts_color  = sts_colors.get(topic["status"], SUBTEXT)
        self.sts_badge.config(text=f"  {icon} {topic['status']}  ",
                               fg=BG if topic["status"] == "Done" else CARD,
                               bg=sts_color)

        # Text fields
        self.d_subject.config(text=topic["title"])
        self.d_topic.config(text=f"📁  {topic['category']}" if topic["category"] else "📁  No category")
        self.d_notes.config(text=topic["notes"] if topic["notes"] else "— No notes added —")
        self.d_created.config(text=f"🗓  Created : {topic.get('created_at', '—')}")
        self.d_updated.config(text=f"🔁  Updated : {topic.get('updated_at', '—')}")

    # ── helpers ──────────────────────────────
    def _selected_topic(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a topic first.")
            return None
        tid = int(sel[0])
        return next((t for t in self.app.data["topics"] if t["id"] == tid), None)

    def _edit_selected(self):
        topic = self._selected_topic()
        if topic:
            dialog = EditDialog(self, self.app, topic)
            self.wait_window(dialog)
            self.on_show()

    def _delete_selected(self):
        topic = self._selected_topic()
        if not topic:
            return
        if messagebox.askyesno("Delete", f"Delete '{topic['title']}'?"):
            self.app.data["topics"].remove(topic)
            save_data(self.app.data)
            self.on_show()
            messagebox.showinfo("Deleted", "Topic deleted successfully.")

    def _change_status(self):
        topic = self._selected_topic()
        if not topic:
            return
        dialog = StatusDialog(self, self.app, topic)
        self.wait_window(dialog)
        self.on_show()


# ─────────────────────────────────────────────
#  FRAME: ADD TOPIC
# ─────────────────────────────────────────────
class AddFrame(tk.Frame):
    key = "add"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=HEADER_BG, pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text="➕  Add New Topic", font=("Segoe UI", 18, "bold"),
                 bg=HEADER_BG, fg=ACCENT).pack(padx=24, anchor="w")

        form = card_frame(self, padx=40, pady=30)
        form.pack(padx=60, pady=30, fill="x")

        fields = [
            ("Subject (Title)",         "title"),
            ("Topic (Category)",        "category"),
            ("Notes / Details",         "notes"),
        ]
        self.vars = {}
        for label, key in fields:
            row = tk.Frame(form, bg=CARD)
            row.pack(fill="x", pady=8)
            tk.Label(row, text=label, font=("Segoe UI", 11), bg=CARD,
                     fg=SUBTEXT, width=22, anchor="w").pack(side="left")
            var = tk.StringVar()
            self.vars[key] = var
            make_entry(row, textvariable=var, width=45).pack(side="left")

        # Priority
        prow = tk.Frame(form, bg=CARD)
        prow.pack(fill="x", pady=8)
        tk.Label(prow, text="Priority", font=("Segoe UI", 11), bg=CARD,
                 fg=SUBTEXT, width=22, anchor="w").pack(side="left")
        self.priority_var = tk.StringVar(value="Medium")
        for val, color in [("High", RED), ("Medium", YELLOW), ("Low", GREEN)]:
            tk.Radiobutton(
                prow, text=val, variable=self.priority_var, value=val,
                bg=CARD, fg=color, selectcolor=CARD,
                activebackground=CARD, font=("Segoe UI", 11)
            ).pack(side="left", padx=12)

        # Buttons
        brow = tk.Frame(form, bg=CARD)
        brow.pack(pady=20)
        make_button(brow, "✅ Save Topic",  self._save,  ACCENT,  width=18).pack(side="left", padx=10)
        make_button(brow, "🗑️ Clear Form", self._clear, BTN_BG, width=14).pack(side="left", padx=10)

    def _save(self):
        title    = self.vars["title"].get().strip()
        category = self.vars["category"].get().strip()
        notes    = self.vars["notes"].get().strip()
        priority = self.priority_var.get()

        if not title:
            messagebox.showerror("Error", "Subject (Title) cannot be empty!")
            return

        self.app.refresh_data()
        topic = {
            "id"        : generate_id(self.app.data["topics"]),
            "title"     : title,
            "category"  : category,
            "priority"  : priority,
            "status"    : "Pending",
            "notes"     : notes,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.app.data["topics"].append(topic)
        save_data(self.app.data)
        messagebox.showinfo("Success", f"Topic '{title}' added successfully!")
        self._clear()

    def _clear(self):
        for var in self.vars.values():
            var.set("")
        self.priority_var.set("Medium")


# ─────────────────────────────────────────────
#  FRAME: SEARCH & FILTER
# ─────────────────────────────────────────────
class SearchFrame(tk.Frame):
    key = "search"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=HEADER_BG, pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔍  Search & Filter", font=("Segoe UI", 18, "bold"),
                 bg=HEADER_BG, fg=ACCENT).pack(padx=24, anchor="w")

        # Filter controls
        ctrl = card_frame(self, padx=24, pady=16)
        ctrl.pack(fill="x", padx=20, pady=12)

        row1 = tk.Frame(ctrl, bg=CARD)
        row1.pack(fill="x", pady=4)

        tk.Label(row1, text="Keyword:", font=("Segoe UI", 11),
                 bg=CARD, fg=SUBTEXT).pack(side="left", padx=(0,8))
        self.kw_var = tk.StringVar()
        make_entry(row1, textvariable=self.kw_var, width=22).pack(side="left", padx=(0,20))

        tk.Label(row1, text="Priority:", font=("Segoe UI", 11),
                 bg=CARD, fg=SUBTEXT).pack(side="left", padx=(0,8))
        self.pri_var = tk.StringVar(value="All")
        pri_cb = ttk.Combobox(row1, textvariable=self.pri_var,
                               values=["All", "High", "Medium", "Low"],
                               state="readonly", width=10,
                               font=("Segoe UI", 11))
        pri_cb.pack(side="left", padx=(0,20))

        tk.Label(row1, text="Status:", font=("Segoe UI", 11),
                 bg=CARD, fg=SUBTEXT).pack(side="left", padx=(0,8))
        self.sts_var = tk.StringVar(value="All")
        sts_cb = ttk.Combobox(row1, textvariable=self.sts_var,
                               values=["All", "Pending", "In Progress", "Done"],
                               state="readonly", width=14,
                               font=("Segoe UI", 11))
        sts_cb.pack(side="left", padx=(0,20))

        make_button(row1, "🔍 Search", self._search, ACCENT, width=12).pack(side="left", padx=8)
        make_button(row1, "✖ Clear",  self._clear,  BTN_BG, width=8).pack(side="left")

        # Results count
        self.result_lbl = tk.Label(ctrl, text="", font=("Segoe UI", 10),
                                    bg=CARD, fg=SUBTEXT)
        self.result_lbl.pack(anchor="w", pady=(8,0))

        # Treeview (reuse style set in ViewFrame)
        tree_frame = tk.Frame(self, bg=BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=8)

        cols = ("id", "subject", "topic", "priority", "status", "notes")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        col_cfg = [
            ("id",       "ID",        50),
            ("subject",  "Subject",  200),
            ("topic",    "Topic",    140),
            ("priority", "Priority",  90),
            ("status",   "Status",   130),
            ("notes",    "Notes",    260),
        ]
        for cid, cname, cw in col_cfg:
            self.tree.heading(cid, text=cname)
            self.tree.column(cid, width=cw, anchor="w" if cid in ("subject","topic","notes") else "center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("high",   foreground=RED)
        self.tree.tag_configure("medium", foreground=YELLOW)
        self.tree.tag_configure("low",    foreground=GREEN)

    def _search(self):
        self.app.refresh_data()
        kw  = self.kw_var.get().strip().lower()
        pri = self.pri_var.get()
        sts = self.sts_var.get()

        results = self.app.data["topics"]
        if kw:
            results = [t for t in results if kw in t["title"].lower() or kw in t["category"].lower() or kw in t["notes"].lower()]
        if pri != "All":
            results = [t for t in results if t["priority"] == pri]
        if sts != "All":
            results = [t for t in results if t["status"] == sts]

        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in results:
            icon = STATUS_ICONS.get(t["status"], "")
            self.tree.insert("", "end", tags=(t["priority"].lower(),),
                             values=(t["id"], t["title"], t["category"],
                                     t["priority"], f"{icon} {t['status']}", t["notes"]))
        self.result_lbl.config(text=f"  {len(results)} result(s) found.")

    def _clear(self):
        self.kw_var.set("")
        self.pri_var.set("All")
        self.sts_var.set("All")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.result_lbl.config(text="")

    def on_show(self):
        self._clear()


# ─────────────────────────────────────────────
#  FRAME: REPORT
# ─────────────────────────────────────────────
class ReportFrame(tk.Frame):
    key = "report"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=HEADER_BG, pady=16)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📊  Summary Report", font=("Segoe UI", 18, "bold"),
                 bg=HEADER_BG, fg=ACCENT).pack(padx=24, anchor="w")

        # Stats cards
        self.stats_frame = tk.Frame(self, bg=BG)
        self.stats_frame.pack(fill="x", padx=20, pady=16)

        # Progress bar section
        prog_card = card_frame(self, padx=24, pady=16)
        prog_card.pack(fill="x", padx=20, pady=4)
        tk.Label(prog_card, text="Overall Progress", font=("Segoe UI", 12, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w")
        self.prog_canvas = tk.Canvas(prog_card, height=28, bg=CARD, bd=0, highlightthickness=0)
        self.prog_canvas.pack(fill="x", pady=8)
        self.prog_lbl = tk.Label(prog_card, text="", font=("Segoe UI", 10),
                                  bg=CARD, fg=SUBTEXT)
        self.prog_lbl.pack(anchor="w")

        # Category breakdown
        cat_card = card_frame(self, padx=24, pady=16)
        cat_card.pack(fill="x", padx=20, pady=8)
        tk.Label(cat_card, text="📁 Category Breakdown", font=("Segoe UI", 12, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", pady=(0,8))
        self.cat_frame = tk.Frame(cat_card, bg=CARD)
        self.cat_frame.pack(fill="x")

        # Buttons
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=12)
        make_button(btn_row, "🔄 Refresh Report", self.on_show,       ACCENT,  width=20).pack(side="left", padx=10)
        make_button(btn_row, "💾 Save to File",   self._save_report,  ACCENT2, width=18).pack(side="left", padx=10)

    def on_show(self):
        self.app.refresh_data()
        topics  = self.app.data["topics"]
        total   = len(topics)
        done    = sum(1 for t in topics if t["status"] == "Done")
        prog    = sum(1 for t in topics if t["status"] == "In Progress")
        pending = sum(1 for t in topics if t["status"] == "Pending")
        high    = sum(1 for t in topics if t["priority"] == "High")

        # Stats cards
        for w in self.stats_frame.winfo_children():
            w.destroy()
        for label, val, color in [
            ("📚 Total", total, ACCENT2), ("✅ Done", done, GREEN),
            ("🔄 In Progress", prog, YELLOW), ("⏳ Pending", pending, RED),
            ("🔴 High Priority", high, RED),
        ]:
            box = card_frame(self.stats_frame, padx=16, pady=12)
            box.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(box, text=str(val), font=("Segoe UI", 26, "bold"),
                     bg=CARD, fg=color).pack()
            tk.Label(box, text=label, font=("Segoe UI", 9),
                     bg=CARD, fg=SUBTEXT).pack()

        # Progress bar
        self.prog_canvas.update_idletasks()
        W = self.prog_canvas.winfo_width() or 600
        pct = (done / total * 100) if total > 0 else 0
        filled_w = int(W * pct / 100)
        self.prog_canvas.delete("all")
        self.prog_canvas.create_rectangle(0, 4, W, 24, fill=BTN_BG, outline="")
        if filled_w > 0:
            self.prog_canvas.create_rectangle(0, 4, filled_w, 24, fill=GREEN, outline="")
        self.prog_lbl.config(text=f"  {pct:.1f}% complete  ({done} of {total} topics done)")

        # Category breakdown
        for w in self.cat_frame.winfo_children():
            w.destroy()
        categories = {}
        for t in topics:
            cat = t["category"] or "Uncategorized"
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in sorted(categories.items()):
            row = tk.Frame(self.cat_frame, bg=CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"  📁 {cat}", font=("Segoe UI", 10),
                     bg=CARD, fg=TEXT, width=28, anchor="w").pack(side="left")
            tk.Label(row, text=f"{count} topic(s)", font=("Segoe UI", 10),
                     bg=CARD, fg=ACCENT2).pack(side="left")

    def _save_report(self):
        self.app.refresh_data()
        topics = self.app.data["topics"]
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        lines = [
            "MindMapr – Smart Revision Assistant",
            f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 60, "",
        ]
        for t in topics:
            lines += [
                f"[{t['id']}] {t['title']}",
                f"    Topic    : {t['category']}",
                f"    Priority : {t['priority']}",
                f"    Status   : {t['status']}",
                f"    Notes    : {t['notes']}",
                f"    Updated  : {t['updated_at']}", "",
            ]
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        messagebox.showinfo("Saved", f"Report saved as:\n{filename}")


# ─────────────────────────────────────────────
#  DIALOG: EDIT TOPIC
# ─────────────────────────────────────────────
class EditDialog(tk.Toplevel):
    def __init__(self, parent, app, topic):
        super().__init__(parent)
        self.app   = app
        self.topic = topic
        self.title(f"Edit – {topic['title']}")
        self.geometry("500x420")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(self, text="✏️ Edit Topic", font=("Segoe UI", 15, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(20, 10))

        form = card_frame(self, padx=24, pady=20)
        form.pack(padx=20, fill="x")

        fields = [("Subject (Title)", "title"), ("Topic (Category)", "category"), ("Notes", "notes")]
        self.vars = {}
        for label, key in fields:
            row = tk.Frame(form, bg=CARD)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=label, font=("Segoe UI", 10), bg=CARD,
                     fg=SUBTEXT, width=20, anchor="w").pack(side="left")
            var = tk.StringVar(value=self.topic.get(key, ""))
            self.vars[key] = var
            make_entry(row, textvariable=var, width=28).pack(side="left")

        # Priority
        prow = tk.Frame(form, bg=CARD)
        prow.pack(fill="x", pady=6)
        tk.Label(prow, text="Priority", font=("Segoe UI", 10), bg=CARD,
                 fg=SUBTEXT, width=20, anchor="w").pack(side="left")
        self.pri_var = tk.StringVar(value=self.topic["priority"])
        for val, color in [("High", RED), ("Medium", YELLOW), ("Low", GREEN)]:
            tk.Radiobutton(prow, text=val, variable=self.pri_var, value=val,
                           bg=CARD, fg=color, selectcolor=CARD,
                           activebackground=CARD, font=("Segoe UI", 10)).pack(side="left", padx=8)

        # Status
        srow = tk.Frame(form, bg=CARD)
        srow.pack(fill="x", pady=6)
        tk.Label(srow, text="Status", font=("Segoe UI", 10), bg=CARD,
                 fg=SUBTEXT, width=20, anchor="w").pack(side="left")
        self.sts_var = tk.StringVar(value=self.topic["status"])
        ttk.Combobox(srow, textvariable=self.sts_var,
                     values=["Pending", "In Progress", "Done"],
                     state="readonly", width=14,
                     font=("Segoe UI", 10)).pack(side="left")

        # Buttons
        brow = tk.Frame(self, bg=BG)
        brow.pack(pady=16)
        make_button(brow, "💾 Save Changes", self._save, ACCENT,  width=16).pack(side="left", padx=8)
        make_button(brow, "Cancel",          self.destroy, BTN_BG, width=10).pack(side="left")

    def _save(self):
        title = self.vars["title"].get().strip()
        if not title:
            messagebox.showerror("Error", "Subject cannot be empty!", parent=self)
            return
        self.topic["title"]    = title
        self.topic["category"] = self.vars["category"].get().strip()
        self.topic["notes"]    = self.vars["notes"].get().strip()
        self.topic["priority"] = self.pri_var.get()
        self.topic["status"]   = self.sts_var.get()
        self.topic["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_data(self.app.data)
        messagebox.showinfo("Saved", "Topic updated successfully!", parent=self)
        self.destroy()


# ─────────────────────────────────────────────
#  DIALOG: CHANGE STATUS
# ─────────────────────────────────────────────
class StatusDialog(tk.Toplevel):
    def __init__(self, parent, app, topic):
        super().__init__(parent)
        self.app   = app
        self.topic = topic
        self.title("Change Status")
        self.geometry("340x220")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(self, text="🔄 Change Status", font=("Segoe UI", 14, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(20, 4))
        tk.Label(self, text=self.topic["title"], font=("Segoe UI", 11),
                 bg=BG, fg=SUBTEXT).pack(pady=(0, 16))

        self.sts_var = tk.StringVar(value=self.topic["status"])
        for val, icon in STATUS_ICONS.items():
            tk.Radiobutton(
                self, text=f"{icon}  {val}", variable=self.sts_var, value=val,
                bg=BG, fg=TEXT, selectcolor=BG,
                activebackground=BG, font=("Segoe UI", 11)
            ).pack(anchor="w", padx=60, pady=3)

        brow = tk.Frame(self, bg=BG)
        brow.pack(pady=14)
        make_button(brow, "✅ Apply", self._apply, ACCENT,  width=12).pack(side="left", padx=8)
        make_button(brow, "Cancel",  self.destroy, BTN_BG, width=10).pack(side="left")

    def _apply(self):
        self.topic["status"]     = self.sts_var.get()
        self.topic["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_data(self.app.data)
        self.destroy()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = MindMaprApp()
    app.mainloop()

