"""An implementation of the Splay Tree.

   A splay tree is a self-adjusting binary search tree with the additional 
   property that recently accessed elements are quick to access again. 
   It performs basic operations such as insertion, search and delete 
   in O(log n) amortized time.
   Reference: http://en.wikipedia.org/wiki/Splay_tree
   
   Authors: liangz10,  April 2013.
"""


class EmptyException(Exception):
    """ A sub class exception of EmptyException, raise it when
        remove from empty tree or remove object not in tree.
    """
    pass


class UnCompareExeption(Exception):
    """ A subclass exception of WrongTypeException, raise it when insert and
        remove from not compariable type of data.
    """
    pass


class BSTNode(object):
    '''A Node in a SplayTree'''
    
    def __init__(self, data, left=None, right=None, down=None):
        '''(BSTNode, object[, BSTNode, BSTNode]) -> NoneType
        A new BSTNode with key data and left and right and down children.
        is_leftchild, is_rightchild, parent.
        '''
        # set a BSTNode initial 
        self.data = data
        self.left = left
        self.right = right
        self.down = down # down link store duplicate element
        self.is_leftchild = False
        self.is_rightchild = False
        self.parent = None
        
    def set_child(self, child):
        '''(BSTNode) -> NoneType
        set BSTNode to a leftchild or right child or None.
        '''
        # set a node to whether is a left child or right child or not
        if child == "left":
            self.is_rightchild = False
            self.is_leftchild = True
        elif child == "right":
            self.is_leftchild = False
            self.is_rightchild = True
        else: # child == None
            self.is_leftchild = False
            self.is_rightchild = False
    
    def zig(self):
        '''(BTNode) -> BTNode
        perform a right-rotation on the node's left child to be the root, 
        and return the root of the re-structured tree 
        Requirement: that x is a non-empty node.
        '''
        # set parent, grandparent, x, and do a right-rotaion of x
        parent, grandparent = self, self.parent
        x = parent.left              # x is left subtree of root
        b, x.right = x.right, parent # b is right subtree of x
        parent.left, parent.parent = b, x
        if b: # check if the right subtree of x have or not, update b
            b.parent = parent
            b.set_child("left")      
        x.parent = grandparent
        x.is_leftchild, x.is_rightchild = False, False
        # if grandparent not None we have to update grandparent and x
        if grandparent: 
            if parent.is_leftchild:
                grandparent.left = x
                x.set_child("left")
            else:
                grandparent.right = x
                x.set_child("right")
        parent.set_child("right") # update parenet as well
        return x
                    
    def zag(self):
        '''(BTNode) -> BTNode
        perform a left-rotation on the node's left child, 
        and return the root of the re-structured tree 
        Requirement: that x is a non-empty node.
        '''        
        # set parent, grandparent, x, and do a right-rotaion of x
        parent, grandparent = self, self.parent
        x = parent.right
        a, x.left = x.left, parent
        parent.right, x.parent = a, grandparent
        if a:# check if the left subtree of x have or not, update a
            a.parent = parent
            a.set_child("right") 
        parent.parent = x
        x.is_leftchild, x.is_rightchild  = False, False
        if grandparent: # if grandparent not None, we have update x as parent
            if parent.is_leftchild:
                grandparent.left = x
                x.set_child("left")
            else:
                grandparent.right = x
                x.set_child("right")          
        parent.set_child("left") # update parent to left subtree
        return x
            
    def splay(self):
        '''(BTNode) -> BTNode
        perform a splay on the node which set the node to the root.
        if parent is root, current is right child, do zag
        if parent is root, current is left child, do zig
        if both of parent and current are right child, do zag-zag
        if both of parent and current are left child, do zig-zig
        if parent is left child and current is right child, do zag-zig
        if parent is right child and current is left child, do zig-zag
        and return the root of the re-structured tree 
        Requirement: root is a non-empty node.
        '''             
        current = self
        # loop over uptil current to the top of the root
        while current.parent:
            # no grandparent, do single rotate: zig or zag
            if not current.parent.parent:
                if current.is_leftchild:
                    current = current.parent.zig()
                else:
                    current = current.parent.zag()
            else: # parent.parent not None
                parent = current.parent
                grandparent = parent.parent
                # both of parent and current is leftchild, do zig_zig rotate
                if (parent.is_leftchild and current.is_leftchild):
                    parent = grandparent.zig()
                    current = parent.zig()
                # both of parent and current is rightchild, do zag_zag rotate
                elif (parent.is_rightchild and current.is_rightchild):                   
                    parent = grandparent.zag()
                    current = parent.zag()
                # parent is leftchild current is rightchild, do zag_zig
                elif parent.is_leftchild and current.is_rightchild: 
                    current = parent.zag()
                    current = current.parent.zig()
                else: # parent is right, current is leftchild, do zig_zag
                    current = parent.zig()
                    current = current.parent.zag()                       
        return current  
    
                    
