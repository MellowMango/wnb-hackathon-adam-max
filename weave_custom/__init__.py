"""
Weave Integration Package

This package provides W&B Weave integration for observability and tracing.
"""

from .trace_hooks import traced, setup_weave_tracing
from .config import WeaveConfig

__all__ = ["traced", "setup_weave_tracing", "WeaveConfig"] 