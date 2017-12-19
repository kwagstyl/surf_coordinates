import numpy as np
import os
from cortex.polyutils import Surface
from perpendicular_path import perpendicular_scalar_func
import io_mesh as io
from neighbours import get_neighbours

surf_io=io.load_mesh_geometry('icbm_avg_mid_sym_mc_left_hires.obj')
surf = Surface(surf_io['coords'], surf_io['faces'])


atlas=np.loadtxt('icbm_avg_mid_sym_mc_atlas_left.txt')
lobule=np.loadtxt('lobule.txt')
medial=(atlas==0).astype(int)
medial[lobule==1]=1
mask=np.where(medial==1)[0]
dists=surf.geodesic_distance(mask,m=5)

max_start=np.argmax(dists)
#np.savetxt('dists.txt',dists)	

inv_dists=surf.geodesic_distance(max_start,m=5)
filtered=inv_dists.copy()
filtered[medial==0]=500
#np.savetxt('invdists.txt',inv_dists)
#filtered=filtered*0
#filtered[max_start]=1
#np.savetxt('start.txt',filtered)

start_vert=np.argmax(dists)
end_vert=np.argmin(filtered)
#print end_vert
end_vert=51203

perp=perpendicular_scalar_func(inv_dists,surf,start_vert, end_vert,mask)
back_perp=perpendicular_scalar_func(perp,surf,start_vert, end_vert,mask)

np.savetxt('radial.txt',back_perp)

grid_p=(perp%5)<1
grid_d=(back_perp%5)<1
combi_grid=grid_p.astype(int)*1+grid_d.astype(int)*2

np.savetxt('rotational.txt',perp)
np.savetxt('grid.txt',combi_grid)






