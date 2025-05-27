from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    operation: str = Field(
        ...,
        description="The mathematical operation to perform. Supported operations: add, subtract, multiply, divide, etc.",
    )

class CalculatorTools(BaseTool):
    name: str = "Calculator"
    description: str = """Useful to perform any mathematical calculations, 
    like sum, minus, multiplication, division, etc.
    The input should be a mathematical expression, e.g. '200*7' or '5000/2*10'"""
    args_schema: type[BaseModel] = CalculatorInput

    def _run(self, operation: str) -> str:
        return eval(operation)
    
    async def _arun(self, operation: str) -> str:
        raise NotImplementedError("CalculatorTools does not support async execution yet.")