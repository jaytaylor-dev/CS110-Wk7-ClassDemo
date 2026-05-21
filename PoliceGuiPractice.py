"""
PREDICTIVE POLICING: A FEEDBACK LOOP DEMO
==========================================
A teaching tool for a computing ethics class studying Cathy O'Neil's
"Weapons of Math Destruction."

THE CORE IDEA (O'Neil, Ch. 5 "Civilian Casualties: Justice in the Age
of Big Data"):

  A predictive policing model does NOT measure crime.
  It measures *recorded* crime --- arrests, citations, stops.
  Recorded crime depends on where police look.
  Where police look depends on the model.

  So the model's "predictions" become self-fulfilling. A district
  flagged as high-risk gets more patrols, more patrols find more
  low-level offenses, those offenses feed back into the model as
  proof the district was high-risk all along. The loop tightens.

THE SETUP:
  Two neighborhoods, A and B, with IDENTICAL true underlying crime.
  We seed the model with a tiny, arbitrary initial bias toward A
  (imagine a single noisy data point, or a historical prejudice).
  Then we just let the loop run. Press the button and watch.

  Nothing about the neighborhoods differs. Only the model's
  attention differs --- and that turns out to be enough.
"""

import tkinter as tk
from tkinter import ttk
import random


# ----------------------------------------------------------------------
# THE MODEL
# ----------------------------------------------------------------------
# Each neighborhood has the SAME true crime rate. The only thing that
# changes over time is how many patrols we send and therefore how much
# crime we *record*. Recorded crime feeds the risk score; the risk
# score decides patrols. That is the entire feedback loop.

class Neighborhood:
    def __init__(self, name, true_crime_rate):
        self.name = name
        self.true_crime_rate = true_crime_rate   # the REALITY (never changes)
        self.risk_score = 50.0                    # the model's belief
        self.patrols = 5                          # patrols sent this week
        self.recorded_total = 0                   # cumulative recorded crime
        self.history = []                         # risk score over time


class PredictivePolicingModel:
    def __init__(self):
        # Two identical neighborhoods. Same true crime. Same everything.
        self.A = Neighborhood("Neighborhood A", true_crime_rate=0.30)
        self.B = Neighborhood("Neighborhood B", true_crime_rate=0.30)

        # THE ORIGINAL SIN: a tiny arbitrary nudge toward A.
        # Maybe a noisy historical arrest record. Maybe a biased cop.
        # Maybe pure chance. It does not matter --- watch what it becomes.
        self.A.risk_score = 55.0
        self.B.risk_score = 45.0

        self.week = 0
        self.total_patrols = 20  # fixed budget, allocated by risk score

    def step(self):
        """Advance one week. This is the whole loop."""
        self.week += 1

        # 1. ALLOCATE PATROLS by risk score (higher risk -> more patrols).
        #    The model directs attention based on its current belief.
        total_risk = self.A.risk_score + self.B.risk_score
        self.A.patrols = round(self.total_patrols * self.A.risk_score / total_risk)
        self.B.patrols = self.total_patrols - self.A.patrols

        # 2. RECORD CRIME. Here is the trap: recorded crime = true crime
        #    rate * how hard you look. Same true rate in both places, but
        #    more patrols means more recorded incidents. The model never
        #    sees true crime --- only what its own patrols dig up.
        avg_patrols = self.total_patrols / 2.0   # what "fair" attention looks like
        for n in (self.A, self.B):
            recorded = n.true_crime_rate * n.patrols * random.uniform(0.9, 1.1)
            n.recorded_total += recorded

            # 3. UPDATE THE RISK SCORE. The model converts recorded crime
            #    into a "crimes found PER PATROL VISIT relative to normal"
            #    signal. The dishonesty: a neighborhood watched twice as
            #    hard records twice as much, and the model reads that extra
            #    haul as proof of extra danger --- so it nudges the score UP.
            #    More patrols than average -> score rises. Fewer -> score
            #    falls. That is what makes the loop compound instead of
            #    settling. Attention literally becomes evidence.
            attention_ratio = n.patrols / avg_patrols   # >1 = over-watched
            n.risk_score *= (1.0 + 0.18 * (attention_ratio - 1.0))
            n.risk_score = max(1.0, min(99.0, n.risk_score))
            n.history.append(n.risk_score)


# ----------------------------------------------------------------------
# THE GUI
# ----------------------------------------------------------------------

