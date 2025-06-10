# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# from crewai.agents.agent_builder.base_agent import BaseAgent
# from typing import List

# # If you want to run a snippet of code before or after the crew starts,
# # you can use the @before_kickoff and @after_kickoff decorators
# # https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


# @CrewBase
# class PoemCrew:
#     """Poem Crew"""

#     agents: List[BaseAgent]
#     tasks: List[Task]

#     # Learn more about YAML configuration files here:
#     # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
#     # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
#     agents_config = "config/agents.yaml"
#     tasks_config = "config/tasks.yaml"

#     # If you would lik to add tools to your crew, you can learn more about it here:
#     # https://docs.crewai.com/concepts/agents#agent-tools
#     @agent
#     def poem_writer(self) -> Agent:
#         return Agent(
#             config=self.agents_config["poem_writer"],  # type: ignore[index]
#         )

#     # To learn more about structured task outputs,
#     # task dependencies, and task callbacks, check out the documentation:
#     # https://docs.crewai.com/concepts/tasks#overview-of-a-task
#     @task
#     def write_poem(self) -> Task:
#         return Task(
#             config=self.tasks_config["write_poem"],  # type: ignore[index]
#         )

#     @crew
#     def crew(self) -> Crew:
#         """Creates the Research Crew"""
#         # To learn how to add knowledge sources to your crew, check out the documentation:
#         # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

#         return Crew(
#             agents=self.agents,  # Automatically created by the @agent decorator
#             tasks=self.tasks,  # Automatically created by the @task decorator
#             process=Process.sequential,
#             verbose=True,
#         )



from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from trip_planner.tools.search_tools import SearchTools
from trip_planner.tools.browser_tools import BrowserTools
from trip_planner.tools.calculator_tools import CalculatorTools
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from litellm import Router
from crewai import Agent, LLM
import yaml
base_dir = Path(__file__).resolve().parent
config_dir = base_dir/"config"


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
            tools=[self.search, self.browser],
            llm=LLM(model="gemini/gemini-2.0-flash")
        )

    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'],
            verbose=True,
            tools=[self.search, self.browser],
            llm=LLM(model="gemini/gemini-2.0-flash")
        )

    @agent
    def travel_concierge(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_concierge'],
            verbose=True,
            tools=[self.search, self.browser],
            llm=LLM(model="gemini/gemini-2.0-flash")
        )

    @agent
    def budget_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_optimizer'],
            verbose=True,
            tools=[self.search, self.browser, self.calculator],
            llm=LLM(model="gemini/gemini-2.0-flash")
        )

    @agent
    def safety_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['safety_advisor'],
            verbose=True,
            tools=[self.search, self.browser],
            llm=LLM(model="gemini/gemini-2.0-flash")
        )

    @agent
    def packing_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['packing_expert'],
            verbose=True,
            tools=[self.search],
            llm=LLM(model="gemini/gemini-2.0-flash")
        )

    @agent
    def itinerary_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_manager'],
            verbose=True,
            llm=LLM(model="gemini/gemini-2.0-flash")
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


    # @crew
    # def crew(self) -> Crew:
    #     """Creates the full travel planning crew"""
    #     return Crew(
    #         agents=[
    #             self.city_selection_expert(),
    #             self.local_expert(),
    #             self.travel_concierge(),
    #             self.budget_optimizer(),
    #             self.safety_advisor(),
    #             self.packing_expert(),
    #             self.itinerary_manager(),
    #         ],
    #         tasks=[
    #             self.identify_best_city(),
    #             self.gather_city_insights(),
    #             self.create_itinerary(),
    #             self.analyze_budget(),
    #             self.evaluate_safety(),
    #             self.suggest_packing_list(),
    #             self.finalize_itinerary(),
    #         ],
    #         process=Process.sequential,
    #         verbose=True,
    #     )

    # Updated Crew Setup in crew.py
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
                self.create_itinerary(),
                self.analyze_budget(),
                self.evaluate_safety(),
                self.suggest_packing_list(),
                self.finalize_itinerary()
            ],
            process=Process.hierarchical,  
            verbose=True,
            manager_agent=self.itinerary_manager(),  # Set as manager
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


# if __name__ == "__main__":
#     run()


