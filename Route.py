""" Sample solutions for Lab 04.
    Implements the graph as a map of (vertex,edge-map) pairs.
"""
class Vertex:
    """ A Vertex in a graph. """
    
    def __init__(self, element):
        """ Create a vertex, with data element. """
        self._element = element
    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)
    def __lt__(self, v):
        return self._element < v.element()
    def element(self):
        """ Return the data for the vertex. """
        return self._element
    
class Edge:
    """ An edge in a graph.
        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """
    
    def __init__(self, v, w, element):
        """ Create an edge between vertice v and w, with label element.
            element can be an arbitrarily complex structure.
        """
        self._vertices = (v,w)
        self._element = element 
    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                   + str(self._vertices[1]) + ' : '
                   + str(self._element) + ')')
    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices
    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]
    def end(self):
        """ Return the second vertex in the ordered. pair. """
        return self._vertices[1]
    def opposite(self, v):
        """ Return the opposite vertex to v in this edge. """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None
    def element(self):
        """ Return the data element for this edge. """
        return self._element
class RouteGraph:
    """ Represent a simple graph.
        This version maintains only undirected graphs, and assumes no
        self loops.
    """
    
    
    
    
    
    
    def __init__(self):
        """ Create an initial empty graph. """
        self._in = dict()
        self._out = dict()
        self._gps = dict()
        self._elt = dict()
        self._vert = dict()
    def __str__(self):
        """ Return a string representation of the graph. """
        if len(self._elt) < 100:
            hstr = ('|V| = ' + str(self.num_vertices())
                    + '; |E| = ' + str(self.num_edges()))
            vstr = '\nVertices: '
            for v in self._out:
                vstr += str(v) + '-'
            edges = self.edges()
            estr = '\nEdges: '
            for e in edges:
                estr += str(e) + ' '
            return hstr + vstr + estr
        else:
            return "Graph too big to print out!"
    
    
    
    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._out)
    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._out:
            num += len(self._out[v])    
        return num //2     
                           
    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._out]
    def get_vertex_by_label(self, element):
        """ get the first vertex that matches element. """
        if element in self._elt:
            return self._elt[element]
        return None 
    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._out:
            for w in self._out[v]:
                
                if self._out[v][w].start() == v:
                    edgelist.append(self._out[v][w])
        return edgelist
    def get_edges(self, v):
        """ Return a list of all edges incident on v. """
        edgelist = []
        if v in self._out:
            for w in self._out[v]:
                edgelist.append(self._out[v][w])
            for q in self._in[v]:
                edgelist.append(self._in[v][q])
            return edgelist
        return None
    def get_edge(self, v, w):
        """ Return the edge between v and w, or None. """
        if (self._out != None
                         and v in self._out
                         and w in self._out[v]):
            return self._out[v][w]
        return None
    def degree(self, v):
        """ Return the degree of vertex v. """
        return len(self._out[v])
    
    
    
    def add_vertex(self, element):
        """ Add a new vertex with data element.
            If there is already a vertex with the same data element,
            this will create another vertex instance.
        """
        v = Vertex(element)
        self._out[v] = dict()
        self._in[v] = dict()
        self._elt[element] = v 
        self._vert[v] = element
        return v
    def add_GPS(self, element, longi, lat):
        """Adds the vertex to a dictionaire as key and its longitude and latitude as value"""
        self._gps[element] = (lat, longi)
    def add_vertex_if_new(self, element):
        """ Add and rdddeturn a vertex with element, if not already in graph.
            Checks for equality between the elements. If there is special
            meaning to parts of the element (e.g. element is a tuple, with an
            'id' in cell 0), then this method may create multiple vertices with
            the same 'id' if any other parts of element are different.
            To ensure vertices are unique for individual parts of element,
            separate methods need to be written.
        """
        if self._elt[element]:
            return self._elt[element]
        return self.add_vertex(element)
    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.
            If either v or w are not vertices in the graph, does not add, and
            returns None.
            
            If an edge already exists between v and w, this will
            replace the previous edge.
        """
        if not v in self._out or not w in self._out:
            return None
        e = Edge(v, w, element)
        self._out[v][w] = e
        self._out[w][v] = e 
        self._in[w][v] = e
        self._in[v][w] = e 
        return e
    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements. """
        for (v,w) in elist:
            self.add_edge(v,w,None)
    
    
        
    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._out:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv     
    def depthfirstsearch(self, v):
        'runs depth first search and calls a private function to do the work'
        marked = {v:None}
        self._depthfirstsearch(v, marked)
        return marked
    def _depthfirstsearch(self, v, marked):
        'for all the edges that vertex v has '
        for e in self.get_edges(v):
            'find the vertex at the other end of the edge'
            w = e.opposite(v)
            'if it hasnt been marked yet'
            if w not in marked:
                'add it to the dictionary with the edge as the value'
                marked[w] = e
                'recursovely call it on that vertex '
                self._depthfirstsearch(w, marked)  
    def _print_breadth(self, marked):
        'loop through the items in the marked dictionary'
        for item in marked:
            'print them formatted'
            print("{ %s : %s }," % (item, marked[item][0]))
        return
    def breadthfirstsearch(self, v):
        'add the root vertex to the dictionary'
        marked = {v:(None, 0)}
        'this is the first level and the only element in this level'
        level = [v]
        'so far we are 0 steps away from the root vertex'
        steps = 0
        'while this level has something in it'
        while len(level) > 0:
            'create a list for the next level'
            nextlevel = []
            'we are now 1 step/hop away'
            steps += 1 
            'for vertex in the currrnet level'
            for w in level:
                'for all the edges the vertex has'
                for e in self.get_edges(w):
                    'find the vertex at the other side of the edge'
                    x = e.opposite(w)
                    'if it aint marked'
                    if x not in marked:
                        'mark it and add the number of hops and its parnet vertex to the dictionary'
                        marked[x] = (w, steps)
                        'put it into the next level list '
                        nextlevel.append(x)
            'reassign the level variable'
            level = nextlevel
        return marked
        
    
    def centralPrint(self, tree, end):
        root = None
        curr = end
        outstr = ""
        'for a key in the tree'
        for item in tree:
            'if the value of that key is None'
            if tree[item] == None:
                'its the root for the tree'
                root == item
        'for all the vertices in the tree'
        for vert in tree:
            'create a list for them'
            lst = []
            'while the current vertex isnt the root vertex'
            while curr != root:
                'add it to the path list'
                lst.append(curr)
                'set the new current to be the original currents parent vertex'
                curr = tree[curr][0]
            'looping reverse through the list'    
            for i in range(len(lst)-1,-1,-1):
                'if its the last item in the list path'
                if i == 0:
                    'dont add the double line at the end'
                    outstr += str(lst[i]) +"(" + str(tree[lst[i]][1]) + ")"
                else:
                    'else do add the double line '
                    outstr += str(lst[i]) +"(" + str(tree[lst[i]][1]) + ")" + "--"
            return outstr 
            
    def dijkstra_all_apq_heap(self, s, heap = True):
        """ Return table of shortest paths from s to all reachable vertices.
            The dictionary has vertices as keys, and as values it has the
            for each v the cost of the path to get to v from s, and the last
            vertex visited before v in the path.
            This version uses an adaptable priority queue using a heap by
            default, or uses an unsorted list.
        """
        closed = {}     
        locations = {}  
        if heap:
            pq = APQHeap()  
        else:
            pq = APQUnsorted()  
        pred = {}          
        pred[s] = None
        locations[s] = pq.add(0,s)        
        while pq.length() > 0:
            cv, mcov = pq.remove_min()   
           
            del locations[mcov]
            closed[mcov] = (cv, pred[mcov]) 
            for e in self.get_edges(mcov):
                w = e.opposite(mcov)
                
                if w not in closed:
                    weight = e.element()
                    newcost = cv + weight
                    if w not in locations:
                        pred[w] = mcov
                        
                        locations[w] = pq.add(newcost,w)
                    elif newcost < pq.get_key(locations[w]):    
                        pred[w] = mcov
                        
                        pq.update_key(locations[w], newcost)
                    else:
                        
                        None
                else:
                    None
                    
        return closed
    def sp(self, v, w):
        tree =  self.dijkstra_all_apq_heap(v)
        curr = tree[w]
        
        path = [] 
        while curr[1] != None:
            
            path.append(curr)
            
            curr = tree[curr[1]]
            
           
        path.reverse()
        self.printOut(path)
        return path 
        
    def printOut(self, lst):
        print("type\tlatitude\tlongitude\telement\t\tcost")
        for elt in lst:
            
            element = elt[1]
            cost = elt[0]
           
            longi = self._gps[element][1]
            latitude = self._gps[element][0]
            print("w\t%s\t%s\t%s\t%s" % (latitude, longi,element, cost))
    def graphreader(self, filename):
            """ Read and return the route map in filename. """
            file = open(filename, 'r')
            entry = file.readline() 
            num = 0
            while entry == 'Node\n':
                num += 1
                nodeid = int(file.readline().split()[1])
                line = file.readline().split()
                longi = float(line[1])
                longi = round(longi, 6)
                lat = float(line[2])
                lat = round(lat, 6)
                vertex = self.add_vertex(nodeid)
                self.add_GPS(vertex, lat, longi)
                entry = file.readline() 
            
            num = 0
            while entry == 'Edge\n':
                num += 1
                source = int(file.readline().split()[1])
                sv = self.get_vertex_by_label(source)
                target = int(file.readline().split()[1])
                
                tv = self.get_vertex_by_label(target)
                length = float(file.readline().split()[1]) 
                cost = float(file.readline().split()[1])
                edge = self.add_edge(sv, tv, cost)
                oneway = bool(file.readline().split()[1])
                
                entry = file.readline() 
            
            return self
    
