"""portfolio_hq — repository-native, read-only presentation utilities.

This package contains NO investment logic, NO order path, and NO brokerage
connection. It reads the repository's own authoritative files and presents
them. It never mutates holdings.yaml, targets.yaml, accepted decisions,
workstreams, allocator behavior, or margin behavior. See
docs/PORTFOLIO_HQ_DASHBOARD_DESIGN.md for the presentation/authority boundary.
"""

__all__ = ["dashboard"]
