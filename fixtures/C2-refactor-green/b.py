def format_badge(name):
    """Format a conference badge label for a person."""
    cleaned = " ".join(name.strip().split()).title()
    return f"[{cleaned}]"
