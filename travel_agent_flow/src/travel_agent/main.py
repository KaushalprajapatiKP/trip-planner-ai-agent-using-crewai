from crewai import Crew, Process, Agent, Task
from crewai.flow import Flow, start, listen
from pydantic import BaseModel
import os
import yaml
import asyncio

# File paths to your YAML files
AGENTS_FILE = "/Users/kaushalprajapati/Desktop/Development/trip-planner-ai-agent-using-crewai/travel_agent_flow/src/travel_agent/crews/travel_crew/config/agents.yaml"
TASKS_FILE = "/Users/kaushalprajapati/Desktop/Development/trip-planner-ai-agent-using-crewai/travel_agent_flow/src/travel_agent/crews/travel_crew/config/tasks.yaml"

class TripState(BaseModel):
    origin: str = ""
    cities: list = []
    date_range: str = ""
    interests: str = ""
    destination: str = ""
    city_insights: str = ""
    itinerary: str = ""
    budget: str = ""
    safety: str = ""
    packing_list: str = ""
    final_document: str = ""

class TripPlannerFlow(Flow[TripState]):
    def __init__(self):
        super().__init__()
        self.agents_data = self.load_yaml(AGENTS_FILE)
        self.tasks_data = self.load_yaml(TASKS_FILE)

    def load_yaml(self, filename):
        with open(filename, "r") as f:
            return yaml.safe_load(f)

    def build_crew(self, task_ids, context):
        agents = {}
        tasks = []

        # Build Agent objects
        for agent_id, data in self.agents_data.items():
            agents[agent_id] = Agent(
                role=data['role'],
                goal=data['goal'],
                backstory=data['backstory'],
                verbose=True
            )

        # Build Task objects
        for task_id in task_ids:
            task_data = self.tasks_data[task_id]
            task = Task(
                description=task_data["description"].format(**context),
                expected_output=task_data["expected_output"],
                agent=agents[task_data["agent_id"]],
                verbose=True
            )
            tasks.append(task)

        return Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

    @start()
    async def identify_best_city(self):
        context = {
            "origin": self.state.origin,
            "cities": ", ".join(self.state.cities),
            "date_range": self.state.date_range,
            "interests": self.state.interests,
        }
        crew = self.build_crew(task_ids=["identify_best_city"], context=context)
        result = await crew.kickoff_async()
        print("----------------------------------------")
        print("Identify Best City Result:")
        print(result)
        print("----------------------------------------")

        self.state.destination = result
        if not self.state.destination:
            raise ValueError("identify_best_city did not produce a destination.")
        return self.state.destination

    @listen(identify_best_city)
    async def gather_city_insights(self):
        context = {
            "origin": self.state.origin,
            "date_range": self.state.date_range,
            "interests": self.state.interests,
            "destination": self.state.destination,
        }
        crew = self.build_crew(task_ids=["gather_city_insights"], context=context)
        result = await crew.kickoff_async()
        print("----------------------------------------")
        print("City Insights Result:")
        print(result)
        print("----------------------------------------")
        self.state.city_insights = result
        return self.state.city_insights

    @listen(gather_city_insights)
    async def create_itinerary(self):
        context = {
            "origin": self.state.origin,
            "date_range": self.state.date_range,
            "interests": self.state.interests,
            "destination": self.state.destination,
        }
        crew = self.build_crew(task_ids=["create_itinerary"], context=context)
        result = await crew.kickoff_async()
        print("----------------------------------------")
        print("Itinerary Result:")
        print(result)
        print("----------------------------------------")
        self.state.itinerary = result
        return self.state.itinerary

    @listen(create_itinerary)
    async def analyze_budget(self):
        context = {
            "origin": self.state.origin,
            "date_range": self.state.date_range,
            "interests": self.state.interests,
            "destination": self.state.destination,
        }
        crew = self.build_crew(task_ids=["analyze_budget"], context=context)
        result = await crew.kickoff_async()
        print("----------------------------------------")
        print("Budget Analysis Result:")
        print(result)
        print("----------------------------------------")
        self.state.budget = result
        return self.state.budget

    @listen(analyze_budget)
    async def evaluate_safety(self):
        context = {
            "origin": self.state.origin,
            "date_range": self.state.date_range,
            "destination": self.state.destination,
        }
        crew = self.build_crew(task_ids=["evaluate_safety"], context=context)
        result = await crew.kickoff_async()
        print("----------------------------------------")
        print("Safety Evaluation Result:")
        print(result)
        print("----------------------------------------")
        self.state.safety = result
        return self.state.safety

    @listen(evaluate_safety)
    async def suggest_packing_list(self):
        context = {
            "date_range": self.state.date_range,
            "destination": self.state.destination,
        }
        crew = self.build_crew(task_ids=["suggest_packing_list"], context=context)
        result = await crew.kickoff_async()
        print("----------------------------------------")
        print("Packing List Result:")
        print(result)
        print("----------------------------------------")
        self.state.packing_list = result
        return self.state.packing_list
    

    @listen(suggest_packing_list)
    async def finalize_itinerary(self):
        context = {
            "date_range": self.state.date_range,
            "destination": self.state.destination,
        }
        crew = self.build_crew(task_ids=["finalize_itinerary"], context=context)
        result = await crew.kickoff_async()

        # ✅ Access the result correctly
        try:
            final_doc = getattr(result, "finalize_itinerary", "").strip()
            self.state.final_document = final_doc
        except AttributeError:
            self.state.final_document = ""
            print("Error: finalize_itinerary not found in CrewOutput")

        os.makedirs("output", exist_ok=True)
        with open("output/final_travel_document.md", "w") as f:
            f.write(self.state.final_document)

        return "Final itinerary document created!"


async def async_run_flow(inputs):
    flow = TripPlannerFlow()
    flow.state.origin = inputs["origin"]
    flow.state.cities = inputs["cities"]
    flow.state.date_range = inputs["date_range"]
    flow.state.interests = inputs["interests"]
    await flow.kickoff_async()
    return flow.state

async def plot():
    """Generate a visualization of the flow"""
    flow = TripPlannerFlow()
    flow.plot("trip_planner_flow")
    print("Flow visualization saved to trip_planner_flow.html")

if __name__ == "__main__":
    inputs = {
        "origin": "Mumbai, India",
        "cities": ["Krabi", "Phuket", "Koh Samui"],
        "date_range": "2025-06-01 to 2025-06-10",
        "interests": "2 adults who love swimming, dancing, hiking, shopping, local food, water sports adventures and rock climbing",
    }
    
    try:
        final_state = asyncio.run(async_run_flow(inputs))
        plot()
        print("\n=== FLOW COMPLETE ===")
        print("Final document saved at output/final_travel_document.md\n")

    except Exception as e:
        print(f"Flow failed: {str(e)}")
