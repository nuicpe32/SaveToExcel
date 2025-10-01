"""
Case Number Generator Utility
Generates running numbers for criminal cases in format: {number}/{buddhist_year}
Example: 1385/2568
"""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, cast, Integer
from app.models.criminal_case import CriminalCase


def get_buddhist_year() -> int:
    """
    Get current Buddhist Era year
    Buddhist Era = Christian Era + 543
    """
    current_year = datetime.now().year
    return current_year + 543


def generate_case_number(db: Session, custom_year: int = None) -> str:
    """
    Generate next case number in format: {number}/{year}

    Args:
        db: Database session
        custom_year: Optional custom Buddhist year (default: current year)

    Returns:
        str: Generated case number, e.g., "1385/2568"

    Example:
        >>> generate_case_number(db)
        "1385/2568"
    """
    buddhist_year = custom_year or get_buddhist_year()
    year_suffix = str(buddhist_year)

    # Find the maximum number for this year
    # Query pattern: {number}/{year}
    max_number = db.query(
        func.max(
            cast(
                func.split_part(CriminalCase.case_number, '/', 1),
                Integer
            )
        )
    ).filter(
        CriminalCase.case_number.like(f'%/{year_suffix}')
    ).scalar()

    # If no cases exist for this year, start from 1
    next_number = (max_number or 0) + 1

    # Format: {number}/{year}
    case_number = f"{next_number}/{buddhist_year}"

    return case_number


def parse_case_number(case_number: str) -> dict:
    """
    Parse case number into components

    Args:
        case_number: Case number string, e.g., "1385/2568"

    Returns:
        dict: {"number": 1385, "year": 2568, "original": "1385/2568"}

    Example:
        >>> parse_case_number("1385/2568")
        {"number": 1385, "year": 2568, "original": "1385/2568"}
    """
    if not case_number or '/' not in case_number:
        return {"number": None, "year": None, "original": case_number}

    try:
        parts = case_number.split('/')
        number = int(parts[0])
        year = int(parts[1])
        return {"number": number, "year": year, "original": case_number}
    except (ValueError, IndexError):
        return {"number": None, "year": None, "original": case_number}


def validate_case_number(case_number: str) -> bool:
    """
    Validate case number format

    Args:
        case_number: Case number string to validate

    Returns:
        bool: True if valid, False otherwise

    Example:
        >>> validate_case_number("1385/2568")
        True
        >>> validate_case_number("invalid")
        False
    """
    if not case_number or '/' not in case_number:
        return False

    parsed = parse_case_number(case_number)
    return parsed["number"] is not None and parsed["year"] is not None


def get_year_statistics(db: Session, year: int = None) -> dict:
    """
    Get statistics for cases in a specific year

    Args:
        db: Database session
        year: Buddhist year (default: current year)

    Returns:
        dict: Statistics including total count, latest number, etc.
    """
    buddhist_year = year or get_buddhist_year()
    year_suffix = str(buddhist_year)

    # Count cases for this year
    total_cases = db.query(func.count(CriminalCase.id)).filter(
        CriminalCase.case_number.like(f'%/{year_suffix}')
    ).scalar() or 0

    # Get latest case number
    latest_number = db.query(
        func.max(
            cast(
                func.split_part(CriminalCase.case_number, '/', 1),
                Integer
            )
        )
    ).filter(
        CriminalCase.case_number.like(f'%/{year_suffix}')
    ).scalar() or 0

    return {
        "year": buddhist_year,
        "total_cases": total_cases,
        "latest_number": latest_number,
        "next_number": latest_number + 1
    }
