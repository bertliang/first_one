"""A skip list data structure.
using a randomized linked list, stored object in orders.
structure that provides expected worst-case performance O(log n) 
for every operation.

Author: liangz10, February 2013.
"""

import random


class _Tail_Node(object):
    
    def __init__(self, data=None, down=None):
        self.data = data
        self.down = down
        self.link = None


class _Node(object):
    """A node in the skip list.
    """

    def __init__(self, data, link=None, down=None):
        """(_SkipNode, object, _SkipNode) -> NoneType
        Initialize this node to store data and have next node link.
        """
        self.data = data
        self.link = link
        self.down = down

class _SkipIter(object):  # "private" class because name starts with _
    """An iterator (allowing the use of for-loops) for skip lists.
    """

    def __init__(self, start):
        """(_SkipIter, _SkipNode) -> NoneType
        Initialize this iterator with node start, a header node that does not
        store an actual skip list element.
        """
        self.current = start

    def __iter__(self):
        """(_SkipIter) -> _SkipIter
        Return this iterator, as required for iterator objects.
        """
        return self

    def __next__(self):
        """(_SkipIter) -> object
        Return the next item for this iterator, if there is one. Raises
        StopIteration if this is none.
        """
        if not self.current.link:
            raise StopIteration()
        self.current = self.current.link
        return self.current.data
    
    
    

