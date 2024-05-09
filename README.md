## POINT SET SYMMETRY FINDER (NB-HW)

### AUTHOR
Rachid Ounit, Ph.D.

### DATE
05/07/2024

### DESCRIPTION
This project contains the Python scripts to analyze a point set and find
its symmetry lines.

### VERSION
0.1.1

### COMPONENTS:
This project is composed of modules:

**constants**: Containing constants values used by the algorithm and helper functions.
**file_data_importer**: Containing the code for importing raw data of the point set.
**point**: Data model for the 2D point.
**pointset**: Data model for the point set.
**pointset_symmetry_analyzer**: The core class for analyzing the point set and find its
symmetry lines.
**pointset_symmetry_viewer**: A class for visualizing results, written for
testing / debugging purposes. A more advanced class can be designed for presenting 
results.
**tests**: Folder containing data and results used for testing.

### REQUIREMENTS & VERSION
Python 3.8 or earlier is required. In addition, the required python packages are:
```
matplotlib
point2d
typing_extensions
```
A requirements.txt file is provided, please use it:
```
pip3 install -r ./requirements.txt
```

### EXECUTION / TESTS: 
An example of execution of the code for several unit tests is provided. Simply run:
```
python3 -m unittest tests.py
```
