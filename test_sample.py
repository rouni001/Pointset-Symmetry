from pointset import PointSet
from pointset_symmetry_analyzer import PointSetSymmetryAnalyzer
from pointset_symmetry_viewer import PointSetSymmetryViewer


print("Test A1: Simple case, 1 symmetry line")
s = PointSet("./tests/data/simple_test.csv")
symmetry_directions, symmetry_lines_points = PointSetSymmetryAnalyzer.find_symmetry(s)
PointSetSymmetryViewer.plot(s, symmetry_lines_points, "tests/results/fig00A1")
print(symmetry_directions)
assert(len(symmetry_directions) ==  1)
