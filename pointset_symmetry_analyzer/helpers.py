import math
from typing import Dict, List
from point2d import Point2D

from constants import EPSILON, MAX_PRECISION
from point import Point


class LineDirectionKey:
    """
    Provides one static method to generate the key value representing the 
    angle of a line.

    Static Methods:
        calculate:    Returns the key value representing the angle of a line.
    """
    @staticmethod
    def calculate(line: Point2D) -> str:
        """
        Returns the key value representing the angle of a line.

        Parameters:
            line (Point2D): A line as Point2D.

        Returns:
            str: the string value representing the angle of a line.
        """
        def round_to_precision(value):
            """
            Rounds a value to the precision
            """
            return round(value * MAX_PRECISION) / MAX_PRECISION
        
        angle = 0 if abs(line.a) < EPSILON or abs(math.pi - line.a) < EPSILON \
        else line.a % math.pi
        value = max(
            round_to_precision(math.degrees((math.pi + angle) % math.pi)),
            round_to_precision(math.degrees(angle))
        )
        return str(value)


class SymmetryLineSet:
    """
    This class implements a container of lines tested for symmetry on a 
    point set. It stores lines identified as symmetric and non-symmetric.

    Attributes:
        symmetric_lines (Dict[str, Point2D]): A dictionary containing the 
            symmetry lines.
        non_symmetric_lines (Set): A set containing the lines known to be 
            non-symmetric.
        
    Methods:
        add: Inserts a line either as symmetry line or non-symmetry line.
        contains: Check whether a line is known as a symmetry line or 
            a non-symmetry line.
        symmetric_directions: Returns the directions of the symmetry 
            lines as a list.
        symmetry_lines: Returns the symmetry lines as a dictionary.
    """
    def __init__(self) -> None:
        self.symmetric_lines: Dict[str, Point2D] = {}
        self.non_symmetric_lines = set()

    def add(self, line: Point2D, symmetric: bool = False) -> None:
        """
        Inserts a line either as symmetry line or non-symmetry line.

        Parameters:
            line (Point2D): A line to be inserted.
            symmetric (bool): If True, then the line is inserted as
                symmetric, otherwise as non-symmetric.
        """
        line_key = LineDirectionKey.calculate(line)
        if symmetric:
            if line_key not in self.symmetric_lines:
                self.symmetric_lines[line_key] = line
        else:
            if line_key not in self.non_symmetric_lines:
                self.non_symmetric_lines.add(line_key)

    def contains(self, line: Point2D, check_non_symmetry: bool = True) -> bool:
        """
        Check whether a line is present as a symmetry line or non-symmetry 
        line. This is achieved by checking, as default, the presence in the 
        set of symmetry lines and the set of non-symmetry lines.

        Parameters:
            line (Point2D): The line to check the presence in the sets.
            check_non_symmetry (bool): To indicate whether the search should
                include the set of non-symmetry lines (default: True).

        Returns:
            bool:   True if the line is an symmetry line or non-symmetry line,
                False otherwise, when check_non_symmetry is True.
                    True if the line is an symmetry line,
                False otherwise, when check_non_symmetry is False.
        """
        line_key = LineDirectionKey.calculate(line)
        if line_key in self.symmetric_lines:
            return True
        if check_non_symmetry:
            return line_key in self.non_symmetric_lines
        return False
    
    def get_symmetric_directions(self) -> List[str]:
        """
        Returns the directions of the symmetry lines as a list.

        Returns:
            List[str]: The list of directions (i.e. the line direction key).
        """
        return [*self.symmetric_lines]

    def get_symmetric_lines(self) -> Dict[str, Point2D]:
        """
        Returns the symmetry lines as a dictionary.

        Returns:
            Dict[str, Point2D]:   Key: A line direction key,
                Value: The line as a Point2D object.
        """
        return self.symmetric_lines


class SymmetryLineValidator:
    """
    Provides static methods for validating a line as symmetric given 
    a subset of points (List[Point]).

    Static Methods:
        symmetric: Checks whether a line is a symmetric to a set of 
            mono-colored points.
        aligned: Checks whether a point is aligned with a line.
        get_projected_distance_key: Computes the key of the relative of 
            a projected point against a line. 

    """
    @staticmethod
    def is_symmetric(
        mono_colored_points: List[Point], line: Point2D, barycenter: Point2D
        ) -> bool:
        """
        Checks whether a line is a symmetric to a set of mono-colored points. 
        Because the points passed are mono-colored, the line is symmetric if 
        the number of projected points against the symmetry is equal to half 
        the number of these mono-colored points (except predictable cases, like
        one or several of the points are on that line already, or one of the 
        points is too close to the barycenter).

        Parameters:
            points (List[Point): A list of points of the same color.
            line (Point2D): The line to checky symmetry against.
            barycenter (Point2D): The barycenter of a point set.

        Returns:
            bool: True if the line is symmetric, False otherwise.
        """
        points_on_line_count = 0
        unique_projected_points_count = set()
        points_processed_count = len(mono_colored_points)
        for point in mono_colored_points:
            if (point["location"] - barycenter).r < EPSILON:
                points_processed_count -= 1
                continue
            angle_barycenter_point_vs_line = \
                (point["location"] - barycenter).a - (line).a
            if SymmetryLineValidator.is_aligned(point, line, barycenter):
                 points_on_line_count += 1
            else:
                distance_key = SymmetryLineValidator.get_projected_distance_key(
                    point["distance_barycenter"], angle_barycenter_point_vs_line
                    )
                if distance_key not in unique_projected_points_count:
                    unique_projected_points_count.add(distance_key)
        return len(unique_projected_points_count) * 2 == \
            points_processed_count - points_on_line_count

    @staticmethod
    def is_aligned(point: Point, line: Point2D, barycenter: Point2D) -> bool:
        """
        Checks whether the point passed as parameter is aligned with the line 
        or that the line passes through that point.

        Parameters:
            point (Point): The point as an Point object.
            line (Point2D): The line as an Point2D object.
            barycenter (Point2D): The barycenter.

        Returns:
            bool: True if the point is aligned, False otherwise.
        """
        if (point["location"] - barycenter).r < EPSILON:
            return True
        angle = (point["location"] - barycenter).a - (line).a
        return abs(angle % math.pi) < EPSILON or \
            abs((abs(angle) - math.pi) % math.pi) < EPSILON
    
    @staticmethod
    def get_projected_distance_key(
        distance_barycenter: float, point_line_barycenter_angle: float
        ) -> str:
        """
        Computes the key of the relative distance of a projected point 
        against a line. 

        Parameters:
            distance_barycenter (float): The distance of the point to 
                the barycenter.
            point_line_barycenter_angle (float): The angle between a point, 
                the barycenter and a line.

        Results:
            str: The key value representing the relative distance of the 
            projected point 
        """
        return str(
            float(
                round(MAX_PRECISION * distance_barycenter * math.cos(
                    point_line_barycenter_angle
                )) / MAX_PRECISION)
            )

