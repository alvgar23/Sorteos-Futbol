# -*- coding: utf-8 -*-
"""
Tournament Draw App (Tkinter Version)
Author: Avtomat Agentics
Date: 2025-11-11

This application allows you to load teams from a text file and perform
random tournament draws (Groups or Eliminations) with country restrictions.

Each line in the .txt file must follow this format:
Team,Country,Pot
Example:
Real Madrid,Spain,1
Chelsea,England,1
Benfica,Portugal,2
...
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import random


class TournamentDrawApp:
    """Main GUI class for the tournament draw application."""

    def __init__(self, root):
        """
        Initialize the main window, widgets, and variables.

        Args:
            root (tk.Tk): The main Tkinter root window.
        """
        self.root = root
        self.root.title("Tournament Draw App")
        self.root.geometry("800x600")
        self.root.configure(bg="#1c1c1c")

        # Variables
        self.teams_data = []
        self.draw_results = []
        self.mode = tk.StringVar(value="Groups")

        # --- GUI Layout ---
        title_label = tk.Label(
            root,
            text="Tournament Draw App",
            font=("Arial", 20, "bold"),
            fg="#00ffcc",
            bg="#1c1c1c",
        )
        title_label.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root, bg="#1c1c1c")
        btn_frame.pack(pady=10)

        load_btn = tk.Button(
            btn_frame,
            text="Load Teams (.txt)",
            command=self.load_file,
            width=18,
            font=("Arial", 12),
        )
        load_btn.grid(row=0, column=0, padx=10)

        draw_btn = tk.Button(
            btn_frame,
            text="Perform Draw",
            command=self.perform_draw,
            width=18,
            font=("Arial", 12),
        )
        draw_btn.grid(row=0, column=1, padx=10)

        export_btn = tk.Button(
            btn_frame,
            text="Export to CSV",
            command=self.export_to_csv,
            width=18,
            font=("Arial", 12),
        )
        export_btn.grid(row=0, column=2, padx=10)

        # Radio Buttons (Mode Selection)
        mode_frame = tk.LabelFrame(
            root, text="Draw Mode", bg="#1c1c1c", fg="#00ffcc", font=("Arial", 12)
        )
        mode_frame.pack(pady=10)
        tk.Radiobutton(
            mode_frame,
            text="Groups",
            variable=self.mode,
            value="Groups",
            command=self.on_mode_change,
            bg="#1c1c1c",
            fg="white",
        ).pack(side="left", padx=20)
        tk.Radiobutton(
            mode_frame,
            text="Eliminations",
            variable=self.mode,
            value="Eliminations",
            command=self.on_mode_change,
            bg="#1c1c1c",
            fg="white",
        ).pack(side="left", padx=20)

        # Text Box for Output
        self.text_box = tk.Text(
            root,
            height=20,
            width=90,
            wrap="word",
            font=("Courier", 11),
            bg="#2b2b2b",
            fg="#00ff99",
        )
        self.text_box.pack(pady=10)

    # ============================================================
    # STEP 1 — Load file
    # ============================================================

    def load_file(self):
        """Open file dialog to load teams from a .txt file."""
        file_path = filedialog.askopenfilename(
            title="Select team file", filetypes=[("Text Files", "*.txt")]
        )
        if not file_path:
            return

        self.teams_data.clear()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        name, country, pot = parts
                        self.teams_data.append(
                            {"name": name.strip(), "country": country.strip(), "pot": pot.strip()}
                        )
            self.show_message(f"Loaded {len(self.teams_data)} teams from file: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file:\n{e}")

    # ============================================================
    # STEP 2 — Mode selection
    # ============================================================

    def on_mode_change(self):
        """Display selected mode in text box."""
        self.show_message(f"Draw mode selected: {self.mode.get()}")

    # ============================================================
    # STEP 3 — Group draw logic (Option B, corrected)
    # ============================================================

    def perform_group_draw(self):
        """Perform draw for 'Groups' mode using flexible pot assignment with country constraints."""
        if not self.teams_data:
            self.show_message("No teams loaded.")
            return []

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, "==== TOURNAMENT DRAW RESULTS (GROUPS) ====\n\n")

        # Organize teams by pot
        pots = {}
        for t in self.teams_data:
            pots.setdefault(t["pot"], []).append(t)

        # Determine correct number of groups
        pot_sizes = [len(p) for p in pots.values()]
        group_count = min(pot_sizes)

        if len(set(pot_sizes)) != 1:
            self.show_message("Warning: Pots are uneven. Extra teams will be placed after main distribution.")

        # Create empty groups
        groups = [[] for _ in range(group_count)]

        # Shuffle all pots
        for plist in pots.values():
            random.shuffle(plist)

        # Assign 1 team per pot to each group (Option B: choose the best group per team)
        for pot_key in sorted(pots.keys(), key=lambda x: int(x)):
            pot_list = pots[pot_key].copy()

            # First pass: assign one team per group
            for team in pot_list[:group_count]:
                # Find groups that do NOT yet have this pot
                candidate_groups = [
                    g for g in groups
                    if pot_key not in [t["pot"] for t in g]
                ]

                # Among those groups, prefer ones without same country
                clean_group = None
                for g in candidate_groups:
                    if all(t["country"] != team["country"] for t in g):
                        clean_group = g
                        break

                if clean_group:
                    clean_group.append(team)
                else:
                    # No clean option, assign to first candidate
                    candidate_groups[0].append(team)

            # Second pass: handle leftover teams (only if pots are uneven)
            leftovers = pot_list[group_count:]
            for team in leftovers:
                placed = False

                # Try groups without country conflict
                for g in groups:
                    if all(t["country"] != team["country"] for t in g):
                        g.append(team)
                        placed = True
                        break

                if not placed:
                    # Place in group with the fewest teams
                    smallest = min(groups, key=lambda x: len(x))
                    smallest.append(team)

        # Display groups
        for i, g in enumerate(groups, start=1):
            self.text_box.insert(tk.END, f"Group {i}:\n")
            for team in g:
                self.text_box.insert(
                    tk.END,
                    f"  {team['name']} ({team['country']}) - Pot {team['pot']}\n"
                )
            self.text_box.insert(tk.END, "\n")

        self.draw_results = groups
        return groups

    # ============================================================
    # STEP 4 — Eliminations draw logic (works perfectly)
    # ============================================================

    def perform_elimination_draw(self):
        """Perform draw for 'Eliminations' mode keeping 1-vs-2 structure and avoiding country clashes."""
        if not self.teams_data:
            self.show_message("No teams loaded.")
            return []

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, "==== TOURNAMENT DRAW RESULTS (ELIMINATIONS) ====\n\n")

        # Organize by pot
        pots = {}
        for t in self.teams_data:
            pots.setdefault(t["pot"], []).append(t)

        # Pot 1 is heads of series
        pot1 = pots.get("1", [])
        pot2 = []

        # Merge remaining pots into pot 2
        for pk, plist in pots.items():
            if pk != "1":
                pot2.extend(plist)

        if len(pots.keys()) > 2:
            self.show_message("Warning: Only Pot 1 and Pot 2 are used in eliminations. Extra pots moved to Pot 2.")

        random.shuffle(pot1)
        random.shuffle(pot2)

        matches = []

        # Pairing 1 vs 2
        for team1 in pot1:
            opponent = None

            # Try to avoid same country
            for t in pot2:
                if t["country"] != team1["country"]:
                    opponent = t
                    break

            if opponent:
                pot2.remove(opponent)
                matches.append([team1, opponent])
            else:
                # No option, take first available
                if pot2:
                    opponent = pot2.pop(0)
                    matches.append([team1, opponent])
                else:
                    matches.append([team1])

        # Handle leftover (odd pot2)
        if pot2:
            leftover = pot2.pop(0)
            self.show_message("Info: One leftover Pot 2 team was added to the best available match.")

            placed = False
            for match in matches:
                match_countries = [t["country"] for t in match]
                if leftover["country"] not in match_countries:
                    match.append(leftover)
                    placed = True
                    break

            if not placed:
                matches[-1].append(leftover)

        # Display matches
        for i, m in enumerate(matches, start=1):
            self.text_box.insert(tk.END, f"Match {i}:\n")
            for t in m:
                self.text_box.insert(
                    tk.END,
                    f"  {t['name']} ({t['country']}) - Pot {t['pot']}\n"
                )
            self.text_box.insert(tk.END, "\n")

        self.draw_results = matches
        return matches

    # ============================================================
    # STEP 5 — CSV export
    # ============================================================

    def export_to_csv(self):
        """Export the last draw results to a CSV file."""
        if not self.draw_results:
            self.show_message("No draw results to export.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Group/Match", "Team", "Country", "Pot"])
                for i, group in enumerate(self.draw_results, start=1):
                    for team in group:
                        writer.writerow(
                            [f"Group {i}" if self.mode.get() == "Groups" else f"Match {i}",
                             team["name"], team["country"], team["pot"]]
                        )
            self.show_message(f"Draw exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting CSV:\n{e}")

    # ============================================================
    # STEP 6 — Final integration
    # ============================================================

    def perform_draw(self):
        """Run the selected draw mode."""
        if self.mode.get() == "Groups":
            self.perform_group_draw()
        else:
            self.perform_elimination_draw()

    # Utility method
    def show_message(self, msg):
        """Display a message in the text box."""
        self.text_box.insert(tk.END, f"{msg}\n")
        self.text_box.see(tk.END)


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentDrawApp(root)
    root.mainloop()