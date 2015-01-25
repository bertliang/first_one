"""A Unittest of SplayTree.
Using Unittset to test the SplayTree ADT data structure.

Author: liangz10, April 2013.
"""


from splaytree import SplayTree, EmptyException, UnCompareExeption
import unittest


class Test_Empty_SplayTree(unittest.TestCase):
    """ A class Test empty SplayTree.
    """
    
    def setUp(self):
        ''' Setup test case each time. 
        '''
        self.test1 = SplayTree()
    
    def tearDown(self):
        ''' Reset test case to default
        '''
        self.test1 = None
    
    def test_emptptree_search(self):
        ''' test search in an empty tree.
        '''
        self.assertFalse(self.test1.search(2), "check search in empty tree")
        
    def test_emptyllist_max(self):
        ''' test max method in empty tree.
        '''        
        self.assertRaises(EmptyException, self.test1.max)
    
    def test_emptyllist_min(self):
        ''' test min method in empty tree.
        '''
        self.assertRaises(EmptyException, self.test1.min)
    
    def test_emptyllist_traverse(self):
        ''' test traverse method in empty tree.
        '''
        self.assertEqual(self.test1.traverse(), [], "traverse in empty tree")
    
    def test_emptyllist_remove(self):
        ''' test remove method in empty tree, raise EmptyException.
        '''
        self.assertRaises(EmptyException, self.test1.remove, 2)
        
    def test_emptyllist_insert(self):
        ''' test insert method in empty tree.
        '''
        self.test1.insert(5)
        self.assertEqual(self.test1.traverse(), [5], "insert in empty tree")
        
    def test_emptyllist_insert_2(self):
        ''' test insert an uncompare data in empty tree, 
            raise UnCompareExeption
        '''
        self.assertRaises(UnCompareExeption, self.test1.insert, {1:2})    
        
        
class Test_OneElement_SplayTree(unittest.TestCase):
    """ A class Test OneElement SplayTree.
    """
    
    def setUp(self):
        ''' Setup test case each time. 
        '''
        self.test1 = SplayTree([5])
    
    def tearDown(self):
        ''' Reset test case to default
        '''
        self.test1 = None
    
    def test_search(self):
        ''' test search in tree.
        '''
        self.assertFalse(self.test1.search(2), "check search in tree")
        self.assertTrue(self.test1.search(5), "check search in tree")
        
    def test_max(self):
        ''' test max method in tree.
        '''        
        self.assertEqual(self.test1.max(), 5, "max method in tree")
    
    def test_min(self):
        ''' test min method in tree.
        '''
        self.assertEqual(self.test1.min(), 5, "min method in tree")
    
    def test_traverse(self):
        ''' test traverse method in tree.
        '''
        self.assertEqual(self.test1.traverse(), [5], "traverse in tree")
    
    def test_remove_1(self):
        ''' test remove an element not in tree, does nothing.
        '''
        self.test1.remove(2)
        self.assertEqual(self.test1.traverse(), [5], "traverse in tree")
        
    def test_remove_2(self):
        ''' test remove an element in tree.
        '''
        self.test1.remove(5)
        self.assertEqual(self.test1.traverse(), [], "traverse in tree")
        
    def test_remove_3(self):
        ''' test remove an uncomareable element in tree, raise UncompareExption.
        '''
        self.assertRaises(UnCompareExeption, self.test1.remove, 'a')
    
    def test_insert(self):
        ''' test insert duplicate element in tree.
        '''
        self.test1.insert(5)
        self.assertEqual(self.test1.traverse(), [5,5], "insert in tree")
    
    def test_insert_2(self):
        ''' test insert different element in tree and splay to the root.
        '''
        self.test1.insert(7)
        self.assertEqual(self.test1.traverse(), [5,7], "insert in tree")
        self.assertEqual(self.test1.root.data, 7, "insert in tree")
                
    def test_insert_3(self):
        ''' test insert uncompareable element in tree.
        '''
        self.assertRaises(UnCompareExeption, self.test1.insert, 'a')
        
        
