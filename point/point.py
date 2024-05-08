from typing_extensions import TypedDict
from point2d import Point2D


class Point(TypedDict):
    """
    Two-dimmensional point from a set. 

    Attributes:
        id (str):   The id/name of the point.
        location (Point2D): The coordinates (cartesian/polar).
        color (int):    The color of the set partiton this point belongs to.
        distance_barycenter (float): The distance between the point and the
            barycenter of the set.
    """
    id: str
    location: Point2D
    color: int
    distance_barycenter: float

