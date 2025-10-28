"""
FastAPI Extra Data Types - Advanced Python Types

This module demonstrates how to use advanced Python data types with FastAPI,
including date/time types, UUIDs, and complex type annotations. FastAPI
automatically handles serialization, validation, and documentation for these
advanced types.

Key concepts covered:
- UUID (Universally Unique Identifier) for unique identifiers
- datetime for complete date and time information
- timedelta for time duration and intervals
- time for time-of-day without date
- Annotated types with Body() for request body parameters
- Automatic type conversion and validation
- Complex calculations with date/time types

Run with: fastapi dev 10extradatatypes.py
"""

from datetime import datetime, time, timedelta
from typing import Annotated, Union
from uuid import UUID
from fastapi import Body, FastAPI

app = FastAPI(
    title="Extra Data Types Demo",
    description="A FastAPI application demonstrating advanced Python data types with automatic validation and serialization",
    version="1.0.0"
)


@app.put("/items/{item_id}")
async def set_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body(), "The start datetime"],
    end_datetime: Annotated[datetime, Body(), "The end datetime"],
    process_after: Annotated[timedelta, Body(), "Time to wait before processing"],
    repeat_at: Annotated[Union[time, None], Body(), "Optional time to repeat the process"] = None
) -> dict:
    """
    Configure item processing schedule with advanced data types.
    
    This endpoint demonstrates FastAPI's support for advanced Python data types
    including UUIDs, datetime objects, timedeltas, and time objects. It shows
    how FastAPI automatically validates, converts, and serializes these types
    while performing complex date/time calculations.
    
    Args:
        item_id (UUID): Unique identifier for the item (path parameter)
        start_datetime (datetime): When to start the item processing
        end_datetime (datetime): When to end the item processing
        process_after (timedelta): Duration to wait before starting processing
        repeat_at (Union[time, None], optional): Time of day to repeat the process
        
    Returns:
        dict: Dictionary containing all input parameters plus calculated values:
            - start_process: Calculated start time (start_datetime + process_after)
            - duration: Calculated total duration (end_datetime - start_process)
            
    Request Body Structure:
        {
            "start_datetime": "2023-12-01T10:00:00",
            "end_datetime": "2023-12-01T15:30:00", 
            "process_after": "01:30:00",
            "repeat_at": "09:00:00"
        }
        
    Response Example:
        {
            "item_id": "550e8400-e29b-41d4-a716-446655440000",
            "start_datetime": "2023-12-01T10:00:00",
            "end_datetime": "2023-12-01T15:30:00",
            "process_after": "01:30:00",
            "repeat_at": "09:00:00",
            "start_process": "2023-12-01T11:30:00",
            "duration": "04:00:00"
        }
        
    Data Type Features:
        
        UUID (item_id):
        - Path parameter with automatic UUID validation
        - Accepts standard UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        - Automatically converts string to UUID object
        - Returns 422 error for invalid UUID format
        
        datetime (start_datetime, end_datetime):
        - ISO 8601 format: "YYYY-MM-DDTHH:MM:SS" or with timezone
        - Automatic parsing from string to datetime object
        - Supports various input formats (ISO, RFC 3339, etc.)
        - Returns 422 error for invalid datetime format
        
        timedelta (process_after):
        - Duration format: "HH:MM:SS" or "D days, HH:MM:SS"
        - Can represent days, hours, minutes, seconds
        - Used for time arithmetic and calculations
        - Automatic conversion from string representation
        
        time (repeat_at):
        - Time-of-day format: "HH:MM:SS" or "HH:MM"
        - Optional field (can be null)
        - Represents time without date information
        - Used for scheduling recurring events
        
    Calculations Performed:
        - start_process = start_datetime + process_after
        - duration = end_datetime - start_process
        
    Validation Examples:
        
        Valid UUID formats:
        - "550e8400-e29b-41d4-a716-446655440000" ✓
        - "6ba7b810-9dad-11d1-80b4-00c04fd430c8" ✓
        
        Valid datetime formats:
        - "2023-12-01T10:00:00" ✓
        - "2023-12-01T10:00:00Z" ✓ (UTC)
        - "2023-12-01T10:00:00+02:00" ✓ (with timezone)
        
        Valid timedelta formats:
        - "01:30:00" ✓ (1.5 hours)
        - "2 days, 03:45:30" ✓ (2 days, 3 hours, 45 minutes, 30 seconds)
        - "120" ✓ (120 seconds)
        
        Valid time formats:
        - "09:00:00" ✓
        - "14:30" ✓
        - null ✓ (optional field)
        
    Error Cases (422 Validation Error):
        - Invalid UUID: "not-a-uuid"
        - Invalid datetime: "2023-13-01T25:00:00" (invalid month/hour)
        - Invalid timedelta: "not-a-duration"
        - Invalid time: "25:00:00" (invalid hour)
        
    Use Cases:
        - Task scheduling and automation systems
        - Event management and calendar applications
        - Workflow and process management
        - Batch processing and job scheduling
        - Recurring task configuration
        - Time-based resource allocation
        
    Advanced Features:
        - Automatic timezone handling for datetime objects
        - Precise duration calculations with timedelta
        - Time-only scheduling with time objects
        - UUID generation and validation for unique identifiers
        - JSON serialization of all complex types
        - OpenAPI documentation with proper type information
        
    Notes:
        - All datetime calculations respect timezone information
        - timedelta supports negative values for past scheduling
        - repeat_at being null means no repetition scheduled
        - UUID is automatically converted to string in JSON response
        - FastAPI handles all type conversions transparently
    """
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration
    }