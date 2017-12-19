# surf_coordinates
Welcome to surf_coordinates:
2D surface-based coordinate system based on geodesic distances

Brainhack Leipzig project started by Alex Huth (https://github.com/alexhuth) and Konrad Wagstyl to create a 2D coordinate system where each vertex is uniquely described by 2 values, and close values mean close coordinates. Thanks also to Hannah Spitzer for the discussions that inspired the project.

Coordinates are calculated as follows:
Calculate the vertex at the maximum geodesic distance from the medial wall.
A geodesic path is then calculated from this point to the medial wall to set the "international date line" for a rotational axis.
The rotational axis is calculated as a scalar field whose gradient is orthogonal to the original geodesic distance map.
The radial axis is the the scalar field whose gradient is orthogonal to the rotational axis.

In summary it provides 2 scalar fields whose gradients are orthogonal, providing a 2D coordinate system.

Required packages:
io_mesh.py from laminar python https://github.com/kwagstyl/laminar_python/blob/master/io_mesh.py

pycortex: https://github.com/gallantlab/pycortex/
you should clone from github then checkout the branch `glrework-merged` and run `python setup.py install`


Once installed just run:
python calculate_coordinates.py

Flatmaps can be explored in the Flatmap.ipynb