class SkipList(object):
    """A Skiplist stores elements in orders, using a randomized linked list
    structure that provides expected worst-case performance O(log n) 
    for every operation.
    """
    
    def __init__(self, container=[], pro=0.5):
        '''(SkipList)->Nonetype
        Initial the skip list to store data in contianer and probobility is 0.5.
        (default:create an empty skip list)
        '''
        self.tail = _Tail_Node()    
        self.head = _Node(None, self.tail) # first level doesn't store data
        self.height = 0 #create an empty list, so default height is 0
        self.pro = pro
        self.size = 0
        for item in container:
            self.insert(item)
    
    def _search(p, data):
        '''
        '''
        while p.link and p.link.data < data:
            p = p.link
        return p
            
    
    def insert(self, data):
        '''(SkipList,object)->Nonetype
        Insert data to the skiplist.
        '''
        level = self._level() #helper function, see below
        node = None
        #if there is no element in the skiplist, insert to the link of 
        #head.down, level plus one
        if self.head.down == None:
            self.head.down = _Node(None, _Node(data))
            self.height += 1
        #if level is greater than height, that mean we have to insert data to
        #the bottom from the list to the self.height, and also add the 
        #extra height to the skiplist.
        elif level > self.height:
            i = 0
            #first we add to the original height, from bottom to 
            #top and insert the data the the link
            #we add the extra height to the original skiplist
            #self.head.link is data, self.head.down is the original
            #skiplist
            p = self.head.down
            p = SkipList._help_insert(p, data,node)
            node = self._contains(data).link
            diff = level - self.height
            while i < diff:
                node = _Node(data, None, node)
                self.head.down = _Node(None, node, self.head.down)
                i += 1
                self.height += 1 #we have increase the self.height
        #if level small than height, we only need to add to the from bottom 
        #to that level, this time, we don't need to increase self.height
        else:
            #first we find the location to insert the node of data
            #see below
            p = self.search(data, self.height-level+1)
            p = SkipList._help_insert(p, data,node)
        self.size += 1
    
    def _help_insert(p, data, node):
        node = _Node(data)        
        while p.down:
            p = SkipList._search(p, data)
            node.link = p.link
            p.link = node
            node.down = _Node(data)
            node = node.down
            p = p.down
        p = SkipList._search(p, data)
        node.link = p.link
        p.link = node            
            
    def search(self, data, level):
        '''(SkipList, object) -> _Node
        return the bottom level of _Node in the skiplist either is p.data 
        samller than data or p == self.head or p.link == None
        '''
        i = 0
        p = self.head.down
        current = p
        while i < level:
            #we first find the node where node's data smaller thatn data
            p = SkipList._search(p, data) #helper function see above
            #this is what we return , could be self.head.down or p.link
            current = p
            #otherwise p will go down one level
            p = p.down
            i += 1
        return current
    
    def remove(self, data):
        '''(SkipList, object)-> SkipList
        Remove one occurrence of data in the skiplist.
        '''
        #first we check whether data in the skiplist or not, 
        #if not, do nothing, if yes, delete it from the bottom to the top
        #see helper function _contains below
        p = self._contains(data) 
        if p != None:
            #we want to know the difference of finding the data level and
            #self.height
            while p:
                #locate the position of the data
                #then delete it
                p = SkipList._search(p, data)
                p.link = p.link.link
                p = p.down
        #after delete it , if the top level does mot have any element, delete 
        #that level, and self.height will decrease
            self.size -= 1
            if len(self) == 0:
                self.clear()
            else:
                while self.head.down.link == None:
                    self.head.down = self.head.down.down
                    self.height -= 1 
    
    def _level(self):
        '''(SkipList)->int
        Return a random level which is samller than self.pro.
        (default: probability is 0.5, example: level start at 1,
        random numbers generated are 0.35, 0.08, 0.41, 0.7
        Then, the node storing will have 4 levels)
        '''
        level = 1        
        p = random.random()
        while p < self.pro:
            p = random.random()
            level += 1
        return level
    
    def _contains(self, data):
        '''(SkipList, object)-> int
        Return -1 if the data not in the skiplist,
        return a number of level from top to bottom of the data.
        '''
        p = self.head.down
        res = None
        #check search the data when level samller than self.height
        while p:
            #check search the p.link exist and p.link.data is samller than data.
            p = SkipList._search(p, data)
            #check the p.data is equal to data, if yes, return that level.
            #if not, p go down one level
            if p.link != None:
                if p.link.data == data:
                    res = p                
                    return res
            p = p.down
        return res
    
    def __len__(self):
        '''(SkipList)-> int
        return the length of the skiplist.
        '''
        return self.size
       
    def __contains__(self, data):
        '''(SkipList, object) -> bool
        return ture if the data in list, return False otherwise.
        '''
        p = self._contains(data)
        if p != None:
            return True
        return False
       
    def count(self, data):
        '''(SkipList, object)-> int
        Return the number of occurrences of data in the MultiSet.
        '''        
        count = 0
        if len(self) != 0:
            p = self.search(data, self.height)
            while p.link and p.link.data <= data:
                if p.link.data == data:
                    count += 1
                p = p.link
        return count
       
    def clear(self):
        '''(SkipList)->Nonetype
        Remove all the elements from MultiSet.
        '''        
        self.__init__()
       
    def __repr__(self):
        '''(SkipList)-> str
        Return a string that represent the MultiSet. 
        the orders is not matters.
        '''        
        res = ''        
        if len(self) != 0:
            p = self._bottom_level()
            res = SkipList._help_str(p.link)
            res = res[:-2]
        return res
       
    def _help_str(p):
        '''(Node) -> str
        Return a string representing a linked list of nodes starting at n
        '''        
        if p == None:
            return ''
        return repr(p.data)+', ' + SkipList._help_str(p.link)
    
    def _bottom_level(self):
        p = self.head
        while p.down:
            p = p.down
        return p
    
    def __iter__(self):
        """(SkipList) -> _SkipIter
        Return an iterator object over this skip list.
        """
        
        if len(self) == 0:
            return _SkipIter(self.head.link)
        else:
            p = self._bottom_level()
            return _SkipIter(p)
    
    def __eq__(self, other):
        '''(SkipList, SkipList)->bool
        Return True when SkipList are the same as other, 
        the same elements and same occurences times.
        otherwise return False
        '''
        if len(self)==0 and len(other)==0:
            return True
        elif len(self) != len(other):
            return False
        else:
            p = self._bottom_level()
            s = other._bottom_level()
            while p.link:
                if p.link.data != s.link.data:
                        return False
                else:
                        p = p.link
                        s = s.link
        return True
        
    def __le__(self, other):
        '''(SkipList, SkipList) -> bool
        Return True when the self SkipList is the subset of other SkipList.
        otherwise return False
        '''
        if len(self) != 0:
            if len(other) == 0:
                return False
            else:
                for i in self:
                    if self.count(i) > other.count(i):
                        return False
        return True     



if __name__ == "__main__":
    a=SkipList([1])
    b=SkipList([3])
    print(a==b)
    b=SkipList([1,1,1,3,4])
    print(b.count(1))
    a=SkipList([1,5,6,2,2,7])
    a.insert(2)
    a.insert(4)
    a.insert(56)
    a.insert(787)
    a.insert(48)
    a.insert(989)
    a.insert(-1)
    a.insert(100)
    print(a.count(2))
    print(len(a))
    a.remove(1)
    a.remove(2)
    print(a.count(2))
    a.remove(2)
    print(len(a))
    print(1 in a)
    a.insert(1)
    print(1 in a)
    print(len(a))
    print(a.count(2))
    print(a.count(0))
    print(a)
   
    