class Element:
    """ A key, value and index. """
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i
    def __eq__(self, other):
        return self._key == other._key
    def __lt__(self, other):
        return self._key < other._key
    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None
    
    def getValue(self):
        return self._value
    
    def getKey(self):
        return self._key
    
    def getIndex(self):
        return self._index
    
    def setKey(self, newkey):
        self._key = newkey
    
    def setIndex(self, newindex):
        self._index = newindex
class APQHeap:
    def __init__(self):
        self._q = []
    
    def __str__(self):
        outstr = "{ "
        left = 2*0+1
        right = 2*0 + 2
        print("Length of q : ",len(self._q))
        print(left)
        print(right)
        while left <= len(self._q)-1:
            outstr += "(" + str(self._q[left].getValue()) + str(self._q[left].getIndex()) + ")" + ", "
            left = 2*left+1
        outstr += "(" + str(self._q[0].getValue()) + str(self._q[0].getIndex()) + ")" + ", "
        while right <= len(self._q)-1:
            outstr += "(" + str(self._q[right].getValue()) + str(self._q[right].getIndex()) + ")" + ", "
            right = 2*right+2
        outstr += "}"
        return outstr 
    def add(self, c, v):
        e = Element(c,v,None)
        if len(self._q) == 0:
            e.setIndex(0)
            self._q.append(e)
        else:
            self._q.append(e)
            curr = len(self._q) -1
            e.setIndex(curr)
            self._bubbleUp(curr)
        return e 
        
    
    def get_key(self, elt):
        return elt.getKey()
            
    def min(self):
        return self._q[0]
    
    def remove_min(self):
        
        min = (self._q[0].getKey(), self._q[0].getValue())
        self._q[0], self._q[len(self._q)-1] = self._q[len(self._q)-1], self._q[0]
        self._q.pop(len(self._q)-1)
        d = 0
        self._bubbleDown( d)
        return min
    
    def is_empty(self):
        if len(self._q) == 0:
            return True
        else:
            return False
    def length(self):
        return len(self._q)
    def update_key(self, element, newkey):
        element.setKey(newkey)
        currindex = element.getIndex()
        self._rebalance(currindex)
        return element 
    
    def _rebalance(self, currindex):
        if currindex < len(self._q) -1:
            e = self._q[currindex]
            key = e.getKey()
            parent = currindex // 2 
            if key < self._q[parent].getIndex():
                self._bubbleUp(currindex)
            else:
                self._bubbleDown(currindex)
        
        return self._q
    def _bubbleDown(self, currindex):
        while True:
            leftchild = 2*currindex + 1
            rightchild = leftchild + 1
            if rightchild < len(self._q) -1 and leftchild < len(self._q) - 2:
                if self._q[leftchild].getKey() < self._q[currindex].getKey() and self._q[leftchild].getKey() < self._q[rightchild].getKey():
                    self._swap(currindex, leftchild)
                    currindex = 2*currindex + 1
                elif self._q[rightchild].getKey() < self._q[currindex].getKey() and self._q[rightchild].getKey() < self._q[leftchild].getKey():
                    self._swap(currindex, rightchild)
                    currindex = 2*currindex+2
                else:
                    return self._q[currindex]
            elif leftchild < len(self._q)-1:
                self._swap(currindex, leftchild)
                return 
            else:
                return 
    
    def _swap(self, element1, element2):
        newindex = self._q[element1].getIndex()
        self._q[element1].setIndex(self._q[element2].getIndex())
        self._q[element2].setIndex(newindex)
        self._q[element1], self._q[element2] = self._q[element2], self._q[element1]
        self._rebalance(element2)
        return 
    def _bubbleUp(self, current ):
        parent = current//2
        while self._q[parent].getKey() > self._q[current].getKey():
            self._swap(current, parent)
            current = parent 
            parent = current//2
        return self._q
    def remove(self,element):
        index = element.getIndex()
        last = len(self._q) -1 
        self._swap(index, last)
            
if __name__ == "__main__":
    
    
    
    
    routemap = RouteGraph()
    routemap.graphreader('corkCityData.txt')
    ids = {}
    ids['wgb'] = 1669466540
    ids['turnerscross'] = 348809726
    ids['neptune'] = 1147697924
    ids['cuh'] = 860206013
    ids['oldoak'] = 358357
    ids['gaol'] = 3777201945
    ids['mahonpoint'] = 330068634
    sourcestr = 'wgb'
    deststr='neptune'
    source = routemap.get_vertex_by_label(ids[sourcestr])    
    dest = routemap.get_vertex_by_label(ids[deststr])
    routemap.sp(source,dest)
   
    
