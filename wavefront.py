# wavefront.py
import numpy as np

class WavefrontOBJ:
    def __init__( self, default_mtl='default_mtl' ):
        self.path      = None               # path of loaded object
        self.mtllibs   = []                 # .mtl files references via mtllib
        self.mtls      = [ default_mtl ]    # materials referenced
        self.mtlid     = []                 # indices into self.mtls for each polygon
        self.vertices  = []                 # vertices as an Nx3 or Nx6 array (per vtx colors)
        self.normals   = []                 # normals
        self.texcoords = []                 # texture coordinates
        self.polygons  = []                 # M*Nv*3 array, Nv=# of vertices, stored as\ vid,tid,nid (-1 for N/A)

    def only_coordinates( self ):
        V=np.zeros( ( len( self.vertices ), 3 ), np.float64 )
        for i in range(len(self.vertices)):
            V[i][0]= self.vertices[i][0]
            V[i][1]= self.vertices[i][1]
            V[i][2]= self.vertices[i][2]
        return V

    def only_faces( self ):   
        all_faces=[]
        for f in self.polygons:
            face=[]
            for indices in f:
                face.append( indices[0] )
            all_faces.append( face )
        return all_faces
    
    def get_coord( self, index ):
        return self.vertices[index]
    
    ### return boundary vertices
    def boundary_vertices( self ):
        bdry_v= set()
        darts = {}
        faces = self.only_faces()
        for f in faces:
            for i in range( len(f) ):
                if ( f[i] in darts ):
                    darts[ f[ i ] ].append( f[ (i+1)%len(f) ] )
                else:
                    darts[ f[ i ] ] = [ f[ (i+1)%len(f) ] ]
        for i, i_list in darts.items():
            for j in i_list:
                j_list = darts[ j ]
                if ( not i in j_list ):
                    bdry_v.add( i )
                    bdry_v.add( j )
        return bdry_v
    
    ### return boundary edges
    def boundary_edges( self ):
        bdry_e= set()
        darts = {}
        faces = self.only_faces()
        for f in faces:
            for i in range( len(f) ):
                if ( f[i] in darts ):
                    darts[ f[ i ] ].append( f[ (i+1)%len(f) ] )
                else:
                    darts[ f[ i ] ] = [ f[ (i+1)%len(f) ] ]
        for i, i_list in darts.items():
            for j in i_list:
                j_list = darts[ j ]
                if ( not i in j_list ):
                    bdry_e.add( (j,i) )
        return bdry_e
    
    ### return boundary edges
    def numpy_boundary_edges( self ):
        edges    = self.boundary_edges()
        np_edges = np.zeros( ( len(edges), 2 ), np.int32 )
        k        = 0;
        for e in edges:
            np_edges[k][0]=e[0]
            np_edges[k][1]=e[1]
            k = k+1
        return np_edges
    
    def ordered_boundary( self ):
        edges    = self.boundary_edges()
        if len(edges)==0:
            return []
        d        = {}
        first = -1
        for e in edges:
            d[ e[0] ] = e[1]
            if first == -1:
                first = e[ 0 ]
        list_e = [first]
        cur   = d[ first ]
        while cur != first:
            list_e.append( cur )
            cur = d[ cur ]
        return list_e
    
    def getAllEdges( self ):
        darts = {}
        faces = self.only_faces()
        for f in faces:
            for i in range( len(f) ):
                if ( f[i] in darts ):
                    darts[ f[ i ] ].append( f[ (i+1)%len(f) ] )
                else:
                    darts[ f[ i ] ] = [ f[ (i+1)%len(f) ] ]
        return darts
    
    def getAllEdgesOfVertex( self, v ):
        allEdges = self.getAllEdges()
        return allEdges[ v ]
    
def load_obj( filename: str, default_mtl='default_mtl', triangulate=False ) -> WavefrontOBJ:
    """Reads a .obj file from disk and returns a WavefrontOBJ instance

    Handles only very rudimentary reading and contains no error handling!

    Does not handle:
        - relative indexing
        - subobjects or groups
        - lines, splines, beziers, etc.
    """
    # parses a vertex record as either vid, vid/tid, vid//nid or vid/tid/nid
    # and returns a 3-tuple where unparsed values are replaced with -1
    def parse_vertex( vstr ):
        vals = vstr.split('/')
        vid = int(vals[0])-1
        tid = int(vals[1])-1 if len(vals) > 1 and vals[1] else -1
        nid = int(vals[2])-1 if len(vals) > 2 else -1
        return (vid,tid,nid)

    with open( filename, 'r' ) as objf:
        obj = WavefrontOBJ(default_mtl=default_mtl)
        obj.path = filename
        cur_mat = obj.mtls.index(default_mtl)
        for line in objf:
            toks = line.split()
            if not toks:
                continue
            if toks[0] == 'v':
                obj.vertices.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'vn':
                obj.normals.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'vt':
                obj.texcoords.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'f':
                poly = [ parse_vertex(vstr) for vstr in toks[1:] ]
                if triangulate:
                    for i in range(2,len(poly)):
                        obj.mtlid.append( cur_mat )
                        obj.polygons.append( (poly[0], poly[i-1], poly[i] ) )
                else:
                    obj.mtlid.append(cur_mat)
                    obj.polygons.append( poly )
            elif toks[0] == 'mtllib':
                obj.mtllibs.append( toks[1] )
            elif toks[0] == 'usemtl':
                if toks[1] not in obj.mtls:
                    obj.mtls.append(toks[1])
                cur_mat = obj.mtls.index( toks[1] )
        return obj

def save_obj( obj: WavefrontOBJ, filename: str ):
    """Saves a WavefrontOBJ object to a file
    Warning: Contains no error checking!
    """
    with open( filename, 'w' ) as ofile:
        for mlib in obj.mtllibs:
            ofile.write('mtllib {}\n'.format(mlib))
        for vtx in obj.vertices:
            ofile.write('v '+' '.join(['{}'.format(v) for v in vtx])+'\n')
        for tex in obj.texcoords:
            ofile.write('vt '+' '.join(['{}'.format(vt) for vt in tex])+'\n')
        for nrm in obj.normals:
            ofile.write('vn '+' '.join(['{}'.format(vn) for vn in nrm])+'\n')
        if not obj.mtlid:
            obj.mtlid = [-1] * len(obj.polygons)
        poly_idx = np.argsort( np.array( obj.mtlid ) )
        cur_mat = -1
        for pid in poly_idx:
            if obj.mtlid[pid] != cur_mat:                
                cur_mat = obj.mtlid[pid]
                ofile.write('usemtl {}\n'.format(obj.mtls[cur_mat]))
            pstr = 'f '
            for v in obj.polygons[pid]:
                # UGLY!
                vstr = '{}/{}/{} '.format(v[0]+1,v[1]+1 if v[1] >= 0 else 'X', v[2]+1 if v[2] >= 0 else 'X' )
                vstr = vstr.replace('/X/','//').replace('/X ', ' ')
                pstr += vstr
            ofile.write( pstr+'\n')



    
    


