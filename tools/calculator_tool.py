import math
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any

class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression to evaluate (e.g., '2 + 2', 'sin(45)').")

class CalculatorTool(BaseTool):
    name: str = "calculator_tool"
    description: str = "Evaluates basic mathematical expressions securely."
    
    def _evaluate_expression(self, expression: str) -> Dict[str, Any]:
        """Safely evaluates a mathematical expression."""
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        
        try:
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return {"expression": expression, "result": result}
        except Exception as e:
            return {"error": str(e)}
    
    def _run(self, expression: str) -> Dict[str, Any]:
        return self._evaluate_expression(expression)
    
    async def _arun(self, expression: str) -> Dict[str, Any]:
        return self._evaluate_expression(expression)


# calculator_tool = CalculatorTool()
# print(calculator_tool._run(expression="log2(28)"))