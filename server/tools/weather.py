"""
Weather forecasting tools for TradeArena agents
"""

import random
import asyncio
from datetime import datetime, timedelta
from strands import tool

@tool(
    name="get_weather",
    description="Retrieves weather forecast for a specified location",
    inputSchema={
        "json": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get weather for"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days for the forecast (1-7)",
                    "minimum": 1,
                    "maximum": 7,
                    "default": 3
                }
            },
            "required": ["city"]
        }
    }
)
async def weather_forecast(city: str, days: int = 3) -> str:
    """Mock weather forecast implementation.
    
    Args:
        city: The name of the city
        days: Number of days for the forecast (1-7)
    
    Returns:
        Weather forecast string with mock data
    """
    # Simulate async API call delay
    await asyncio.sleep(0.5)  # Simulated network delay
    
    # Mock weather conditions
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Thunderstorms", "Clear", "Overcast"]
    temperatures = range(15, 35)  # Temperature range in Celsius
    
    forecast_lines = [f"Weather forecast for {city} for the next {days} days:"]
    
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        condition = random.choice(conditions)
        temp_high = random.choice(temperatures)
        temp_low = temp_high - random.randint(5, 10)
        humidity = random.randint(40, 90)
        wind_speed = random.randint(5, 25)
        
        if i == 0:
            day_label = "Today"
        elif i == 1:
            day_label = "Tomorrow"
        else:
            day_label = date.strftime("%A, %B %d")
        
        forecast_lines.append(
            f"{day_label}: {condition}, High: {temp_high}°C, Low: {temp_low}°C, "
            f"Humidity: {humidity}%, Wind: {wind_speed} km/h"
        )
    
    # Add a summary
    avg_temp = sum(random.choice(temperatures) for _ in range(days)) / days
    forecast_lines.append(f"\nSummary: Average temperature expected to be around {avg_temp:.1f}°C")
    forecast_lines.append("Note: This is mock weather data for demonstration purposes")
    
    return "\n".join(forecast_lines)
