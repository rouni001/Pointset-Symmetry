import os
import csv
from typing import List
from point2d import Point2D


class FileDataImporter:
    """
    Provides statics methods for importing points data from csv files. 
    This class is responsible for handling file reading and exceptions.

    Static Methods:
        load_points_from_csv: Reads points from a CSV file and returns 
            points as a list.
        load_points: Validates file existence and handle exception thrown 
            by load_points_from_csv.
    """
    @staticmethod
    def load_points_from_csv(filename: str) -> List[Point2D]:
        """
        Reads points from a CSV file and returns points as a list.

        Parameters:
            filename (str): The path of the file.

        Returns:
            List[Point2D]: The list of points from the file as Point2D.
        
        Raises:
            Exception: If the file is malformed or missing the X,Y values. 
        """
        points: List[Point2D] = []
        with open(filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) < 1:
                    continue
                if len(row) < 2:
                    raise Exception(f"Missing X, Y coordinates in row: {row}")
                points.append(Point2D(float(row[0]), float(row[1])))
        return points

    @staticmethod
    def load_points(filename: str) -> List[Point2D]:
        """
        Validates file existence and handle exception thrown by 
        "load_points_from_csv".

        Parameters:
            filename (str): The path of the file.

        Returns:
            List[Point2D]: The list of points as Point2D type.
        
        Raises:
            Exception: If the file contains a line without two values. 
        """        
        if not os.path.exists(filename):
            raise Exception(f"Failed to access file: {filename}")
        points = []
        try:
            points = FileDataImporter.load_points_from_csv(filename)
        except Exception as e:
            raise Exception(
                    f"Failed to extract coordinates in points in {filename}."
                    ).with_traceback(e.__traceback__)
        return points
