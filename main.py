import polyscope as ps
import numpy as	np
from wavefront import *

ps.init()
obj = load_obj( 'feline_half.obj')
ps_mesh = ps.register_surface_mesh("spot", obj.only_coordinates(), obj.only_faces() )

# `verts` is a Nx3 numpy array of vertex positions
# `faces` is a Fx3 array of indices, or a nested list
# verts=np.array([[1.,0.,0.],[0.,1.,0.],[-1.,0.,0.],[0.,-1.,0.],[0.,0.,1.]])
# faces=[[0,1,2,3],[1,0,4],[2,1,4],[3,2,4],[0,3,4]]
#ps.register_surface_mesh("my mesh", verts, faces )
# bdry  = obj.numpy_boundary_edges()
# ps_net= ps.register_curve_network("boundary", obj.only_coordinates(), bdry )
L = obj.ordered_boundary()
print(L)

ps.show()