class SplayTree(object):
    """A Splaytree, which is self-balanced binary search tree.
    """
    
    def __init__(self, init_values = []):
        '''(SplayTree [, list of object]) -> NoneType
        REQ: objects in init_values must all be comparable
        '''
        self.root = None
        #add all the initital elements, this is just done to make it easier
        #to build a tree for testing
        self._len = 0
        for element in init_values:
            self.insert(element)
            
    def _type_check(compare_data, data):
        '''(object, object)->bool
        Return True if two object if a comparalbe object.
        otherwise return Flase.
        '''
        try:
            data < compare_data # try to compared two object
        except TypeError:
            return False        
        except:
            return False
        else:
            return True    
    
    def __contains__(self, search_value):
        '''(SplayTree , object) -> bool
        Return True is search_value in self, otherwise return False
        perform: "object in my_tree"
        '''        
        return self.search(search_value) # return search method below
        
    def search(self, search_value):
        '''(SplayTree, object) -> bool
        Returns true iff the search_value is present in the splay tree, 
        searches using the standard splay tree search algorithm.
        '''
        if not self.root: # empty tree, return False
            return False
        if not SplayTree._type_check(self.root.data, search_value):
            return False  # not compariable data, return False
        # splay the tree, then check the root data of the tree
        node = SplayTree._search_helper(self.root, search_value)
        self.root = node.splay()
        if self.root.data == search_value: 
            return True
        return False
    
    def _search_helper(root, search_value):
        '''(BTNode, object) -> NoneType
        helper function in search and insert method
        if search value in tree, return that node
        if not, return the last visited node
        REQ: the root not empty!
        '''
        # no subtree, return it
        if not root.left and not root.right:
            return root
        # set parent and current to root.parent and root
        parent, current = root.parent, root
        while current:
            # we found the duplicate data, return its node
            if(current.data == search_value):
                return current
            elif(current.data > search_value):
                parent, current = current, current.left
            else: #(current.data < search_value):
                parent, current = current, current.right
        # current is None now, means search_value not in root,
        # so we return its parent.
        return parent
    
    def __repr__(self):
        '''(Splaytree) -> str
        print out the splaytee. 
        '''
        return SplayTree._print_helper(self.root, "")
    
    def _print_helper(root, indentation):
        '''(BTNode) -> str
        helper function to print out the splaytee. 
        '''        
        #Base Case: empty tree
        if(root == None):
            return ""
        #RD: return my data, along with my lef & right subtree's data
        else:
            ret = SplayTree._print_helper(root.right, indentation + "  ")
            ret += indentation + str(root.data)
            ret += SplayTree._print_helper(root.down, indentation + "-")
            ret += "\n"
            ret += SplayTree._print_helper(root.left, indentation + "  ")
            return ret
       
    def _help_insert(root, insert_obj):
        """(SplayTree, object) -> Splaytree
        Help Insert item into this Splaytree, splay the new node to the root.
        if item not in list, insert as a normal BST.
        if item already in list, insert to the down subtree of that node
           and splay the parent node to root.
        """
        # get the position to insert the node.
        current = SplayTree._search_helper(root, insert_obj)
        node = BSTNode(insert_obj)
        node.parent = current
        # insert a new node to left subtree
        if insert_obj < current.data:
            node.set_child("left")                   
            current.left = node
            root = node.splay() # splay this node to the root
        # insert_obj > current.data, 
        # linked new node's right subtreee to current's right subtree,
        # linked current right subtree's parent to the new node             
        elif insert_obj > current.data:
            node.set_child("right")
            current.right = node
            root = node.splay() # splay this node to the root
        # insert_obj == current.data, duplicate data, we store it to down
        # subtree        
        else:
            node.down = current.down
            if current.down:
                current.down.parent = node
            current.down = node
            root = current.splay() # splay this node's parent to the root
        return root
                
    def insert(self, insert_obj):
        '''(Splaytree, object) -> NoneType
        Insert insert_obj into the tree, splay the new node to the root.
        REQ: insert_obj must be comparable with all of the objects in the tree
        '''
        if not self.root: # empty tree
            # check insert obj, if it not comparable to itself, raise exception
            if not SplayTree._type_check(insert_obj, insert_obj):
                raise UnCompareExeption('Uncomparable object')
            else: # it is comparable, insert it
                self.root = BSTNode(insert_obj)
                self._len += 1
        # not an empty tree, check comparable of root.data and insert obj
        elif not SplayTree._type_check(self.root.data, insert_obj):
            raise UnCompareExeption('Uncomparable object')
        else: # then insert new node
            self.root = SplayTree._help_insert(self.root, insert_obj)
            self._len += 1
            
    def remove(self, delete_obj):
        '''(Splaytree, object) -> NoneType
        Remove delete_obj from this tree if it's present.
        first we check if the delete_obj in self or not,
        if the delete_obj in root, we already splay it to the root,
           then replace root.data with the largest data in right subtree
           then delete that node, and splay it's parent to the root
        if delete_obj not in root, we already splay it as in search method.
        '''
        # check if it is an empty tree
        if self.root:
            # check delete_obj is compareable to data in root
            if not SplayTree._type_check(self.root.data, delete_obj):
                raise UnCompareExeption('Uncomparable object')
            else: # search the node to delete
                node = SplayTree._search_helper(self.root, delete_obj)
                # delete_obj not in tree, splay the last visit node to root
                if node.data != delete_obj: 
                    self.root = node.splay()
                # delete_obj is in tree, and have duplicate element,
                # delete the down subtree, splay the node to the root
                elif node.down:
                    if node.down.down:
                        node.down.down.parent = node
                    node.down = node.down.down
                    self.root = node.splay()
                    self._len -= 1
                # delete_obj in tree, and unique, see helper delete below
                else:
                    self.root = SplayTree._delete_helper(node, delete_obj)
                    self._len -= 1
        else: # empty tree, raise romove from empty tree exception
            raise EmptyException("try to Remove from empty tree")
            
    def _delete_helper(root, delete_obj):
        '''(BSTNode, object) -> BSTNode
        Ensure that delete_obj in the tree rooted at root, 
        and return the root of the resulting tree after splay the parent of the 
        delete node.
        REQUIRE: delete_obj is in tree, and the root.data is delete_obj.
        '''
        # no subtree, easy, delete it
        if not root.left and not root.right:
            if not root.parent:   # only one element in tree
                return None
            else:
                if root.is_leftchild:
                    root.parent.left = None
                else:
                    root.parent.right = None
                root = root.parent.splay() 
        # no right subtree, easy, return left left subtree
        elif not root.right:
            if not root.parent: # element in root
                root.left.parent = None
                root = root.left
                root.is_leftchild = False
            else:
                root.left.parent = root.parent
                root.parent.left = root.left
                root = root.parent.splay()
        # no left subtree, easy, return right right subtree    
        elif not root.left:
            if not root.parent: # element in root
                root.right.parent = None
                root = root.right 
                root.is_rightchild = False
            else:
                root.right.parent = root.parent
                root.parent.right = root.right
                root = root.parent.splay()
        # have left and right subtree, hard..... replace the smallest element 
        # in right subtree, then go to delete that node
        else:
            smallest = SplayTree._smallest(root.right)
            root.data = smallest
            if root.right.data == smallest: # right subtree has not left subtree
                if root.right.right:
                    root.right.right.parent = root
                root.right = root.right.right
                root = root.splay()
            else:
                parent, current = root, root.right
                while current.left: # go to the delete node
                    parent, current = current, current.left
                if current.right: # delete node has right rubtree, update it
                    parent.left = current.right
                    parent.left.parent = parent
                    parent.left.set_child('left')
                else: # delete node has no child
                    parent.left = None
                root = parent.splay()
        return root
    
    def __len__(self):
        '''(SplayTree)-> int
        return totol number of element in tree
        '''
        return self._len
    
    def count(self, data):
        '''(SplayTree)-> int
        return total number occurrence of data in tree.
        '''
        # check if the data in tree or not, 
        if data in self:
            return SplayTree._help_count(self.root)
        return 0
    
    def _help_count(root):
        '''(BTNode)-> int
        Return total number of of down subtree in the root.
        REQUIRE: down subtree carry the same element in root.
        '''
        if not root:
            return 0
        else:
            return 1 + SplayTree._help_count(root.down)
            
    def _smallest(root):
        '''(BSTNode) -> int
        Return the largest key in the tree rooted at root.
        Precondition: root is not None
        '''
        # base case, no right subtree, return its data
        if (root.left == None): 
            return root.data
        else: # recurive go to right subtree
            return SplayTree._smallest(root.left)
        
    def max(self):
        '''(SplayTree) -> object
        returns the maximum element in the splay tree, 
        the tree is splayed as it would be in a search for the maximum element
        '''
        if not self.root:
            raise EmptyException("try to max from empty tree")
        else:
            root = self.root 
            while root.right: # keep going right of tree
                root = root.right
            root = root.splay() # splay it t the root
            self.root = root
            return root.data #return max num
    
    def min(self):
        '''(SplayTree) -> object
        returns the minimum element in the splay tree, 
        the tree is splayed as it would be in a search for the minimum element
        '''
        if not self.root:
            raise EmptyException("try to min from empty tree")
        else:
            root = self.root
            while root.left: # keep going left of the tree
                root = root.left
            root = root.splay() # spaly it to the root
            self.root = root 
            return root.data # return the min number
    
    def traverse(self):
        '''(SplayTree)-> list
        performs an in-order traversal of the splay tree, 
        Returns a list of the elements present in the tree in sorted order, 
        does not splay any elements
        '''
        return SplayTree._help_traverse(self.root)
    
    def _help_traverse(root):
        '''(BTNode) -> list
        helper function of traverse, return list of elements present in the 
        tree in sorted order, performs an in-order traversal of the tree.
        '''
        if not root:  # base case, return empty list
            return []
        else: # keep going left and right, return in-order traversal of tree.
            left = SplayTree._help_traverse(root.left)
            down = SplayTree._help_traverse(root.down)
            right = SplayTree._help_traverse(root.right)
            return  left + [root.data] + down + right

    def __iter__(self):
        '''(SplayTree)-> NoneType
         an iterator for the tree, allows you to use code like: 
         for(element in my_splaytree)
        '''
        l = SplayTree._help_traverse(self.root) # get a list of element of tree
        for i in l:       
            yield i  # yield each element in the list.