class DemoApp:
    BG = "#1a1a2e"
    FG = "#e8e8f0"
    ACCENT = "#e94560"
    CALM = "#16c79a"
    PANEL = "#16213e"

    def __init__(self, root):
        self.root = root
        self.model = PredictivePolicingModel()

        root.title("Predictive Policing  --  A Weapons of Math Destruction Demo")
        root.configure(bg=self.BG)
        root.geometry("780x680")

        # ---- Title ----
        tk.Label(root, text="PREDICTIVE POLICING SIMULATOR",
                 font=("Helvetica", 20, "bold"),
                 bg=self.BG, fg=self.FG).pack(pady=(18, 2))
        tk.Label(root,
                 text="Two neighborhoods. Identical true crime rate (30%). Watch what the model does.",
                 font=("Helvetica", 11),
                 bg=self.BG, fg="#9a9ab0").pack(pady=(0, 12))

        # ---- The two neighborhood panels ----
        panels = tk.Frame(root, bg=self.BG)
        panels.pack(pady=6)
        self.panel_A = self._make_panel(panels, "Neighborhood A", 0)
        self.panel_B = self._make_panel(panels, "Neighborhood B", 1)

        # ---- Week counter ----
        self.week_label = tk.Label(root, text="Week 0",
                                   font=("Helvetica", 14, "bold"),
                                   bg=self.BG, fg=self.FG)
        self.week_label.pack(pady=(14, 6))

        # ---- Buttons ----
        btns = tk.Frame(root, bg=self.BG)
        btns.pack(pady=8)
        self.step_btn = tk.Button(btns, text="  Send Patrols  ->  Next Week  ",
                                  font=("Helvetica", 13, "bold"),
                                  bg=self.ACCENT, fg="white",
                                  activebackground="#c13651", activeforeground="white",
                                  relief="flat", padx=14, pady=8,
                                  command=self.step)
        self.step_btn.grid(row=0, column=0, padx=6)
        tk.Button(btns, text="  Reset  ",
                  font=("Helvetica", 13),
                  bg=self.PANEL, fg=self.FG,
                  activebackground="#0f1830", activeforeground=self.FG,
                  relief="flat", padx=14, pady=8,
                  command=self.reset).grid(row=0, column=1, padx=6)

        # ---- The punchline label (revealed as the gap grows) ----
        self.verdict = tk.Label(root, text="",
                                font=("Helvetica", 12, "italic"),
                                bg=self.BG, fg=self.ACCENT, wraplength=700,
                                justify="center")
        self.verdict.pack(pady=(16, 4))

        self.refresh()

    def _make_panel(self, parent, title, col):
        frame = tk.Frame(parent, bg=self.PANEL, padx=22, pady=18,
                         highlightbackground="#0f1830", highlightthickness=2)
        frame.grid(row=0, column=col, padx=12)

        tk.Label(frame, text=title, font=("Helvetica", 15, "bold"),
                 bg=self.PANEL, fg=self.FG).pack()

        risk_val = tk.Label(frame, text="50", font=("Helvetica", 42, "bold"),
                            bg=self.PANEL, fg=self.FG)
        risk_val.pack(pady=(6, 0))
        tk.Label(frame, text="RISK SCORE", font=("Helvetica", 9),
                 bg=self.PANEL, fg="#9a9ab0").pack()

        bar = ttk.Progressbar(frame, length=180, maximum=100)
        bar.pack(pady=12)

        patrol_lbl = tk.Label(frame, text="Patrols this week: 5",
                              font=("Helvetica", 11), bg=self.PANEL, fg=self.FG)
        patrol_lbl.pack(pady=2)
        recorded_lbl = tk.Label(frame, text="Recorded crime (total): 0.0",
                                font=("Helvetica", 11), bg=self.PANEL, fg=self.FG)
        recorded_lbl.pack(pady=2)
        truth_lbl = tk.Label(frame, text="TRUE crime rate: 30%",
                             font=("Helvetica", 11, "bold"),
                             bg=self.PANEL, fg=self.CALM)
        truth_lbl.pack(pady=(8, 0))

        return {"risk": risk_val, "bar": bar, "patrol": patrol_lbl,
                "recorded": recorded_lbl, "frame": frame}

    def _update_panel(self, panel, n):
        panel["risk"].config(text=f"{n.risk_score:.0f}")
        panel["bar"]["value"] = n.risk_score
        panel["patrol"].config(text=f"Patrols this week: {n.patrols}")
        panel["recorded"].config(text=f"Recorded crime (total): {n.recorded_total:.1f}")

        # Color the panel border red as risk climbs --- visual drama.
        if n.risk_score > 70:
            panel["frame"].config(highlightbackground=self.ACCENT)
            panel["risk"].config(fg=self.ACCENT)
        elif n.risk_score < 30:
            panel["frame"].config(highlightbackground=self.CALM)
            panel["risk"].config(fg=self.CALM)
        else:
            panel["frame"].config(highlightbackground="#0f1830")
            panel["risk"].config(fg=self.FG)

    def refresh(self):
        self._update_panel(self.panel_A, self.model.A)
        self._update_panel(self.panel_B, self.model.B)
        self.week_label.config(text=f"Week {self.model.week}")

        gap = abs(self.model.A.risk_score - self.model.B.risk_score)
        if self.model.week == 0:
            self.verdict.config(
                text="Both neighborhoods are identical. The only difference is a "
                     "tiny arbitrary nudge in the model's starting belief. Press the button.")
        elif gap > 50:
            self.verdict.config(
                text="The model now treats these neighborhoods as worlds apart. "
                     "But their TRUE crime rate (green) never changed --- it was 30% the "
                     "whole time. The model didn't discover crime. It manufactured a "
                     "high-risk zone out of its own attention.")
        elif gap > 20:
            self.verdict.config(
                text="The gap is widening. More patrols -> more recorded incidents -> "
                     "higher risk score -> even more patrols. The loop is feeding itself.")
        else:
            self.verdict.config(
                text="Watch the risk scores begin to diverge, even though the green "
                     "TRUE crime rate is identical in both.")

    def step(self):
        self.model.step()
        self.refresh()

    def reset(self):
        self.model = PredictivePolicingModel()
        self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app = DemoApp(root)
    root.mainloop()