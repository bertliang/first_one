"""An implementation of the Multiset ADT.
  A class of MultiSet which is a collection of object, like regular set
  but it can contain duplicate elements. If you still interesting in multiset, 
  take a loot at:
        http://en.wikipedia.org/wiki/Multiset

  Authors: liangz10
  """


from skiplist import SkipList

    
class MultiSet(object):
    """ A class of MultiSet which is a collection of object, like regular set
        but it can contain duplicate elements. It uses SkipList to implement.
    """
    
    def __init__(self):
        '''(MultiSet)-> Nonetype
        Initialize a MultiSet.
        '''
        self.sk = SkipList()
        
        
    def __contains__(self, data):
        '''(MultiSet, object)-> bool
        Return True when the MultiSet contains data, otherwise return False
        '''
        return (data in self.sk)       
                
    def count(self, data):
        '''(Multiset, object)-> int
        Return the number of occurrences of data in the MultiSet.
        '''
        return self.sk.count(data)
        
    def insert(self, data):
        '''(MultiSet, object) -> Nonetype
        Add element to MultiSet in None descending order.
        ex: {1,3,4,6,8}
        '''
        self.sk.insert(data)
    
    def __repr__(self):
        '''(MultiSet)-> str
        Return a string that represent the MultiSet. 
        the orders is not matters.
        '''
        res = repr(self.sk)
        res = "MultiSet([" + res + "])"
        return res
    
    def remove(self, data):
        '''(MultiSet, object)-> Nonetype
        Remove the object from MultiSet, if it not in MultiSet, do nothing.
        '''
        self.sk.remove(data)   
            
    def clear(self):
        '''(MultiSet)->Nonetype
        Remove all the elements from MultiSet.
        '''
        self.sk.clear()
    
    def __len__(self):
        '''(MultiSet)->int
        Retunr the lenght of MultiSet.
        '''
        return len(self.sk)
    
    def __eq__(self, other):
        '''(MultiSet, MultiSet)->bool
        Return True when multiset are the same as self MultiSet, 
        the same elements and same occurences times.
        otherwise return False
        '''
        if type(self) != type(other):
            return False        
        return (self.sk == other.sk)
        
    def __le__(self, other):
        '''(MultiSet, MultiSet) -> bool
        Return True when the self is the subset of multiset.
        otherwise return False
        '''
        if type(self) != type(other):
            return False
        return (self.sk <= other.sk)
        
    def __sub__(self, other):
        '''(MultiSet, MultiSet) -> MultiSet
        Return a new multiset that contains every element 
        that belongs to multiset s1 but not to multiset s2;
        in others word is the difference between self and multiset,
        which is self - multiset
        '''
        if type(self) == type(other):
            res = MultiSet()
            for i in self.sk:
                num1 = self.count(i)
                num2 = other.count(i)
                num3 = res.count(i)
                if num1 - num2- num3 > 0:
                    res.insert(i)
            return res
    
    def __isub__(self, other):
        '''(MultiSet, MultiSet) -> MultiSet
        Update self so that remove every element in other is remove from 
        self, which is self -= multiset
        '''
        if type(self) == type(other):
            if len(self) != 0:
                for i in other.sk:
                    if i in self:
                        self.remove(i)
            return self
        
    
    def __add__(self, other):
        '''(MultiSet, MultiSet) -> MultiSet
        return a new MultiSet which contains all the elements in self and
        multiset.
        '''
        if type(self) == type(other):
            res = MultiSet()
            if len(self) !=0:
                for i in self.sk: 
                    res.insert(i)
            if len(other) !=0:
                for i in other.sk:
                    res.insert(i)
            return res
    
    def __iadd__(self, other):
        '''(MultiSet, MultiSet) -> MultiSet
        update self which all the elements in other multiset are adding to self.
        '''
        if type(self) == type(other):
            if len(other) !=0:
                for i in other.sk:
                    self.insert(i)
            return self
    
    def __and__(self, other):
        '''(MultiSet, MultiSet) -> MultiSet
        return a new multiset that contains the elements belong to both self
        and other. which is meaned the intersection of self and multiset.
        '''
        if type(self) == type(other):
            res = MultiSet()
            temp = self
            if len(other) != 0 and len(temp) != 0:
                for i in other.sk:
                    if temp.__contains__(i):
                        res.insert(i)
                        temp.remove(i)
            return res
    
    def __iand__(self, other):
        '''(MultiSet, MultiSet) -> MultiSet
        Update self so that it contians only the common of self and other.
        '''
        if type(self) == type(other):
            self = self.__and__(other)
            return self
    
    def isdisjoint(self, other):
        '''(MultiSet, MultiSet) -> MultiSet
        Return True if self have no element in common of other.
        '''
        if type(self) == type(other):
            res = self.__and__(other)
            if len(res) != 0:
                return False
        return True
        
        
if __name__ == "__main__":
    a=MultiSet()
    a.insert(1)
    a.insert(3)
    a.insert(2)
    a.insert(4)
    a.insert(3)
    a.remove(4)
    #a.remove(1)
    #a.remove(2)
    #a.remove(3)
    print(a.__contains__(1))
    print(a.__contains__(4))
    print(a)
    #print(a.__repr__())
    #b=MultiSet()
    #c=MultiSet()
    #d=MultiSet()
    #b.insert(1)
    #b.insert(3)
    #b.insert(4)
    #b.insert(3)
    
    #print(b)
    #print(a.__sub__(b))
    #print(a)
    #print(a.__and__(b))
    #print(c.__eq__(d))
    #print(a.__eq__(b))
    #b.insert(4)
    #print(b.__eq__(a))
    #b.insert(3)
    #print(b)
    #print(b.len())
    #print(a.__le__(b))
    #c=MultiSet()
    #print(c.__le__(b))
    #print(a.count(1))
    #print(a.count(3))
    #print(a.len())
    #print(a._index(2))
    #a.remove(2)
    #print(a)
    #print(a.len())
    #a.clear()
    #print(a)
    #print(a.len())