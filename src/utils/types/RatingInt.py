"""Module for defining and validating the RatingInt type."""

from typing import Annotated

from pydantic import BeforeValidator, PositiveInt


def validate_rating(rating: PositiveInt) -> int:
    """Validate that the rating is between 1 and 5.

    Args:
        rating (PositiveInt): The rating value to validate.

    Returns:
        int: The validated rating.

    Raises:
        ValueError: If the rating is not between 1 and 5.
    """
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5")
    return rating


# Type alias for a validated rating integer between 1 and 5
RatingInt = Annotated[PositiveInt, BeforeValidator(validate_rating)]
