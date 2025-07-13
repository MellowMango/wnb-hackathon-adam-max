"""
Weave Trace Hooks

This module provides automatic instrumentation for CrewAI agents and flows.
"""

import os
import weave
from typing import Any, Callable, Dict, Optional
from functools import wraps
from datetime import datetime


def traced(component: str = None, operation: str = None):
    """
    Decorator to automatically trace function calls with Weave.
    
    Args:
        component: Component name (e.g., "research_crew", "youtube_agent")
        operation: Operation name (e.g., "analyze_content", "plan_route")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract component and operation names
            comp_name = component or getattr(func, '__name__', 'unknown')
            op_name = operation or func.__name__
            
            # Create trace name
            trace_name = f"{comp_name}.{op_name}"
            
            # Start trace
            with weave.trace(name=trace_name) as trace:
                # Add metadata
                trace.add_tag("component", comp_name)
                trace.add_tag("operation", op_name)
                trace.add_tag("timestamp", datetime.now().isoformat())
                
                # Add input parameters (sanitized)
                sanitized_kwargs = _sanitize_trace_data(kwargs)
                trace.log_input(sanitized_kwargs)
                
                try:
                    # Execute function
                    result = func(*args, **kwargs)
                    
                    # Log output (sanitized)
                    sanitized_result = _sanitize_trace_data(result)
                    trace.log_output(sanitized_result)
                    
                    return result
                    
                except Exception as e:
                    # Log error
                    trace.log_error(str(e))
                    trace.add_tag("status", "error")
                    raise
                else:
                    trace.add_tag("status", "success")
        
        return wrapper
    return decorator


def _sanitize_trace_data(data: Any) -> Any:
    """
    Sanitize data for tracing by removing sensitive information.
    
    Args:
        data: Data to sanitize
        
    Returns:
        Sanitized data safe for tracing
    """
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Skip sensitive keys
            if any(sensitive in key.lower() for sensitive in ['password', 'token', 'key', 'secret']):
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = _sanitize_trace_data(value)
        return sanitized
    
    elif isinstance(data, list):
        return [_sanitize_trace_data(item) for item in data[:10]]  # Limit list size
    
    elif isinstance(data, str):
        # Truncate very long strings
        return data[:1000] + "..." if len(data) > 1000 else data
    
    else:
        return data


class WeaveTraceManager:
    """
    Manages Weave tracing for the entire application.
    """
    
    def __init__(self, project_name: str = "crewai-mcp-pipeline"):
        self.project_name = project_name
        self.initialized = False
        
    def initialize(self, api_key: str = None):
        """
        Initialize Weave tracing.
        
        Args:
            api_key: W&B API key (optional if set in environment)
        """
        if self.initialized:
            return
        
        # Set API key if provided
        if api_key:
            os.environ["WANDB_API_KEY"] = api_key
        
        # Initialize Weave
        weave.init(self.project_name)
        self.initialized = True
        
        print(f"✅ Weave tracing initialized for project: {self.project_name}")
    
    def trace_crew_execution(self, crew_name: str, task_name: str):
        """
        Create a context manager for tracing crew execution.
        
        Args:
            crew_name: Name of the crew
            task_name: Name of the task
            
        Returns:
            Weave trace context manager
        """
        trace_name = f"crew.{crew_name}.{task_name}"
        return weave.trace(name=trace_name)
    
    def trace_agent_action(self, agent_name: str, action: str):
        """
        Create a context manager for tracing agent actions.
        
        Args:
            agent_name: Name of the agent
            action: Action being performed
            
        Returns:
            Weave trace context manager
        """
        trace_name = f"agent.{agent_name}.{action}"
        return weave.trace(name=trace_name)
    
    def trace_mcp_call(self, server_name: str, method: str):
        """
        Create a context manager for tracing MCP calls.
        
        Args:
            server_name: Name of the MCP server
            method: Method being called
            
        Returns:
            Weave trace context manager
        """
        trace_name = f"mcp.{server_name}.{method}"
        return weave.trace(name=trace_name)


# Global trace manager instance
_trace_manager = None


def setup_weave_tracing(project_name: str = "crewai-mcp-pipeline", api_key: str = None) -> WeaveTraceManager:
    """
    Set up Weave tracing for the application.
    
    Args:
        project_name: Name of the Weave project
        api_key: W&B API key (optional)
        
    Returns:
        WeaveTraceManager instance
    """
    global _trace_manager
    
    if _trace_manager is None:
        _trace_manager = WeaveTraceManager(project_name)
    
    _trace_manager.initialize(api_key)
    return _trace_manager


def get_trace_manager() -> Optional[WeaveTraceManager]:
    """
    Get the global trace manager instance.
    
    Returns:
        WeaveTraceManager instance or None if not initialized
    """
    return _trace_manager


# Convenience functions for common tracing patterns
def trace_crew(crew_name: str, task_name: str = "execute"):
    """
    Decorator for tracing crew execution.
    
    Args:
        crew_name: Name of the crew
        task_name: Name of the task
    """
    return traced(component=f"crew.{crew_name}", operation=task_name)


def trace_agent(agent_name: str, action: str = "execute"):
    """
    Decorator for tracing agent actions.
    
    Args:
        agent_name: Name of the agent
        action: Action being performed
    """
    return traced(component=f"agent.{agent_name}", operation=action)


def trace_mcp(server_name: str, method: str = "call"):
    """
    Decorator for tracing MCP calls.
    
    Args:
        server_name: Name of the MCP server
        method: Method being called
    """
    return traced(component=f"mcp.{server_name}", operation=method)


def trace_flow(flow_name: str, stage: str = "execute"):
    """
    Decorator for tracing flow execution.
    
    Args:
        flow_name: Name of the flow
        stage: Stage being executed
    """
    return traced(component=f"flow.{flow_name}", operation=stage)


# Example usage
if __name__ == "__main__":
    # Initialize tracing
    trace_manager = setup_weave_tracing("test-project")
    
    @traced("test_component", "test_operation")
    def test_function(param1: str, param2: int) -> dict:
        """Test function with tracing."""
        return {"result": f"processed {param1} with {param2}"}
    
    # Test the function
    result = test_function("test_data", 42)
    print(f"Result: {result}")
    
    print("✅ Tracing test completed") 