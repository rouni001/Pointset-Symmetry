import math
from typing import Dict, List, DefaultDict
from point2d import Point2D

from constants import EPSILON
from point import Point
from pointset import PointSet
from pointset_symmetry_analyzer import (
    SymmetryLineSet,
    SymmetryLineValidator,
    LineDirectionKey
)


class PointSetSymmetryAnalyzer:
    """
    Provides static methods to identify the symmetry lines existing in a 
    point set. Here is implemented the fast/optimized algorithm for processing
    the points as defined in a PointSet object.

    Static Methods:
        find_symmetry: Returns the symmetry lines, directions and 
            points at their edges, from a PointSet object.
        is_symmetric: Check whether a line is a symmetry line
            giving the topology of the pointset.
        create_symmetry_lines_endpoints: Returns coordinates of the symmetry 
            lines.
        infer_next_symmetric: Populates the SymmetryLineSet object with new 
            symmetry lines inferred from "new_symmetry_line" and the known 
            symmetry lines.

    """
    @staticmethod
    def find_symmetry(points: PointSet):
        """
        Finds all the symmetry lines (directions and edge points) existing in a
        PointSet object.

        Returns:
            List[str]:  The directions of the symmetry lines identified (as an
                angles in degree formatted as str).
            Dict[str, List[Point2D]]: A dictionary providing for each 
                identified symmetry line two 2D points delimiting it. 
        """
        lines = SymmetryLineSet()
        # Create a partition of the points per color
        color_to_points = DefaultDict(list)
        for p in points.get():
            color_to_points[p["color"]].append(p)

        for p in points.get():
            if (p["location"] - points.barycenter()).r < EPSILON:
                continue
            # Determine the direction of the (PB), the line passing
            # through the barycenter B and the current point p:
            line =  points.barycenter() - p["location"]

            # Skip if (PB) is a symmetry line already found/tested:
            if lines.contains(line):
                continue
            # Check whether (PB) is symmetric across the points partition:
            symmetry = PointSetSymmetryAnalyzer.is_symmetric(
                color_to_points, line, points.barycenter()
                )
            if symmetry:
                PointSetSymmetryAnalyzer.infer_next_symmetric(lines, line)
            lines.add(line, symmetry)

        if points.size() %  2 == 0:    
        # Find more symmetry using equidistant points when the size is even:
            for partition_block in color_to_points.values():
                if len(partition_block) == 1:
                    continue    
                for a in range(len(partition_block)):
                    for b in range(a + 1, len(partition_block)):
                        # Determine the direction of the (MB), the line passing
                        # through B and the midpoint M of 2 equidistant points,
                        # A and B, using the current partition blocck:
                        mid_point = partition_block[a]["location"] + \
                            partition_block[b]["location"]
                        mid_point.r /= 2.0
                        line =  points.barycenter() - mid_point

                        # Skip if (MB) is a symmetry line already found/tested:
                        if lines.contains(line):
                            continue
                        # Check whether (MB) is symmetric across the points 
                        # partition:
                        symmetric = PointSetSymmetryAnalyzer.is_symmetric(
                            color_to_points, line, points.barycenter()
                            )
                        if symmetric:
                            PointSetSymmetryAnalyzer.infer_next_symmetric(
                                lines, line
                                )
                        lines.add(line, symmetric)

        return lines.get_symmetric_directions(), \
            PointSetSymmetryAnalyzer.create_symmetry_lines_endpoints(
                points.barycenter(), 
                points.radius(), 
                lines.get_symmetric_lines()
            )

    @staticmethod
    def is_symmetric(
        partition: Dict[str, List[Point]], line: Point2D, barycenter: Point2D
        ):
        """
        Check whether a line is a symmetry line giving the topology of the 
        pointset.

        Returns:
            bool: True if the line is symmetric, False otherwise. 
        """
        # Check points not equidistant with any point to the barycenter are
        # aligned with/on the line:
        #   These points are those that do not share a color with any other 
        #   points, thus, they are in partition blocks of size one. 
        for single_point_block in partition.values():
            if len(single_point_block) > 1:
                continue
            if not SymmetryLineValidator.is_aligned(
                single_point_block[0], line, barycenter
                ):
                return False
        # Check that equidistant points to the barycenter are symmetric to 
        # the line:
        #   These points are those that share a color with at least one/several
        #   other points, thus, they are in partition blocks 
        #   with multiple points.             
        for multiple_points_block in partition.values():                
            if len(multiple_points_block) == 1:
                continue
            if not SymmetryLineValidator.is_symmetric(
                multiple_points_block, line, barycenter
                ):
                return False
        return True

    @staticmethod
    def create_symmetry_lines_endpoints(
        barycenter: Point2D, radius: float, symmetry_directions: List[Point2D]
        ) -> Dict[str, List[Point2D]]:
        """
        Returns the coordinates of the symmetry lines.

        Returns:
            Dict[str, List[Point2D]]: A dictionary providing for each 
                identified symmetry line L two 2D points delimiting L.
        """
        res = {}
        for direction in symmetry_directions.values():
            res[direction] = [
                Point2D(barycenter.x + math.cos(direction.a) * radius, 
                        barycenter.y + math.sin(direction.a) * radius),
                Point2D(barycenter.x - math.cos(direction.a) * radius, 
                        barycenter.y - math.sin(direction.a) * radius)
            ]
        return res
    
    @staticmethod
    def infer_next_symmetric(
        lines: SymmetryLineSet, new_symmetry_line: Point2D
        ) -> None:
        """
        Populates the SymmetryLineSet object with new symmetry lines inferred 
        from "new_symmetry_line" and the known symmetry lines.
        """
        new_lines: Dict[str, Point2D] = {}
        # Searching for symmetry lines possibly not identified yet:

        for existing_line in lines.get_symmetric_lines().values() :
            angle_step = existing_line.a - new_symmetry_line.a
            # Create L the symmetric line of "existing_line" against 
            # "new_symmetry_line": 
            line_from_new = Point2D(0,0)
            line_from_new.a = (new_symmetry_line.a - angle_step) % math.pi
            # Check whether L is already known:
            if LineDirectionKey.calculate(line_from_new) not in new_lines:
                new_lines[LineDirectionKey.calculate(line_from_new)] = \
                    line_from_new
            # Create M the symmetric line of "new_symmetry_line" line 
            # against "existing_line": 
            line_from_existing = Point2D(0,0)
            line_from_existing.a = (existing_line.a + angle_step) % math.pi
            # Check whether M is already known:
            if LineDirectionKey.calculate(line_from_existing) not in new_lines:
                new_lines[LineDirectionKey.calculate(line_from_existing)] = \
                    line_from_existing
        # Indexing the new symmetry lines found:
        for new_line in new_lines.values():
            if not lines.contains(new_line, False):
                lines.add(new_line, True)



