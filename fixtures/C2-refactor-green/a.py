def register_user(users, name):
    """Register a user with a normalized display name."""
    cleaned = " ".join(name.strip().split()).title()
    if cleaned in users:
        raise ValueError(f"duplicate user: {cleaned}")
    users.append(cleaned)
    return cleaned
