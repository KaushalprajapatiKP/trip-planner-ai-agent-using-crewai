# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# from typing import List
# import os
# import yaml
# from pathlib import Path
# from trip_planner.tools.search_tools import SearchTools
# from trip_planner.tools.browser_tools import BrowserTools
# from trip_planner.tools.calculator_tools import CalculatorTools

# @CrewBase
# class TripPlannnerCrew():
#     """Trip Planning Crew"""

#     def __init__(self):
#         base_dir = Path(__file__).resolve().parent
#         config_dir = base_dir / "config"
#         self.agents_config = self.load_yaml(config_dir / "agents.yaml")
#         self.tasks_config = self.load_yaml(config_dir / "tasks.yaml")
#         self.tools_config = self.load_yaml(config_dir / "tools.yaml")
#         self.search_tool = SearchTools()
#         self.browser_tool = BrowserTools()
#         self.calculator_tool = CalculatorTools()

#     def load_yaml(self, filepath):
#         with open(filepath, "r", encoding="utf-8") as f:
#             return yaml.safe_load(f)

#     @agent
#     def city_selection_expert(self) -> Agent:
#         return Agent(
#             config=self.agents_config["city_selection_expert"],
#             tools=[self.search_tool, self.browser_tool],
#             verbose=True
#         )

#     @agent
#     def local_expert(self) -> Agent:
#         return Agent(
#             config=self.agents_config["local_expert"],
#             tools=[self.search_tool, self.browser_tool],
#             verbose=True
#         )

#     @agent
#     def travel_concierge(self) -> Agent:
#         return Agent(
#             config=self.agents_config["travel_concierge"],
#             tools=[self.browser_tool, self.calculator_tool, self.search_tool],
#             verbose=True
#         )

#     @agent
#     def budget_optimizer(self) -> Agent:
#         return Agent(
#             config=self.agents_config["budget_optimizer"],
#             tools=[self.calculator_tool, self.browser_tool],
#             verbose=True
#         )

#     @agent
#     def safety_advisor(self) -> Agent:
#         return Agent(
#             config=self.agents_config["safety_advisor"],
#             tools=[self.search_tool, self.browser_tool],
#             verbose=True
#         )

#     @agent
#     def packing_expert(self) -> Agent:
#         return Agent(
#             config=self.agents_config["packing_expert"],
#             tools=[self.browser_tool],
#             verbose=True
#         )

#     @agent
#     def itinerary_manager(self) -> Agent:
#         return Agent(
#             config=self.agents_config["itinerary_manager"],
#             verbose=True
#         )

#     @task
#     def identify_best_city(self) -> Task:
#         task_config = self.tasks_config["identify_best_city"]
#         return Task(
#             config={
#                 "description": task_config["description"],
#                 "expected_output": task_config["expected_output"],
#                 "context": [
#                     "Origin: {origin}",
#                     "Cities: {cities}",
#                     "Dates: {date_range}",
#                     "Interests: {interests}"
#                 ],
#             },
#             agent=self.city_selection_expert,
#             verbose=True
#         )

#     @task
#     def gather_city_insights(self) -> Task:
#         task_config = self.tasks_config["gather_city_insights"]
#         return Task(
#             config={
#                 "description": task_config["description"],
#                 "expected_output": task_config["expected_output"],
#                 "context": ["Selected city: {destination}"]
#             },
#             agent=self.local_expert,
#             verbose=True
#         )

#     @task
#     def create_itinerary(self) -> Task:
#         task_config = self.tasks_config["create_itinerary"]
#         return Task(
#             config={
#                 "description": task_config["description"],
#                 "expected_output": task_config["expected_output"],
#                 "context": [
#                     "Travel dates: {date_range}",
#                     "Interests: {interests}"
#                 ]
#             },
#             agent=self.travel_concierge,
#             verbose=True
#         )

#     @task
#     def analyze_budget(self) -> Task:
#         task_config = self.tasks_config["analyze_budget"]
#         return Task(
#             config={
#                 "description": task_config["description"],
#                 "expected_output": task_config["expected_output"],
#                 "context": [
#                     "Origin: {origin}",
#                     "Dates: {date_range}",
#                     "Interests: {interests}"
#                 ]
#             },
#             agent=self.budget_optimizer,
#             verbose=True
#         )

#     @task
#     def evaluate_safety(self) -> Task:
#         task_config = self.tasks_config["evaluate_safety"]
#         return Task(
#             config={
#                 "description": task_config["description"],
#                 "expected_output": task_config["expected_output"],
#                 "context": [
#                     "City: {destination}",
#                     "Dates: {date_range}"
#                 ]
#             },
#             agent=self.safety_advisor,
#             verbose=True
#         )

#     @task
#     def suggest_packing_list(self) -> Task:
#         task_config = self.tasks_config["suggest_packing_list"]
#         return Task(
#             config={
#                 "description": task_config["description"],
#                 "expected_output": task_config["expected_output"],
#                 "context": [
#                     "Destination: {destination}",
#                     "Dates: {date_range}"
#                 ]
#             },
#             agent=self.packing_expert,
#             verbose=True
#         )

#     @task
#     def finalize_itinerary(self) -> Task:
#         task_config = self.tasks_config["finalize_itinerary"]
#         return Task(
#             config={
#                 "description": task_config["description"],
#                 "expected_output": task_config["expected_output"],
#                 "context": [
#                     "Final City: {destination}",
#                     "Trip Date: {date_range}"
#                 ]
#             },
#             agent=self.itinerary_manager,
#             verbose=True
#         )


