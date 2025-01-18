def is_mobile(user_agent: str) -> bool:
    """Check if the user agent is from a mobile device."""
    mobile_patterns = [
        'Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone',
        'webOS', 'BlackBerry', 'Samsung', 'Opera Mini'
    ]
    return any(pattern.lower() in user_agent.lower() for pattern in mobile_patterns)