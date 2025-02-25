import pint # this module is used for unit conversion
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from typing import Dict, Any

class UnitConversionInput(BaseModel):
    value: float = Field(description="Numeric value to convert.")
    from_unit: str = Field(description="Unit to convert from (e.g., meters, kilograms, USD).")
    to_unit: str = Field(description="Unit to convert to (e.g., feet, pounds, EUR).")

class UnitConversionTool(BaseTool):
    name: str = "unit_conversion_tool"
    description: str = "Converts values between different measurement units."
    
    def __init__(self):
        super().__init__()
        object.__setattr__(self, "ureg", pint.UnitRegistry())
    
    def _convert_unit(self, value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        """Converts a value from one unit to another."""
        try:
            converted_value = (self.ureg.Quantity(value, from_unit)).to(to_unit).magnitude
            return {
                "original_value": value,
                "from_unit": from_unit,
                "to_unit": to_unit,
                "converted_value": converted_value
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _run(self, value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        return self._convert_unit(value, from_unit, to_unit)
    
    async def _arun(self, value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
        return self._convert_unit(value, from_unit, to_unit)


# unit_coversion_tool = UnitConversionTool()
# print(unit_coversion_tool._run(value=100, from_unit="meters", to_unit="feet"))