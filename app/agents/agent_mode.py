"""
Agent Mode - Looping decision-maker for Avatar AI Agent

This transforms Avatar from a simple command-response system into a true AI agent
that can plan, execute, observe, and decide on multi-step tasks.

Agent Loop: Think -> Plan -> Act -> Observe -> Think -> ... -> Complete
"""

from app.brain.llm import LLMInterface
from app.actions.open_apps import OpenAppsAction
from app.actions.search_web import SearchWebAction
from app.actions.search_summary import SearchSummaryAction
from app.actions.system_control import SystemControlAction
from app.memory.memory_manager import MemoryManager
from typing import Dict, Any, List
import json
from datetime import datetime

class AgentMode:
    """
    Advanced AI Agent that can handle complex multi-step tasks
    through iterative planning and execution
    """
    
    def __init__(self):
        self.llm = LLMInterface()
        self.memory = MemoryManager()
        
        # Available tools
        self.tools = {
            "open_apps": OpenAppsAction(),
            "search_web": SearchWebAction(),
            "search_summary": SearchSummaryAction(),
            "system_control": SystemControlAction()
        }
        
        # Agent state
        self.reset_state()
    
    def reset_state(self):
        """Reset agent state for new task"""
        self.state = {
            "task": "",
            "plan": [],
            "current_step": 0,
            "observations": [],
            "completed_steps": [],
            "final_result": "",
            "is_complete": False,
            "max_iterations": 10,
            "current_iteration": 0
        }
    
    async def execute_task(self, task: str) -> Dict[str, Any]:
        """
        Execute a complex task using agent mode
        """
        self.reset_state()
        self.state["task"] = task
        
        try:
            # Step 1: Think & Plan
            plan = await self._create_plan(task)
            self.state["plan"] = plan
            
            # Step 2: Execute loop (Act -> Observe -> Think)
            while not self.state["is_complete"] and self.state["current_iteration"] < self.state["max_iterations"]:
                await self._execute_next_step()
                self.state["current_iteration"] += 1
            
            # Step 3: Generate final answer
            if self.state["is_complete"]:
                final_result = await self._generate_final_answer()
                self.state["final_result"] = final_result
            else:
                self.state["final_result"] = "Task incomplete - reached maximum iterations"
            
            # Store in memory
            self.memory.store_agent_task(self.state)
            
            return self._format_response()
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "state": self.state
            }
    
    async def _create_plan(self, task: str) -> List[Dict[str, Any]]:
        """
        Think Phase: Create a plan using LLM
        """
        system_prompt = """
        You are Avatar AI Agent in intelligent planning mode. Think first, then act.
        
        CRITICAL RULES:
        1. For "find", "research", "compare", "best", "top" queries - USE search_summary
        2. search_summary returns analyzed data WITHOUT opening browser
        3. search_web opens browser - ONLY use when user explicitly asks to open/browse
        4. Think about what the user REALLY wants - information or action?
        
        Available tools:
        - search_summary: Intelligent search with analysis (parameters: query, engine, max_results)
        - search_web: Open browser with search (parameters: query, engine)
        - open_apps: Open applications/websites (parameters: app_name, url)
        - system_control: Control system functions (parameters: command)
        
        Examples of INTELLIGENT planning:
        
        Task: "Find best Python course and compare it"
        Steps:
        1. Use search_summary to find and analyze Python courses
        2. Provide comparison and recommendations
        
        Task: "Research and compare 3 Python courses"
        Steps:
        1. Use search_summary to research Python courses
        2. Analyze and compare the results
        
        Task: "Open python.org"
        Steps:
        1. Use open_apps to open python.org
        
        Task: "Search for python tutorials and browse results"
        Steps:
        1. Use search_web to open browser with python tutorials
        
        Return a JSON array of steps. Each step should have:
        {
            "step_number": 1,
            "description": "What this step accomplishes",
            "tool": "tool_name",
            "parameters": {"key": "value"},
            "expected_outcome": "What we expect to achieve"
        }
        
        Think intelligently - prioritize information gathering over browser opening!
        Maximum 5 steps.
        """
        
        try:
            full_prompt = f"{system_prompt}\n\nTask: {task}"
            response = self.llm.model.generate_content(full_prompt)
            plan_data = json.loads(response.text.strip())
            
            # Ensure it's a list
            if isinstance(plan_data, dict) and "steps" in plan_data:
                plan_data = plan_data["steps"]
            elif not isinstance(plan_data, list):
                # Fallback: create simple plan
                plan_data = [{"step_number": 1, "description": task, "tool": "search_web", "parameters": {"query": task}, "expected_outcome": "Get results"}]
            
            return plan_data
            
        except Exception as e:
            # Enhanced fallback plan - create multi-step based on task complexity
            return self._create_fallback_plan(task)
    
    def _create_fallback_plan(self, task: str) -> List[Dict[str, Any]]:
        """
        Create a multi-step plan based on task complexity when LLM planning fails
        """
        task_lower = task.lower()
        
        # Complex task patterns - prioritize intelligent analysis
        if "and" in task_lower or "then" in task_lower or "compare" in task_lower or "best" in task_lower or "top" in task_lower:
            if "python course" in task_lower and ("compare" in task_lower or "research" in task_lower or "best" in task_lower):
                return [
                    {
                        "step_number": 1,
                        "description": "Intelligently search and analyze Python courses",
                        "tool": "search_summary",
                        "parameters": {"query": "best Python courses comparison 2024", "max_results": 5},
                        "expected_outcome": "Get analyzed comparison of Python courses"
                    },
                    {
                        "step_number": 2,
                        "description": "Search for Python course reviews and ratings",
                        "tool": "search_summary",
                        "parameters": {"query": "Python course reviews ratings", "max_results": 3},
                        "expected_outcome": "Get review analysis"
                    }
                ]
            elif "find" in task_lower and ("compare" in task_lower or "best" in task_lower or "top" in task_lower):
                return [
                    {
                        "step_number": 1,
                        "description": f"Intelligently search and analyze: {task}",
                        "tool": "search_summary",
                        "parameters": {"query": task, "max_results": 5},
                        "expected_outcome": "Get analyzed results and comparison"
                    }
                ]
            elif "find" in task_lower and "open" in task_lower:
                return [
                    {
                        "step_number": 1,
                        "description": f"Search for: {task}",
                        "tool": "search_summary",
                        "parameters": {"query": task, "max_results": 3},
                        "expected_outcome": "Get search results analysis"
                    },
                    {
                        "step_number": 2,
                        "description": "Open top result in browser",
                        "tool": "open_apps",
                        "parameters": {"url": "https://www.google.com"},
                        "expected_outcome": "Open found result"
                    }
                ]
        
        # Default single step
        return [{
            "step_number": 1,
            "description": f"Search for: {task}",
            "tool": "search_web",
            "parameters": {"query": task},
            "expected_outcome": "Get search results"
        }]
    
    async def _execute_next_step(self):
        """
        Act Phase: Execute the next planned step
        """
        if self.state["current_step"] >= len(self.state["plan"]):
            await self._check_completion()
            return
        
        current_step_data = self.state["plan"][self.state["current_step"]]
        step_number = current_step_data["step_number"]
        description = current_step_data["description"]
        tool_name = current_step_data["tool"]
        parameters = current_step_data.get("parameters", {})
        
        try:
            # Execute the tool
            if tool_name in self.tools:
                result = await self.tools[tool_name].execute(parameters)
                
                # Store observation
                observation = {
                    "step_number": step_number,
                    "description": description,
                    "tool": tool_name,
                    "parameters": parameters,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.state["observations"].append(observation)
                self.state["completed_steps"].append(step_number)
                
                # Move to next step
                self.state["current_step"] += 1
                
            else:
                raise Exception(f"Unknown tool: {tool_name}")
                
        except Exception as e:
            # Store error observation
            observation = {
                "step_number": step_number,
                "description": description,
                "tool": tool_name,
                "parameters": parameters,
                "result": f"Error: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "error": True
            }
            
            self.state["observations"].append(observation)
            self.state["current_step"] += 1
    
    async def _check_completion(self):
        """
        Think Phase: Decide if task is complete based on observations
        """
        if not self.state["observations"]:
            self.state["is_complete"] = False
            return
        
        system_prompt = """
        You are Avatar AI Agent analyzing task completion.
        
        Original task: {task}
        Completed steps: {completed_steps}
        Observations: {observations}
        
        Analyze if the task is complete. Consider:
        1. Have we achieved the main goal?
        2. Are there any remaining steps needed?
        3. Should we continue with more actions?
        
        Return JSON with:
        {{
            "is_complete": true/false,
            "reasoning": "Why the task is or isn't complete",
            "next_action_suggestion": "What to do next (if not complete)"
        }}
        """.format(
            task=self.state["task"],
            completed_steps=len(self.state["completed_steps"]),
            observations=json.dumps(self.state["observations"][-3:], indent=2)  # Last 3 observations
        )
        
        try:
            response = self.llm.model.generate_content(system_prompt)
            completion_data = json.loads(response.text.strip())
            
            self.state["is_complete"] = completion_data.get("is_complete", True)
            
        except Exception as e:
            # Default to complete if we can't decide
            self.state["is_complete"] = True
    
    async def _generate_final_answer(self) -> str:
        """
        Generate final summary and answer
        """
        system_prompt = """
        You are Avatar AI Agent providing a final summary.
        
        Task: {task}
        Steps completed: {completed_steps}
        Observations: {observations}
        
        Provide a comprehensive summary of what was accomplished and the final result.
        Be helpful and specific about what was achieved.
        """.format(
            task=self.state["task"],
            completed_steps=len(self.state["completed_steps"]),
            observations=json.dumps(self.state["observations"], indent=2)
        )
        
        try:
            response = self.llm.model.generate_content(system_prompt)
            return response.text.strip()
        except Exception as e:
            return f"Task completed with {len(self.state['completed_steps'])} steps. Final result: {self.state['observations'][-1]['result'] if self.state['observations'] else 'No results'}"
    
    def _format_response(self) -> Dict[str, Any]:
        """
        Format the agent response for API
        """
        return {
            "success": True,
            "task": self.state["task"],
            "agent_mode": True,
            "plan": self.state["plan"],
            "completed_steps": self.state["completed_steps"],
            "observations": self.state["observations"],
            "final_result": self.state["final_result"],
            "is_complete": self.state["is_complete"],
            "iterations_used": self.state["current_iteration"],
            "summary": {
                "total_steps": len(self.state["plan"]),
                "steps_completed": len(self.state["completed_steps"]),
                "success_rate": len(self.state["completed_steps"]) / len(self.state["plan"]) if self.state["plan"] else 0
            }
        }
