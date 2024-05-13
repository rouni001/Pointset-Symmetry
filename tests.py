import math
import unittest
from point2d import Point2D

from pointset import PointSet
from pointset_symmetry_analyzer import PointSetSymmetryAnalyzer
from pointset_symmetry_viewer import PointSetSymmetryViewer


class TestPointSetSymmetryAnalyzer_CreateBisectorLine(unittest.TestCase):
    def test_1_vertical(self):
        """
        Test 1: Bisector from two vertical points
        """
        a = Point2D(0,0)
        b = Point2D(0,2)
        barycenter = (a + b)
        barycenter.r /= 2.0

        line = PointSetSymmetryAnalyzer.create_bisector_line(a, b, barycenter)
        unittest.TestCase.assertTrue(self, abs(line.a) < 0.000001)

    def test_2_horizontal(self):
        """
        Test 2: Bisector from two horizontal points
        """
        a = Point2D(0,0)
        b = Point2D(2,0)
        barycenter = (a + b)
        barycenter.r /= 2.0

        line = PointSetSymmetryAnalyzer.create_bisector_line(a, b, barycenter)
        unittest.TestCase.assertTrue(self, abs(line.a - math.pi/2) < 0.000001)

    def test_3_various_angles(self):
        """
        Test 3: Bisector from two points oriented in various angles and
        different locations for the barycenter
        """
        a = Point2D(1,-1)
        b = Point2D(-5,5)
        barycenter = (a + b)
        barycenter.r /= 2.0
        line = PointSetSymmetryAnalyzer.create_bisector_line(a, b, barycenter)
        unittest.TestCase.assertTrue(self, abs(line.a - math.pi/4) < 0.000001)

        a = Point2D(1,1)
        b = Point2D(5,5)
        barycenter = (a + b)
        barycenter.r /= 2.0
        line = PointSetSymmetryAnalyzer.create_bisector_line(a, b, barycenter)
        unittest.TestCase.assertTrue(self, abs(line.a - 3*math.pi/4) < 0.000001)

        a = Point2D(1,1)
        b = Point2D(5,5)
        barycenter = Point2D(1,5)
        line = PointSetSymmetryAnalyzer.create_bisector_line(a, b, barycenter)
        unittest.TestCase.assertTrue(self, abs(line.a - 3*math.pi/4) < 0.000001)

        a = Point2D(1,1)
        b = Point2D(5,5)
        barycenter = Point2D(5,1)
        line = PointSetSymmetryAnalyzer.create_bisector_line(a, b, barycenter)
        unittest.TestCase.assertTrue(self, abs(line.a + math.pi/4) < 0.000001)


class TestPointSetSymmetryAnalyzer_FindSymmetry(unittest.TestCase):
    def test_1_two_points_graphs(self):
        """
        Test 1: Two sets: Each with 2 points and 2 symmetry lines
        """
        s = PointSet("./tests/data/test_001_2_points.csv")
        symmetry_directions, symmetry_lines_points = PointSetSymmetryAnalyzer.find_symmetry(s)
        PointSetSymmetryViewer.plot(s, symmetry_lines_points, "tests/results/fig00A0")

        unittest.TestCase.assertEqual(self, len(symmetry_directions), 2)
        unittest.TestCase.assertEqual(self, symmetry_directions, ['90.0','0.0'])

        s = PointSet("./tests/data/test_002_2_points.csv")
        symmetry_directions, symmetry_lines_points = PointSetSymmetryAnalyzer.find_symmetry(s)
        PointSetSymmetryViewer.plot(s, symmetry_lines_points, "tests/results/fig00A1")

        unittest.TestCase.assertEqual(self, len(symmetry_directions), 2)
        unittest.TestCase.assertEqual(self, symmetry_directions, ['0.0','90.0'])

    def test_2_simple(self):
        """
        Test 2: Simple case, 1 symmetry line
        """
        s = PointSet("./tests/data/simple_test.csv")
        symmetry_directions, symmetry_lines_points = PointSetSymmetryAnalyzer.find_symmetry(s)
        PointSetSymmetryViewer.plot(s, symmetry_lines_points, "tests/results/fig00A2")
        unittest.TestCase.assertEqual(self, len(symmetry_directions), 1, )
        unittest.TestCase.assertEqual(self, symmetry_directions, ['135.0'])

    def test_3_polygon(self):
        """
        Test 3: small file (1K points), 8 symmetry lines
        """
        s = PointSet("./tests/data/symmetric_polygon_points.csv")
        symmetry_directions, symmetry_lines_points = PointSetSymmetryAnalyzer.find_symmetry(s)
        PointSetSymmetryViewer.plot(s, symmetry_lines_points, "tests/results/fig00A3", False)
        unittest.TestCase.assertEqual(self, len(symmetry_directions),  8)
        unittest.TestCase.assertEqual(self, symmetry_directions, ['0.0', '90.0', '135.0', '45.0', '157.5', '67.5', '22.5', '112.5'])

    def test_4_large_rotations(self):
        """
        Test 4: Large file (100K points), 100 symmetry lines
        """
        s = PointSet("./tests/data/test_file_large_100k.csv")
        symmetry_directions, symmetry_lines_points = PointSetSymmetryAnalyzer.find_symmetry(s)
        PointSetSymmetryViewer.plot(s, symmetry_lines_points, "tests/results/fig00A4", False)
        unittest.TestCase.assertEqual(self, len(symmetry_directions), 100)
        unittest.TestCase.assertEqual(
            self, 
            symmetry_directions,
            ['0.0', '7.2', '176.4', '3.6', '21.6', '169.2', '14.4', '25.2', '162.0', '18.0', '10.8', '57.6', '151.2', '50.4', '165.6', '61.2', '144.0', '54.0', '158.4', '36.0', '68.4', '129.6', '43.2', '32.4', '75.6', '115.2', '39.6', '46.8', '172.8', '28.8', '122.4', '133.2', '108.0', '126.0', '140.4', '93.6', '104.4', '147.6', '79.2', '111.6', '118.8', '136.8', '72.0', '86.4', '97.2', '90.0', '82.8', '100.8', '64.8', '154.8', '178.2', '12.6', '171.0', '5.4', '41.4', '156.6', '27.0', '48.6', '142.2', '34.2', '19.8', '113.4', '120.6', '99.0', '149.4', '106.2', '135.0', '70.2', '77.4', '84.6', '63.0', '91.8', '163.8', '55.8', '127.8', '1.8', '167.4', '16.2', '153.0', '73.8', '124.2', '45.0', '88.2', '95.4', '59.4', '30.6', '37.8', '52.2', '9.0', '109.8', '23.4', '81.0', '131.4', '145.8', '160.2', '117.0', '174.6', '138.6', '102.6', '66.6']
            )
        
    def test_5_large_complex(self):
        """
        Test 5: Large file (500k points), multiple polygons: No symmetry
        """
        s = PointSet("./tests/data/polygon_points_500k.csv")
        symmetry_directions, symmetry_lines_points = PointSetSymmetryAnalyzer.find_symmetry(s)
        PointSetSymmetryViewer.plot(s, symmetry_lines_points, "tests/results/fig00A5", False)
        unittest.TestCase.assertEqual(self, len(symmetry_directions),  0)


if __name__ == '__main__':
    unittest.main()

