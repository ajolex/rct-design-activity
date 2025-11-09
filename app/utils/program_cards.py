"""
Utilities for loading and managing program cards.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import PROGRAM_CARDS


def get_all_program_cards() -> Dict[str, Dict]:
    """
    Get all available program cards.
    Returns a dictionary keyed by card ID with card metadata.
    """
    return PROGRAM_CARDS


def get_program_card(card_id: str) -> Optional[Dict]:
    """
    Get a specific program card by ID.
    
    Args:
        card_id: The unique identifier for the card (e.g., 'education_bridge_to_basics')
    
    Returns:
        The card dictionary or None if not found
    """
    return PROGRAM_CARDS.get(card_id)


def get_card_display_name(card_id: str) -> str:
    """
    Get a human-readable display name for a card.
    """
    card = get_program_card(card_id)
    return card["title"] if card else card_id


def get_cards_by_sector(sector: str) -> Dict[str, Dict]:
    """
    Get all cards for a specific sector (e.g., 'Education', 'Health', 'Agriculture').
    """
    return {
        card_id: card
        for card_id, card in PROGRAM_CARDS.items()
        if card.get("sector") == sector
    }


def validate_card_exists(card_id: str) -> bool:
    """
    Check if a program card exists.
    """
    return card_id in PROGRAM_CARDS


def load_card_from_json(json_path: Path) -> Dict:
    """
    Load a program card definition from a JSON file.
    Useful for extending with custom cards.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_card_to_json(card_data: Dict, output_path: Path) -> None:
    """
    Save a program card definition to a JSON file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(card_data, f, indent=2)


def format_card_for_display(card: Dict) -> Dict:
    """
    Format a program card for display in the UI.
    Adds HTML-safe strings and structured sections.
    """
    return {
        "title": card.get("title"),
        "sector": card.get("sector"),
        "theme": card.get("theme"),
        "context_sections": [
            ("Problem", card.get("context", {}).get("problem")),
            ("Resources", card.get("context", {}).get("resources")),
            ("Logistics", card.get("context", {}).get("logistics")),
        ],
        "concept_sections": [
            ("Activities", card.get("concept", {}).get("activities")),
            ("Approach", card.get("concept", {}).get("approach")),
            ("Engagement", card.get("concept", {}).get("engagement")),
        ],
        "decision_horizon": card.get("decision_horizon"),
        "reach": card.get("metrics", {}).get("reach"),
        "budget": card.get("metrics", {}).get("budget"),
        "considerations": card.get("considerations"),
    }
