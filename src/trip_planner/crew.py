from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
import yaml
from pathlib import Path
from trip_planner.tools.search_tools import SearchTools
from trip_planner.tools.browser_tools import BrowserTools
from trip_planner.tools.calculator_tools import CalculatorTools


@CrewBase
class TripPlannnerCrew():
    """Trip Planning Crew"""

    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        config_dir = base_dir / "config"
        self.agents_config = self.load_yaml(config_dir / "agents.yaml")
        self.tasks_config = self.load_yaml(config_dir / "tasks.yaml")
        self.tools_config = self.load_yaml(config_dir / "tools.yaml")
    
    # === Tool Registration ===
    @tool
    def search_tools(self):
        return SearchTools()

    @tool
    def browser_tools(self):
        return BrowserTools()

    @tool
    def calculator_tools(self):
        return CalculatorTools()

    def load_yaml(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # === Agents ===
    @agent
    def city_selection_expert(self) -> Agent:
        return Agent(config=self.agents_config["city_selection_expert"], verbose=True)

    @agent
    def local_expert(self) -> Agent:
        return Agent(config=self.agents_config["local_expert"], verbose=True)

    @agent
    def travel_concierge(self) -> Agent:
        return Agent(config=self.agents_config["travel_concierge"], verbose=True)

    @agent
    def budget_optimizer(self) -> Agent:
        return Agent(config=self.agents_config["budget_optimizer"], verbose=True)

    @agent
    def safety_advisor(self) -> Agent:
        return Agent(config=self.agents_config["safety_advisor"], verbose=True)

    @agent
    def packing_expert(self) -> Agent:
        return Agent(config=self.agents_config["packing_expert"], verbose=True)

    @agent
    def itinerary_manager(self) -> Agent:
        return Agent(config=self.agents_config["itinerary_manager"], verbose=True)

    # === Tasks ===
    @task
    def identify_best_city(self) -> Task:
        return Task(config=self.tasks_config["identify_best_city"], verbose=True)

    @task
    def gather_city_insights(self) -> Task:
        return Task(config=self.tasks_config["gather_city_insights"], verbose=True)

    @task
    def create_itinerary(self) -> Task:
        return Task(config=self.tasks_config["create_itinerary"], verbose=True)

    @task
    def analyze_budget(self) -> Task:
        return Task(config=self.tasks_config["analyze_budget"], verbose=True)

    @task
    def evaluate_safety(self) -> Task:
        return Task(config=self.tasks_config["evaluate_safety"], verbose=True)

    @task
    def suggest_packing_list(self) -> Task:
        return Task(config=self.tasks_config["suggest_packing_list"], verbose=True)

    @task
    def finalize_itinerary(self) -> Task:
        return Task(config=self.tasks_config["finalize_itinerary"], verbose=True)

    # === Crew ===
    @crew
    def crew(self) -> Crew:
        """Creates the trip planning crew"""
        return Crew(
            agents=[
                self.city_selection_expert(),
                self.local_expert(),
                self.travel_concierge(),
                self.budget_optimizer(),
                self.safety_advisor(),
                self.packing_expert(),
            ],
            tasks=[
                self.identify_best_city(),
                self.gather_city_insights(),
                self.analyze_budget(),
                self.evaluate_safety(),
                self.suggest_packing_list(),
                self.create_itinerary(),
            ],
            process=Process.hierarchical,
            verbose=True,
            manager_agent=self.itinerary_manager(),
        )


# === Runner ===

def run():
    """
    Run the trip planning crew.
    """
    inputs = {
        "origin": "Mumbai, India",
        "destination": "Krabi, Thailand",
        "start_date": "2025-06-01",
        "end_date": "2025-06-10",
        "interests": "2 adults who love swimming, dancing, hiking, shopping, local food, water sports adventures and rock climbing"
    }

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Run the crew
    result = TripPlannnerCrew().crew().kickoff(inputs=inputs)

    # Save to file
    report_path = "output/report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(result.raw)

    # Print result
    print("\n\n=== FINAL REPORT ===\n")
    print(result.raw)
    print(f"\n\nReport has been saved to {report_path}")

if __name__ == "__main__":
    run()
