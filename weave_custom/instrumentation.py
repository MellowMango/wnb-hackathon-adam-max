"""
Observability Instrumentation

Decorators and utilities for adding observability to MCP tool calls.
"""

import time
import functools
import weave
from typing import Any, Callable


def instrument_mcp_call(service_name: str):
    """
    Decorator to instrument MCP tool calls with timing and logging.
    
    Args:
        service_name: Name of the MCP service (e.g., 'youtube', 'maps')
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @weave.op(name=f"mcp.{service_name}.{func.__name__}")
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Log success metrics
                weave.log({
                    "service": service_name,
                    "function": func.__name__,
                    "duration_ms": duration * 1000,
                    "status": "success",
                    "args_count": len(args),
                    "kwargs_count": len(kwargs)
                })
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Log error metrics
                weave.log({
                    "service": service_name,
                    "function": func.__name__,
                    "duration_ms": duration * 1000,
                    "status": "error",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "args_count": len(args),
                    "kwargs_count": len(kwargs)
                })
                
                raise
                
        return wrapper
    return decorator


def instrument_agent_task(agent_name: str):
    """
    Decorator to instrument agent task execution.
    
    Args:
        agent_name: Name of the agent
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @weave.op(name=f"agent.{agent_name}.{func.__name__}")
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Log agent task metrics
                weave.log({
                    "agent": agent_name,
                    "task": func.__name__,
                    "duration_ms": duration * 1000,
                    "status": "completed",
                    "result_type": type(result).__name__
                })
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Log agent error metrics
                weave.log({
                    "agent": agent_name,
                    "task": func.__name__,
                    "duration_ms": duration * 1000,
                    "status": "failed",
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })
                
                raise
                
        return wrapper
    return decorator


def instrument_workflow(workflow_name: str):
    """
    Decorator to instrument complete workflow execution.
    
    Args:
        workflow_name: Name of the workflow
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @weave.op(name=f"workflow.{workflow_name}")
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Log workflow metrics
                weave.log({
                    "workflow": workflow_name,
                    "duration_ms": duration * 1000,
                    "status": "completed",
                    "result_type": type(result).__name__
                })
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Log workflow error metrics
                weave.log({
                    "workflow": workflow_name,
                    "duration_ms": duration * 1000,
                    "status": "failed",
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })
                
                raise
                
        return wrapper
    return decorator