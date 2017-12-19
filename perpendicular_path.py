import numpy as np
import cortex
from cortex.polyutils import Surface


def perpendicular_scalar_func(sfunc, surf, origin, antipode, mask):
    sfunc_grad = surf.surface_gradient(sfunc, at_verts=False)
    normals = surf.face_normals
    grad_perps = np.cross(sfunc_grad, normals)
    #norm_grad_perps = grad_perps / np.sqrt((grad_perps ** 2).sum(1))
    norm_grad_perps = np.nan_to_num(grad_perps.T / np.sqrt((grad_perps ** 2).sum(1))).T

    # compute integrated divergence
    X = norm_grad_perps
    c32, c13, c21 = surf._cot_edge
    x1 = 0.5 * (c32 * X).sum(1)
    x2 = 0.5 * (c13 * X).sum(1)
    x3 = 0.5 * (c21 * X).sum(1)

    conn1, conn2, conn3 = surf._polyconn
    divx = conn1.dot(x1) + conn2.dot(x2) + conn3.dot(x3)

    # create a surface with a cut
    print("about to cut path")
    cut_path = np.array(surf.geodesic_path(origin, antipode,m=5))
    cut_path = np.union1d(cut_path, mask)
    #noncut_polys = np.array([p for p in surf.polys if ])
    good_polys = ~np.any(np.in1d(surf.polys, cut_path).reshape(surf.polys.shape), 1)

    cut_surf = Surface(surf.pts, surf.polys[good_polys])
    # run the geodesic distance code to generate laplace solver (lol)
    cut_surf.geodesic_distance([0])
    print('2')
    cconn1, cconn2, cconn3 = cut_surf._polyconn
    divx_cut = cconn1.dot(x1[good_polys]) + cconn2.dot(x2[good_polys]) + cconn3.dot(x3[good_polys])

    # integrate to find fxn whose gradient is norm_grad_perps
    print('3')
    part_perp_func = cut_surf._nLC_solvers[1.0](divx_cut[cut_surf._goodrows])
    perp_func = np.zeros_like(sfunc)
    perp_func[cut_surf._goodrows] = part_perp_func

    return perp_func


