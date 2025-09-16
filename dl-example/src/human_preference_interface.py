"""
Human Preference Interface for DPbQN Algorithm

This module provides interfaces for collecting and processing human preferences
to guide the Deep Preference-based Q Network optimization process.

Author: Generated for Logos/Nimbus/Status ecosystem research
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, asdict
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from abc import ABC, abstractmethod

from dpbqn_algorithm import PortfolioSolution, HumanPreference, ProjectSchedule


class PreferenceInterface(ABC):
    """Abstract base class for preference collection interfaces"""

    @abstractmethod
    def collect_preference(self, solution1: PortfolioSolution,
                          solution2: PortfolioSolution) -> Optional[HumanPreference]:
        """Collect human preference between two solutions"""
        pass

    @abstractmethod
    def display_solution(self, solution: PortfolioSolution) -> str:
        """Display solution in human-readable format"""
        pass


class CLIPreferenceInterface(PreferenceInterface):
    """Command-line interface for collecting preferences"""

    def __init__(self, evaluator_id: str = "human_evaluator"):
        self.evaluator_id = evaluator_id

    def display_solution(self, solution: PortfolioSolution) -> str:
        """Display solution in human-readable format"""
        display = f"""
Portfolio Solution:
==================
Selected Projects: {', '.join(solution.selected_projects)}
Total Cost: ${solution.total_cost:,.2f}
Total Duration: {solution.total_duration} time units
Risk Score: {solution.risk_score:.2f}
Feasibility: {solution.feasibility_score:.2f}

Project Schedules:
"""

        for schedule in solution.schedules:
            display += f"""
  - {schedule.project_id}:
    Start Time: {schedule.start_time}
    Duration: {schedule.duration}
    Resources: {', '.join([f'{k}: {v:.2f}' for k, v in schedule.resources_allocated.items()])}
    Priority: {schedule.priority:.2f}
