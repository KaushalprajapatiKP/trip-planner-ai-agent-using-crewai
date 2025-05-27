import yaml
from typing import Dict, Any, List


class Crew:
    def __init__(self, agents_path="agents.yml", tasks_path="tasks.yml", flow_path="flow.yml"):
        self.agents = self.load_yaml(agents_path).get("agents", [])
        self.tasks = self.load_yaml(tasks_path).get("tasks", [])
        self.flow = self.load_yaml(flow_path).get("flow", {})
        
        # Index agents and tasks by id for quick lookup
        self.agent_map = {agent["id"]: agent for agent in self.agents}
        self.task_map = {task["id"]: task for task in self.tasks}
        self.step_outputs: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def load_yaml(filepath: str) -> dict:
        with open(filepath, "r") as f:
            return yaml.safe_load(f)

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        return self.agent_map.get(agent_id)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        return self.task_map.get(task_id)

    def resolve_input_value(self, value: Any, trip_inputs: Dict[str, Any], step_outputs: Dict[str, Dict[str, Any]]) -> Any:
        # Resolves input values from references or returns literals as-is
        if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
            ref = value[2:-2].strip()
            parts = ref.split(".")
            if parts[0].startswith("step_"):
                step_id = parts[0]
                output_key = parts[1] if len(parts) > 1 else None
                if step_id in step_outputs and output_key:
                    return step_outputs[step_id].get(output_key)
                return None
            else:
                return trip_inputs.get(parts[0], None)
        else:
            return value

    async def execute_agent_task(self, agent_id: str, task_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        This method is a placeholder to call actual agent logic.
        Replace with real API calls or model invocation.
        For now, it returns dummy data for demo.
        """
        print(f"[Crew] Executing agent '{agent_id}' task '{task_id}' with inputs: {inputs}")

        # Dummy simulated outputs (expand or replace as needed)
        dummy_outputs = {
            "identify_best_city": {
                "chosen_city": inputs.get("cities", [None])[0],
                "city_selection_report": f"Selected {inputs.get('cities', ['unknown'])[0]}"
            },
            "gather_city_insights": {
                "local_guide": f"Info about {inputs.get('chosen_city', 'unknown city')}."
            },
            "create_itinerary": {
                "itinerary_markdown": f"Sample itinerary for {inputs.get('chosen_city')}."
            },
            "analyze_budget": {
                "budget_report": f"Budget details for {inputs.get('chosen_city')}."
            },
            "evaluate_safety": {
                "safety_report": f"Safety info for {inputs.get('chosen_city')}."
            },
            "suggest_packing_list": {
                "packing_list": f"Packing list for {inputs.get('chosen_city')}."
            },
            "finalize_itinerary": {
                "final_travel_document": f"Final itinerary document for {inputs.get('chosen_city')}."
            },
        }

        return dummy_outputs.get(task_id, {})

    async def run_flow(self, trip_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the entire workflow defined in flow.yml sequentially.
        trip_inputs: dict containing initial input parameters (origin, cities, date_range, interests, etc.)
        """
        self.step_outputs = {}
        results = {}

        for step in self.flow.get("steps", []):
            agent_id = step.get("agent")
            task_id = step.get("task_id")
            step_id = step.get("id")
            input_template = step.get("inputs", {})

            # Resolve inputs for this step from trip inputs and previous step outputs
            resolved_inputs = {}
            for key, val in input_template.items():
                resolved_inputs[key] = self.resolve_input_value(val, trip_inputs, self.step_outputs)

            # Execute the agent's task
            output = await self.execute_agent_task(agent_id, task_id, resolved_inputs)

            # Save outputs for future steps
            self.step_outputs[step_id] = output
            results[step_id] = output

        return results


# Example usage (for testing only, normally you would import Crew and call run_flow from FastAPI or other service)

if __name__ == "__main__":
    import asyncio

    crew = Crew()

    example_trip_input = {
        "origin": "New York",
        "cities": ["Lisbon", "Barcelona"],
        "date_range": "2025-06-01 to 2025-06-10",
        "interests": ["history", "beaches"]
    }

    async def main():
        results = await crew.run_flow(example_trip_input)
        print("\nWorkflow completed. Step outputs:")
        for step_id, output in results.items():
            print(f"{step_id}: {output}")

    asyncio.run(main())
