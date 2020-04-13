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
            outstr += "[ " + "(" + str(self._q[left].getValue()) + str(self._q[left].getIndex()) + ")" + ", "
            left = 2*left+1
        outstr += "[ " + "(" + str(self._q[0].getValue()) + str(self._q[0].getIndex()) + ")" +"]" + ", "
        while right <= len(self._q)-1:
            outstr += "(" + str(self._q[right].getValue()) + str(self._q[right].getIndex()) + ")"+ " ]" + ", "
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
            return self._bubbleUp(curr)
            
    def min(self):
        return self._q[0]
    
    def remove_min(self):
        min = self._q[0]
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
        e = self._q[currindex]
        key = e.getKey()
        parent = currindex // 2 
        if key < self._q[parent].getIndex():
            self._bubbleUp(currindex)
        else:
            self._bubbleDown(currindex)

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
    pq = APQHeap()
    pq.add(4,"h")
    print(pq)
    pq.add(3,"g")
    print(pq)
    pq.add(6,"d")
    print(pq)
    pq.add(5,"W")
    print(pq)
    pq.add(9,"s")
    pq.add(8,"e")
    pq.add(2,"q")
    pq.add(12,"n")
    pq.add(2,"i")
    print(pq)
    print(pq.min())
    print(pq.remove_min())
    print(pq)