"""
Weave Configuration

This module provides configuration management for Weave integration.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class WeaveConfig:
    """
    Configuration for Weave integration.
    """
    
    # Project settings
    project_name: str = "crewai-mcp-pipeline"
    api_key: Optional[str] = None
    
    # Tracing settings
    trace_all_agents: bool = True
    trace_all_tasks: bool = True
    trace_all_flows: bool = True
    trace_mcp_calls: bool = True
    
    # Data settings
    max_string_length: int = 1000
    max_list_items: int = 10
    sanitize_sensitive_data: bool = True
    
    # Performance settings
    enable_async_logging: bool = True
    batch_size: int = 100
    flush_interval: int = 30
    
    @classmethod
    def from_environment(cls) -> "WeaveConfig":
        """
        Create configuration from environment variables.
        
        Returns:
            WeaveConfig instance
        """
        return cls(
            project_name=os.getenv("WANDB_PROJECT", "crewai-mcp-pipeline"),
            api_key=os.getenv("WANDB_API_KEY"),
            trace_all_agents=os.getenv("WEAVE_TRACE_AGENTS", "true").lower() == "true",
            trace_all_tasks=os.getenv("WEAVE_TRACE_TASKS", "true").lower() == "true",
            trace_all_flows=os.getenv("WEAVE_TRACE_FLOWS", "true").lower() == "true",
            trace_mcp_calls=os.getenv("WEAVE_TRACE_MCP", "true").lower() == "true",
            max_string_length=int(os.getenv("WEAVE_MAX_STRING_LENGTH", "1000")),
            max_list_items=int(os.getenv("WEAVE_MAX_LIST_ITEMS", "10")),
            sanitize_sensitive_data=os.getenv("WEAVE_SANITIZE_DATA", "true").lower() == "true",
            enable_async_logging=os.getenv("WEAVE_ASYNC_LOGGING", "true").lower() == "true",
            batch_size=int(os.getenv("WEAVE_BATCH_SIZE", "100")),
            flush_interval=int(os.getenv("WEAVE_FLUSH_INTERVAL", "30"))
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of configuration
        """
        return {
            "project_name": self.project_name,
            "api_key": "[REDACTED]" if self.api_key else None,
            "trace_all_agents": self.trace_all_agents,
            "trace_all_tasks": self.trace_all_tasks,
            "trace_all_flows": self.trace_all_flows,
            "trace_mcp_calls": self.trace_mcp_calls,
            "max_string_length": self.max_string_length,
            "max_list_items": self.max_list_items,
            "sanitize_sensitive_data": self.sanitize_sensitive_data,
            "enable_async_logging": self.enable_async_logging,
            "batch_size": self.batch_size,
            "flush_interval": self.flush_interval
        }


# Global configuration instance
_config = None


def get_weave_config() -> WeaveConfig:
    """
    Get the global Weave configuration.
    
    Returns:
        WeaveConfig instance
    """
    global _config
    if _config is None:
        _config = WeaveConfig.from_environment()
    return _config


def set_weave_config(config: WeaveConfig):
    """
    Set the global Weave configuration.
    
    Args:
        config: WeaveConfig instance
    """
    global _config
    _config = config 