from typing import Dict, List
from point2d import Point2D
import matplotlib.pyplot as plt

from pointset import PointSet



class PointSetSymmetryViewer:
    """
    Provides statics methods for visualizing the point set and its symmetry 
    lines. 
    
    Note: This class is implemented primarily for TESTING/DEBUGGING purposes.
        A more advanced class would be implemented for presentation goals to
        a wide audience.

    Static Methods:
        plot: Plots and generates a figure image placing the points and the 
            symmetry lines.
        get_color_name: Returns a RGBA code corresponding to a color index.
    """
    @staticmethod
    def plot(
        points: PointSet, 
        symmetry_lines: Dict[str, List[Point2D]], 
        fig_filename: str, 
        include_labels: bool = True, 
        include_barycenter: bool = True
        ) -> None:
        """
        Plots and generates a figure image where the points and the symmetry 
        lines are placed.

        Parameters:
            points (PointSet): The point set.
            symmetry_lines (Dict[str, List[Point2D]]): The dictionary 
                containting the coordinates of the symmetry lines.
            fig_filename (str): The path of the figure to save the plot/image 
                generated.
            include_labels (bool): Whether the points label should be included
                in the image.
            include_barycenter (bool): Whether the barycenter point should 
                be included in the image.
        """
        x_coords = [pt["location"].x for pt in points.get()]
        y_coords = [pt["location"].y for pt in points.get()]
        labels = points.ids()
        colors = [
            PointSetSymmetryViewer.get_color_name(c) for c in points.colors()
            ]

        if include_barycenter:
            labels.append("Barycenter")
            x_coords.append(points.barycenter().x)
            y_coords.append(points.barycenter().y)
            colors.append((0,0,0,1))

        fig, ax = plt.subplots()
        ax.scatter(x_coords, y_coords, c=colors)

        if include_labels:
            for (i, idx) in enumerate(labels):
                ax.annotate(idx, (x_coords[i], y_coords[i]))

        for coord_points in symmetry_lines.values():
            plt.plot(
                [pt.x for pt in coord_points], 
                [pt.y for pt in coord_points], 
                linestyle='-'
                )
        plt.savefig(fig_filename)
        plt.show()

    @staticmethod
    def get_color_name(index: int) -> str:
        """
        Returns a color name corresponding to a color group index.

        Paramaeters:
            index (int): A color group index

        Returns:
            Tuple[float, float, float, float]: RGBA code value corresponding
                to the indx.
        """
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        return colors[index % len(colors)]