class Test_Multielement_SplayTree(unittest.TestCase):
    """ A class Test Multielement SplayTree.
    """
    
    def setUp(self):
        ''' Setup test case each time. 
        '''
        self.test1 = SplayTree([-2, -7, 15, 7, 12, 9, 5])
    
    def tearDown(self):
        ''' Reset test case to default
        '''
        self.test1 = None
    
    def test_search(self):
        ''' test search in tree.
        '''
        self.assertFalse(self.test1.search(2), "check search in tree")
        self.assertEqual(self.test1.root.data, -2, "insert in tree")
        self.assertTrue(self.test1.search(5), "check search in tree")
        self.assertEqual(self.test1.root.data, 5, "insert in tree")
        
    def test_max(self):
        ''' test max method in tree.
        '''        
        self.assertEqual(self.test1.max(), 15, "max method in tree")
        self.assertEqual(self.test1.root.data, 15, "insert in tree")
    
    def test_min(self):
        ''' test min method in tree.
        '''
        self.assertEqual(self.test1.min(), -7, "min method in tree")
        self.assertEqual(self.test1.root.data, -7, "insert in tree")
    
    def test_traverse(self):
        ''' test traverse method in tree.
        '''
        self.assertEqual(self.test1.traverse(), [-7, -2, 5, 7, 9, 12, 15]\
                         , "traverse in tree")
    
    def test_remove_1(self):
        ''' test remove an uncomareable element in tree, raise UncompareExption.
        '''
        self.assertRaises(UnCompareExeption, self.test1.remove, 'a')
        
    def test_remove_2(self):
        ''' test remove an element in tree.
        '''
        self.test1.remove(5)
        self.assertEqual(self.test1.traverse(), [-7, -2, 7, 9, 12, 15]\
                         , "traverse in tree")
        self.assertEqual(self.test1.root.data, 9, "insert in tree")
        
    def test_insert(self):
        ''' test insert duplicate element in tree.
        '''
        self.test1.insert(7)
        self.assertEqual(self.test1.traverse(), [-7, -2, 5, 7, 7, 9, 12, 15]\
                         , "traverse in tree")
        self.assertEqual(self.test1.root.data, 7, "insert in tree")
    
    def test_insert_2(self):
        ''' test insert different element in tree and splay to the root.
        '''
        self.test1.insert(10)
        self.assertEqual(self.test1.traverse(), [-7, -2, 5, 7, 9, 10, 12, 15]\
                         , "traverse in tree")
        self.assertEqual(self.test1.root.data, 10, "insert in tree")
                
    def test_insert_3(self):
        ''' test insert uncompareable element in tree.
        '''
        self.assertRaises(UnCompareExeption, self.test1.insert, 'a')
        
        
class Test_Multielement_Str_SplayTree(unittest.TestCase):
    """ A class Test Multielement SplayTree.
    """
    
    def setUp(self):
        ''' Setup test case each time. 
        '''
        self.test1 = SplayTree(['c', 'z', 'b', 'a', 'd', 's'])
    
    def tearDown(self):
        ''' Reset test case to default
        '''
        self.test1 = None
    
    def test_search(self):
        ''' test search in tree.
        '''
        self.assertFalse(self.test1.search(2), "check search in tree")
        self.assertTrue(self.test1.search('a'), "check search in tree")
        self.assertEqual(self.test1.root.data, 'a', "insert in tree")
        
    def test_max(self):
        ''' test max method in tree.
        '''        
        self.assertEqual(self.test1.max(), 'z', "max method in tree")
        self.assertEqual(self.test1.root.data, 'z', "insert in tree")
    
    def test_min(self):
        ''' test min method in tree.
        '''
        self.assertEqual(self.test1.min(), 'a', "min method in tree")
        self.assertEqual(self.test1.root.data, 'a', "insert in tree")
    
    def test_traverse(self):
        ''' test traverse method in tree.
        '''
        self.assertEqual(self.test1.traverse(), ['a', 'b', 'c', 'd', 's', 'z']\
                         , "traverse in tree")
    
    def test_remove_1(self):
        ''' test remove an uncomareable element in tree, raise UncompareExption.
        '''
        self.assertRaises(UnCompareExeption, self.test1.remove, 2)
        
    def test_remove_2(self):
        ''' test remove an element in tree.
        '''
        self.test1.remove('s')
        self.assertEqual(self.test1.traverse(), ['a', 'b', 'c', 'd', 'z']\
                         , "traverse in tree")
        self.assertEqual(self.test1.root.data, 'z', "insert in tree")
        
    def test_insert(self):
        ''' test insert duplicate element in tree.
        '''
        self.test1.insert('c')
        self.assertEqual(self.test1.traverse(), \
                         ['a', 'b', 'c', 'c', 'd', 's', 'z']\
                         , "traverse in tree")
        self.assertEqual(self.test1.root.data, 'c', "insert in tree")
    
    def test_insert_2(self):
        ''' test insert different element in tree and splay to the root.
        '''
        self.test1.insert('m')
        self.assertEqual(self.test1.traverse(),\
                         ['a', 'b', 'c', 'd', 'm', 's', 'z']\
                         , "traverse in tree")
        self.assertEqual(self.test1.root.data, 'm', "insert in tree")
                
    def test_insert_3(self):
        ''' test insert uncompareable element in tree.
        '''
        self.assertRaises(UnCompareExeption, self.test1.insert, 3)
        
          
if __name__ == "__main__":
    unittest.main(exit = False)