#     @crew
#     def crew(self) -> Crew:
#         """Creates the trip planning crew"""
#         return Crew(
#             agents=[
#                 self.city_selection_expert,
#                 self.local_expert,
#                 self.travel_concierge,
#                 self.budget_optimizer,
#                 self.safety_advisor,
#                 self.packing_expert,
#                 self.itinerary_manager
#             ],
#             tasks=[
#                 self.identify_best_city,
#                 self.gather_city_insights,
#                 self.create_itinerary,
#                 self.analyze_budget,
#                 self.evaluate_safety,
#                 self.suggest_packing_list,
#                 self.finalize_itinerary
#             ],
#             process=Process.sequential,
#             verbose=True,
#         )

# def run():
#     """Run the trip planning crew"""
#     inputs = {
#         "origin": "Mumbai, India",
#         "cities": ["Krabi", "Phuket", "Koh Samui"],
#         "date_range": "2025-06-01 to 2025-06-10",
#         "interests": "2 adults who love swimming, dancing, hiking, shopping, local food, water sports adventures and rock climbing",
#         "destination": "Krabi, Thailand"
#     }

#     os.makedirs("output", exist_ok=True)
    
#     try:
#         result = TripPlannnerCrew().crew().kickoff(inputs=inputs)
#         report_path = "output/report.md"
#         with open(report_path, "w", encoding="utf-8") as f:
#             f.write(result.raw)
#         print("\n=== FINAL REPORT ===\n")
#         print(result.raw)
#     except KeyboardInterrupt:
#         print("\nOperation cancelled by user")

# if __name__ == "__main__":
#     run()

# src/travel_crew/crew.py
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from trip_planner.tools.search_tools import SearchTools
from trip_planner.tools.browser_tools import BrowserTools
from trip_planner.tools.calculator_tools import CalculatorTools
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class TravelCrew():
    """Travel planning crew for generating full trip plans"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Initialize shared tools
    search = SearchTools()
    browser = BrowserTools()
    calculator = CalculatorTools()

    @agent
    def city_selection_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selection_expert'],
            verbose=True,
            tools=[self.search, self.browser]
        )

    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'],
            verbose=True,
            tools=[self.search, self.browser]
        )

    @agent
    def travel_concierge(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_concierge'],
            verbose=True,
            tools=[self.search, self.browser]
        )

    @agent
    def budget_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_optimizer'],
            verbose=True,
            tools=[self.search, self.browser, self.calculator]
        )

    @agent
    def safety_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['safety_advisor'],
            verbose=True,
            tools=[self.search, self.browser]
        )

    @agent
    def packing_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['packing_expert'],
            verbose=True,
            tools=[self.search]
        )

    @agent
    def itinerary_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_manager'],
            verbose=True
            # No tools – aggregates results
        )
    @task
    def identify_best_city(self) -> Task:
        return Task(
            config=self.tasks_config['identify_best_city'],
            agent=self.city_selection_expert()
        )

    @task
    def gather_city_insights(self) -> Task:
        return Task(
            config=self.tasks_config['gather_city_insights'],
            agent=self.local_expert()
        )

    @task
    def create_itinerary(self) -> Task:
        return Task(
            config=self.tasks_config['create_itinerary'],
            agent=self.travel_concierge()
        )

    @task
    def analyze_budget(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_budget'],
            agent=self.budget_optimizer()
        )

    @task
    def evaluate_safety(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_safety'],
            agent=self.safety_advisor()
        )

    @task
    def suggest_packing_list(self) -> Task:
        return Task(
            config=self.tasks_config['suggest_packing_list'],
            agent=self.packing_expert()
        )

    @task
    def finalize_itinerary(self) -> Task:
        return Task(
            config=self.tasks_config['finalize_itinerary'],
            agent=self.itinerary_manager(),
            output_file='output/final_itinerary.md'
        )


    @crew
    def crew(self) -> Crew:
        """Creates the full travel planning crew"""
        return Crew(
            agents=[
                self.city_selection_expert(),
                self.local_expert(),
                self.travel_concierge(),
                self.budget_optimizer(),
                self.safety_advisor(),
                self.packing_expert(),
                self.itinerary_manager(),
            ],
            tasks=[
                self.identify_best_city(),
                self.gather_city_insights(),
                self.create_itinerary(),
                self.analyze_budget(),
                self.evaluate_safety(),
                self.suggest_packing_list(),
                self.finalize_itinerary(),
            ],
            process=Process.sequential,
            verbose=True,
        )

    
import yaml
from pathlib import Path
def run():
    """Run the travel planning crew with dynamic user input"""
    # Sample input (you can replace with input() or function args)
    user_input = {
        'origin': 'New York',
        'date_range': '2025-08-10 to 2025-08-20',
        'cities': 'Tokyo, Barcelona, Cape Town',
        'interests': 'food, art, architecture',
        'destination': 'Barcelona'
    }
    travel_crew = TravelCrew()
    base_dir = Path(__file__).resolve().parent
    config_dir = base_dir/"config"
    # Load agent config
    with open(f'{config_dir}/agents.yaml', 'r') as f:
        agent_configs = yaml.safe_load(f)

    # Load and fill task config
    with open(f'{config_dir}/tasks.yaml', 'r') as f:
        raw_tasks_config = yaml.safe_load(f)

    # Replace placeholders in task config
    tasks_config = {}
    for key, task in raw_tasks_config.items():
        tasks_config[key] = {
            k: (v.format(**user_input) if isinstance(v, str) else v)
            for k, v in task.items()
        }
    result = TravelCrew().crew().kickoff(inputs=user_input)

    print("✅ Final travel itinerary saved to: output/final_itinerary.md")
    return result


if __name__ == "__main__":
    run()