"""

        return display

    def collect_preference(self, solution1: PortfolioSolution,
                          solution2: PortfolioSolution) -> Optional[HumanPreference]:
        """Collect human preference via command line"""
        print("\n" + "="*60)
        print("HUMAN PREFERENCE COLLECTION")
        print("="*60)

        print("\nSOLUTION A:")
        print(self.display_solution(solution1))

        print("\nSOLUTION B:")
        print(self.display_solution(solution2))

        print("\nWhich solution do you prefer?")
        print("1. Solution A")
        print("2. Solution B")
        print("3. No preference / Skip")

        while True:
            try:
                choice = input("Enter your choice (1/2/3): ").strip()

                if choice == '3':
                    return None

                if choice not in ['1', '2']:
                    print("Please enter 1, 2, or 3")
                    continue

                # Get preference strength
                while True:
                    try:
                        strength_input = input("How strong is your preference? (1=weak, 5=strong): ").strip()
                        strength = float(strength_input)
                        if 1 <= strength <= 5:
                            # Normalize to 0-1 range
                            preference_strength = (strength - 1) / 4
                            break
                        else:
                            print("Please enter a value between 1 and 5")
                    except ValueError:
                        print("Please enter a valid number")

                # Get confidence level
                while True:
                    try:
                        confidence_input = input("How confident are you? (1=not confident, 5=very confident): ").strip()
                        confidence = float(confidence_input)
                        if 1 <= confidence <= 5:
                            # Normalize to 0-1 range
                            confidence_normalized = (confidence - 1) / 4
                            break
                        else:
                            print("Please enter a value between 1 and 5")
                    except ValueError:
                        print("Please enter a valid number")

                # Get optional reasoning
                reasoning = input("Optional - Why do you prefer this solution? (press Enter to skip): ").strip()
                if not reasoning:
                    reasoning = None

                # Create preference object
                preferred_solution = solution1 if choice == '1' else solution2
                alternative_solution = solution2 if choice == '1' else solution1

                preference = HumanPreference(
                    preferred_solution=preferred_solution,
                    alternative_solution=alternative_solution,
                    preference_strength=preference_strength,
                    evaluator_id=self.evaluator_id,
                    confidence=confidence_normalized,
                    timestamp=datetime.now().isoformat(),
                    reasoning=reasoning
                )

                return preference

            except KeyboardInterrupt:
                print("\nOperation cancelled by user")
                return None
            except Exception as e:
                print(f"Error: {e}. Please try again.")


class GUIPreferenceInterface(PreferenceInterface):
    """Graphical user interface for collecting preferences"""

    def __init__(self, evaluator_id: str = "human_evaluator"):
        self.evaluator_id = evaluator_id
        self.preference_result = None
        self.root = None

    def display_solution(self, solution: PortfolioSolution) -> str:
        """Display solution in human-readable format"""
        display = f"Selected Projects: {', '.join(solution.selected_projects)}\n"
        display += f"Total Cost: ${solution.total_cost:,.2f}\n"
        display += f"Total Duration: {solution.total_duration} time units\n"
        display += f"Risk Score: {solution.risk_score:.2f}\n"
        display += f"Feasibility: {solution.feasibility_score:.2f}\n\n"

        display += "Project Schedules:\n"
        for schedule in solution.schedules:
            display += f"• {schedule.project_id}: Start {schedule.start_time}, Duration {schedule.duration}\n"
            resource_str = ', '.join([f'{k}: {v:.2f}' for k, v in schedule.resources_allocated.items()])
            display += f"  Resources: {resource_str}\n"

        return display

    def collect_preference(self, solution1: PortfolioSolution,
                          solution2: PortfolioSolution) -> Optional[HumanPreference]:
        """Collect human preference via GUI"""
        self.preference_result = None

        # Create GUI window
        self.root = tk.Tk()
        self.root.title("Portfolio Solution Preference Collection")
        self.root.geometry("800x600")

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Which portfolio solution do you prefer?",
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Solution A frame
        solution_a_frame = ttk.LabelFrame(main_frame, text="Solution A", padding="10")
        solution_a_frame.grid(row=1, column=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))

        solution_a_text = tk.Text(solution_a_frame, height=15, width=35, wrap=tk.WORD)
        solution_a_text.insert(tk.END, self.display_solution(solution1))
        solution_a_text.config(state=tk.DISABLED)
        solution_a_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Solution B frame
        solution_b_frame = ttk.LabelFrame(main_frame, text="Solution B", padding="10")
        solution_b_frame.grid(row=1, column=1, padx=(10, 0), sticky=(tk.W, tk.E, tk.N, tk.S))

        solution_b_text = tk.Text(solution_b_frame, height=15, width=35, wrap=tk.WORD)
        solution_b_text.insert(tk.END, self.display_solution(solution2))
        solution_b_text.config(state=tk.DISABLED)
        solution_b_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Preference selection frame
        pref_frame = ttk.Frame(main_frame)
        pref_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0), sticky=(tk.W, tk.E))

        # Radio buttons for preference
        preference_var = tk.StringVar(value="")

        ttk.Label(pref_frame, text="Your preference:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W)

        pref_a_radio = ttk.Radiobutton(pref_frame, text="Solution A", variable=preference_var, value="A")
        pref_a_radio.grid(row=1, column=0, sticky=tk.W, padx=(20, 0))

        pref_b_radio = ttk.Radiobutton(pref_frame, text="Solution B", variable=preference_var, value="B")
        pref_b_radio.grid(row=1, column=1, sticky=tk.W, padx=(20, 0))

        no_pref_radio = ttk.Radiobutton(pref_frame, text="No preference", variable=preference_var, value="None")
        no_pref_radio.grid(row=1, column=2, sticky=tk.W, padx=(20, 0))

        # Strength scale
        ttk.Label(pref_frame, text="Preference strength:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        strength_var = tk.DoubleVar(value=3.0)
        strength_scale = ttk.Scale(pref_frame, from_=1, to=5, variable=strength_var, orient=tk.HORIZONTAL, length=200)
        strength_scale.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=(20, 0))

        strength_label = ttk.Label(pref_frame, text="3 (Moderate)")
        strength_label.grid(row=3, column=2, sticky=tk.W, padx=(10, 0))

        def update_strength_label(*args):
            val = strength_var.get()
            labels = {1: "1 (Weak)", 2: "2 (Slight)", 3: "3 (Moderate)", 4: "4 (Strong)", 5: "5 (Very Strong)"}
            strength_label.config(text=labels.get(round(val), f"{val:.1f}"))

        strength_var.trace('w', update_strength_label)

        # Confidence scale
        ttk.Label(pref_frame, text="Confidence level:", font=('Arial', 12)).grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        confidence_var = tk.DoubleVar(value=3.0)
        confidence_scale = ttk.Scale(pref_frame, from_=1, to=5, variable=confidence_var, orient=tk.HORIZONTAL, length=200)
        confidence_scale.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=(20, 0))

        confidence_label = ttk.Label(pref_frame, text="3 (Moderate)")
        confidence_label.grid(row=5, column=2, sticky=tk.W, padx=(10, 0))

        def update_confidence_label(*args):
            val = confidence_var.get()
            labels = {1: "1 (Low)", 2: "2 (Slight)", 3: "3 (Moderate)", 4: "4 (High)", 5: "5 (Very High)"}
            confidence_label.config(text=labels.get(round(val), f"{val:.1f}"))

        confidence_var.trace('w', update_confidence_label)

        # Reasoning text box
        ttk.Label(pref_frame, text="Reasoning (optional):", font=('Arial', 12)).grid(row=6, column=0, sticky=tk.W, pady=(15, 5))
        reasoning_text = tk.Text(pref_frame, height=3, width=60)
        reasoning_text.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        # Buttons
        button_frame = ttk.Frame(pref_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=(10, 0))

        def on_submit():
            pref = preference_var.get()
            if not pref or pref == "None":
                self.preference_result = None
            else:
                preferred_solution = solution1 if pref == "A" else solution2
                alternative_solution = solution2 if pref == "A" else solution1

                reasoning = reasoning_text.get("1.0", tk.END).strip()
                if not reasoning:
                    reasoning = None

                self.preference_result = HumanPreference(
                    preferred_solution=preferred_solution,
                    alternative_solution=alternative_solution,
                    preference_strength=(strength_var.get() - 1) / 4,  # Normalize to 0-1
                    evaluator_id=self.evaluator_id,
                    confidence=(confidence_var.get() - 1) / 4,  # Normalize to 0-1
                    timestamp=datetime.now().isoformat(),
                    reasoning=reasoning
                )

            self.root.quit()
            self.root.destroy()

        def on_cancel():
            self.preference_result = None
            self.root.quit()
            self.root.destroy()

        submit_btn = ttk.Button(button_frame, text="Submit", command=on_submit)
        submit_btn.grid(row=0, column=0, padx=(0, 10))

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=on_cancel)
        cancel_btn.grid(row=0, column=1)

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        solution_a_frame.columnconfigure(0, weight=1)
        solution_a_frame.rowconfigure(0, weight=1)

        solution_b_frame.columnconfigure(0, weight=1)
        solution_b_frame.rowconfigure(0, weight=1)

        # Run the GUI
        self.root.mainloop()

        return self.preference_result


class BatchPreferenceCollector:
    """Collects multiple preferences in batch for efficiency"""

    def __init__(self, interface: PreferenceInterface):
        self.interface = interface
        self.collected_preferences: List[HumanPreference] = []

    def collect_pairwise_preferences(self, solutions: List[PortfolioSolution],
                                   max_comparisons: Optional[int] = None) -> List[HumanPreference]:
        """
        Collect pairwise preferences between solutions

        Args:
            solutions: List of portfolio solutions
            max_comparisons: Maximum number of pairwise comparisons

        Returns:
            List of collected preferences
        """
        preferences = []
        comparisons_made = 0

        # Generate all possible pairs
        for i in range(len(solutions)):
            for j in range(i + 1, len(solutions)):
                if max_comparisons and comparisons_made >= max_comparisons:
                    break

                print(f"\nComparison {comparisons_made + 1}" +
                      (f" of {max_comparisons}" if max_comparisons else ""))

                preference = self.interface.collect_preference(solutions[i], solutions[j])
                if preference:
                    preferences.append(preference)

                comparisons_made += 1

            if max_comparisons and comparisons_made >= max_comparisons:
                break

        self.collected_preferences.extend(preferences)
        return preferences

    def collect_ranking_preferences(self, solutions: List[PortfolioSolution]) -> List[HumanPreference]:
        """
        Collect preferences by having user rank solutions

        Args:
            solutions: List of portfolio solutions

        Returns:
            List of inferred pairwise preferences
        """
        print("\n" + "="*60)
        print("SOLUTION RANKING")
        print("="*60)

        # Display all solutions
        for i, solution in enumerate(solutions):
            print(f"\nSOLUTION {i + 1}:")
            print(self.interface.display_solution(solution))

        # Get ranking
        print(f"\nRank these solutions from best (1) to worst ({len(solutions)}):")
        ranking = {}

        for i in range(len(solutions)):
            while True:
                try:
                    rank_input = input(f"Rank for Solution {i + 1} (1-{len(solutions)}): ").strip()
                    rank = int(rank_input)
                    if 1 <= rank <= len(solutions):
                        if rank in ranking.values():
                            print(f"Rank {rank} already assigned. Please choose a different rank.")
                            continue
                        ranking[i] = rank
                        break
                    else:
                        print(f"Please enter a rank between 1 and {len(solutions)}")
                except ValueError:
                    print("Please enter a valid integer")

        # Convert ranking to pairwise preferences
        preferences = []
        for i in range(len(solutions)):
            for j in range(len(solutions)):
                if i != j and ranking[i] < ranking[j]:  # solution i is ranked better than j
                    preference = HumanPreference(
                        preferred_solution=solutions[i],
                        alternative_solution=solutions[j],
                        preference_strength=0.8,  # Strong preference from ranking
                        evaluator_id=self.interface.evaluator_id,
                        confidence=0.9,
                        timestamp=datetime.now().isoformat(),
                        reasoning=f"Ranked solution {i+1} as {ranking[i]} vs solution {j+1} as {ranking[j]}"
                    )
                    preferences.append(preference)

        self.collected_preferences.extend(preferences)
        return preferences

    def export_preferences(self, filename: str):
        """Export collected preferences to JSON file"""
        preferences_data = []
        for pref in self.collected_preferences:
            # Convert preference to serializable format
            pref_dict = {
                'evaluator_id': pref.evaluator_id,
                'preference_strength': pref.preference_strength,
                'confidence': pref.confidence,
                'timestamp': pref.timestamp,
                'reasoning': pref.reasoning,
                'criteria_focus': pref.criteria_focus,
                'preferred_solution': {
                    'selected_projects': pref.preferred_solution.selected_projects,
                    'total_cost': pref.preferred_solution.total_cost,
                    'total_duration': pref.preferred_solution.total_duration,
                    'risk_score': pref.preferred_solution.risk_score,
                    'feasibility_score': pref.preferred_solution.feasibility_score
                },
                'alternative_solution': {
                    'selected_projects': pref.alternative_solution.selected_projects,
                    'total_cost': pref.alternative_solution.total_cost,
                    'total_duration': pref.alternative_solution.total_duration,
                    'risk_score': pref.alternative_solution.risk_score,
                    'feasibility_score': pref.alternative_solution.feasibility_score
                }
            }
            preferences_data.append(pref_dict)

        with open(filename, 'w') as f:
            json.dump(preferences_data, f, indent=2)

        print(f"Exported {len(preferences_data)} preferences to {filename}")

    def get_preference_statistics(self) -> Dict[str, Any]:
        """Get statistics about collected preferences"""
        if not self.collected_preferences:
            return {}

        strengths = [p.preference_strength for p in self.collected_preferences]
        confidences = [p.confidence for p in self.collected_preferences]

        return {
            'total_preferences': len(self.collected_preferences),
            'average_strength': np.mean(strengths),
            'average_confidence': np.mean(confidences),
            'strength_std': np.std(strengths),
            'confidence_std': np.std(confidences),
            'evaluators': list(set(p.evaluator_id for p in self.collected_preferences)),
            'with_reasoning': sum(1 for p in self.collected_preferences if p.reasoning)
        }


class PreferenceGuidedSampling:
    """Uses human preferences to guide solution sampling and generation"""

    def __init__(self, collected_preferences: List[HumanPreference]):
        self.preferences = collected_preferences

    def analyze_preference_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in human preferences"""
        if not self.preferences:
            return {}

        # Analyze preferred characteristics
        preferred_costs = []
        preferred_durations = []
        preferred_project_counts = []

        for pref in self.preferences:
            preferred_costs.append(pref.preferred_solution.total_cost)
            preferred_durations.append(pref.preferred_solution.total_duration)
            preferred_project_counts.append(len(pref.preferred_solution.selected_projects))

        # Analyze project selection patterns
        project_preferences = {}
        for pref in self.preferences:
            for project in pref.preferred_solution.selected_projects:
                project_preferences[project] = project_preferences.get(project, 0) + 1

        return {
            'preferred_cost_range': (min(preferred_costs), max(preferred_costs)),
            'preferred_duration_range': (min(preferred_durations), max(preferred_durations)),
            'preferred_project_count_range': (min(preferred_project_counts), max(preferred_project_counts)),
            'average_preferred_cost': np.mean(preferred_costs),
            'average_preferred_duration': np.mean(preferred_durations),
            'average_preferred_project_count': np.mean(preferred_project_counts),
            'popular_projects': sorted(project_preferences.items(), key=lambda x: x[1], reverse=True)
        }

    def suggest_solution_modifications(self, solution: PortfolioSolution) -> List[str]:
        """Suggest modifications to a solution based on preference patterns"""
        patterns = self.analyze_preference_patterns()
        suggestions = []

        if not patterns:
            return ["No preference data available for suggestions"]

        # Cost-based suggestions
        avg_preferred_cost = patterns.get('average_preferred_cost', 0)
        if solution.total_cost > avg_preferred_cost * 1.2:
            suggestions.append("Consider reducing total cost - current solution is above preferred range")
        elif solution.total_cost < avg_preferred_cost * 0.8:
            suggestions.append("Could potentially increase investment - current solution is below preferred range")

        # Duration-based suggestions
        avg_preferred_duration = patterns.get('average_preferred_duration', 0)
        if solution.total_duration > avg_preferred_duration * 1.2:
            suggestions.append("Consider reducing project timeline - current duration is above preferred range")

        # Project count suggestions
        avg_preferred_count = patterns.get('average_preferred_project_count', 0)
        current_count = len(solution.selected_projects)
        if current_count < avg_preferred_count * 0.8:
            suggestions.append("Consider adding more projects to the portfolio")
        elif current_count > avg_preferred_count * 1.2:
            suggestions.append("Consider reducing the number of projects for better focus")

        # Popular project suggestions
        popular_projects = patterns.get('popular_projects', [])
        if popular_projects:
            top_projects = [p[0] for p in popular_projects[:3]]
            missing_popular = [p for p in top_projects if p not in solution.selected_projects]
            if missing_popular:
                suggestions.append(f"Consider including popular projects: {', '.join(missing_popular)}")

        return suggestions if suggestions else ["Solution appears well-aligned with preferences"]
