# Trip Planner AI Agent using CrewAI

This project is a fully-featured **AI-powered Travel Planner** built using the **CrewAI** framework. It leverages agents and tasks to collaborate and generate a comprehensive travel itinerary.

---

## 📁 Directory Structure

```
travel_agent_flow/
├── output/
│   └── final_travel_document.md        # Generated final itinerary output
│
├── src/travel_agent/
│   ├── main.py                        # Main entry point for running the flow
│   ├── tools/
│   │   ├── search_tools.py            # Search related tools for agents
│   │   ├── browser_tools.py           # Browser related tools for agents
│   │   └── calculator_tools.py        # Budget calculations, etc.
│   │
│   └── crews/travel_crew/
│       ├── config/
│       │   ├── agents.yaml            # YAML file defining all agents
│       │   └── tasks.yaml             # YAML file defining all tasks
│       │
│       └── travel_crew.py            # Crew and flow definitions
│
├── README.md                          # Documentation
├── LICENSE
├── .gitignore
├── pyproject.toml                     # Project dependencies
├── uv.lock                            # Locked dependency versions by uv
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies

```bash
uv sync
```

### 2️⃣ Run the Flow

```bash
uv run src.travel_agent.main.py
```

### 3️⃣ Output

The final travel itinerary will be saved at:

```
output/final_travel_document.md
```

---

## 🧑‍💻 How It Works

This project is built on **CrewAI**, a powerful framework for orchestrating multiple AI agents in flows.

### 🔸 Agents

Agents are defined in `agents.yaml`. Each agent has:

* **Role**: Defines what expertise the agent brings.
* **Goal**: The objective the agent focuses on.
* **Backstory**: Provides narrative context to help guide the agent's responses.

Example agent definition in YAML:

```yaml
travel_planner:
  role: "Expert Travel Consultant"
  goal: "Design optimal travel plans tailored to user preferences"
  backstory: "Has 15 years of experience planning custom trips for adventure seekers and families."
```

### 🔸 Tasks

Tasks are discrete units of work that agents execute. They are defined in `tasks.yaml` with:

* `description`: Task details (supports context variables).
* `expected_output`: Defines what output is expected.
* `agent_id`: Links the task to a specific agent.

Example task definition:

```yaml
identify_best_city:
  description: "Select the best city to visit from: {cities}"
  expected_output: "### Chosen City: ..."
  agent_id: "travel_planner"
```

### 🔸 Crews

A Crew is a collection of agents working together to complete one or more tasks sequentially or in parallel.

* Defined dynamically in `travel_crew.py`.
* Responsible for building agents from YAML and executing workflows.

### 🔸 Flows

Flows define how tasks are executed **sequentially** with dependencies on previous tasks’ results.

Example sequence:

```
identify_best_city → gather_city_insights → create_itinerary → analyze_budget → evaluate_safety → suggest_packing_list → finalize_itinerary
```

---

## 🔧 Tools

Custom tools help agents fetch real data and make smarter decisions:

* `search_tools.py` – Used for searching travel recommendations.
* `browser_tools.py` – Simulates browser activities if needed.
* `calculator_tools.py` – Helps calculate budgets, distances, etc.

---

## 📜 License

MIT License

---

## 🌍 Future Enhancements

* 🌐 Integrate real APIs (e.g., Skyscanner, Google Travel) for live data.
* 🏷️ UI layer with React for input and visualization.
* 📦 Dockerized setup for easy deployment.
* 💬 Multi-language support.

---

For questions, feel free to open issues or contribute!

Happy travels ✈️🏝️
