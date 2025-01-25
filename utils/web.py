from typing import Dict, List


def is_mobile(user_agent: str) -> bool:
    """Check if the user agent is from a mobile device."""
    mobile_patterns = [
        'Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone',
        'webOS', 'BlackBerry', 'Samsung', 'Opera Mini'
    ]
    return any(pattern.lower() in user_agent.lower() for pattern in mobile_patterns)

def russian_keyboard_layout() -> Dict[str, List[str]]:
    """
    Returns a Russian keyboard layout.
    """
    russian_layout = {
        'row1': ['ё', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
        'row2': ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ'],
        'row3': ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э'],
        'row4': ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.']
    }   
    return russian_layout
