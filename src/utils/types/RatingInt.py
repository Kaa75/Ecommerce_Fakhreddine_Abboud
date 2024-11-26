from typing import Annotated

from pydantic import BeforeValidator, PositiveInt


def validate_rating(rating: PositiveInt) -> int:
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5")
    return rating


RatingInt = Annotated[PositiveInt, BeforeValidator(validate_rating)]
