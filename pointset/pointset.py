from typing import Dict, List
from point2d import Point2D

from constants import EPSILON
from file_data_importer import FileDataImporter
from point import Point


class PointSet:
    """
    Annotates a set of points from a CSV file.

    Attributes:
        point_set (Dict[str, Point]): A dictionary to store the points. 
        set_barycenter (Point2D]): The barycenter of the point set. 
        set_radius (float): The maximum distance between the barycenter and 
            any point in the point set. 

    Methods:
        size:   Returns the number of points in the set.
        get:    Returns the points of the set.
        barycenter: Returns the barycenter of the set
        radius: Returns the radius of the set.
        ids:    Returns the ids of the points.
        colors: Returns the colors of the points. 
    """

    def __init__(self, filename: str) -> None:
        """
        Initializes the object by loading points data from a CSV file.

        Parameter:
            filename (str): the path of the file containing the points data.
        """
        self.point_set: Dict[str, Point] = {}
        self.set_barycenter: Point2D = Point2D(0,0)
        self.set_radius: float = 0.0

        points = FileDataImporter.load_points(filename)
        if len(points) == 0:
            raise Exception(
                f"Failed to access points from {filename}: File empty?"
                )
        
        for (idx, pt) in enumerate(points):
            point: Point={
                    "location": pt,
                    "id": str(idx),
                    "color": 0
                    }
            self.point_set[str(idx)] = point
            self.set_barycenter += pt

        self.set_barycenter.r /= float(len(points))
        self.__set_colors_and_distances()

    def __set_colors_and_distances(self) -> None:
        """
        Private method to assign the colors and distances to each point.
        This method sorts all the points using their distances to the 
        barycenter and groups together points of same distance. Points
        of the same distance are assigned the same and unique color index.
        Finally, for each point, the color index and distance calculated
        are saved in their Point attributes.
        """
        point_to_barycenter_distances = {}
        for (idx, point) in self.point_set.items():
            point_to_barycenter_distances[idx] = \
                (point["location"] - self.set_barycenter).r
        sorted_distances_dict = dict(
                sorted(
                    point_to_barycenter_distances.items(), 
                    key=lambda item: item[1], 
                    reverse=True
                    )
                )
        self.set_radius = sorted_distances_dict[[*sorted_distances_dict][0]]
        color = 1
        prev_distance = None
        for (idx, distance) in sorted_distances_dict.items():
            if prev_distance is None:
                prev_distance = distance
            elif abs(prev_distance - distance) > EPSILON:
                prev_distance = distance
                color += 1
            self.point_set[idx]["color"] = color
            self.point_set[idx]["distance_barycenter"] = distance

    def size(self) -> int:
        """
        Returns the number of points in the set.
        """
        return len(self.point_set)

    def get(self) -> List[Point]:
        """
        Returns the points of the set.   
        """
        return [*self.point_set.values()]

    def ids(self) -> List[str]:
        """
        Returns the ids of the points.

        Raises:
            Exception: If the point set is empty        
        """
        if len(self.point_set) > 0:
            return [point["id"] for point in self.point_set.values()]
        raise Exception("Failed to access points ids: Point Set is empty.")

    def colors(self) -> List[float]:
        """
        Returns the colors of the points. 

        Raises:
            Exception: If the point set is empty        
        """
        if len(self.point_set) > 0:
            return [point["color"] for point in self.point_set.values()]
        raise Exception("Failed to access points colors: Point Set is empty.")
    
    def barycenter(self) -> Point2D:
        """
        Returns the barycenter of the set.

        Raises:
            Exception: If the point set is empty
        """
        if len(self.point_set) > 0:
            return self.set_barycenter
        raise Exception("Failed to get the set barycenter: Pointset is empty.")
    
    def radius(self) -> Point2D:
        """
        Returns the radius of the set.

        Raises:
            Exception: If the point set is empty.   
        """
        if len(self.point_set) > 0:
            return self.set_radius
        raise Exception("Failed to get the set radius: Pointset is empty.")

