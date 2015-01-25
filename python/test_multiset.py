from multiset import MultiSet
import unittest


class Test_Empty_MultiSet(unittest.TestCase):
    """ A class Test empty multiset.
    """
    
    def setUp(self):
        """ Setup test case each time. 
        """
        self.test1 = MultiSet()
        self.test2 = MultiSet()
    
    def tearDown(self):
        """ Reset test case to default
        """
        self.test1 = None
        self.test2 = None
    
    def test_emptyllist(self):
        """ test __contains__, count, len, remove method in empty set.
        """
        self.assertFalse(2 in self.test1, "check contains method in empty set")
        self.assertEqual(self.test1.count(2), 0, "count method in empty set")
        self.assertEqual(len(self.test1), 0, "len method in empty set")
        self.assertEqual(self.test1.remove(1), None, "remove in empty set")
    
    def test_emptyllist_2(self):
        """test clear, repr method in empty set.
        """
        #check clear method in empty set
        self.test1.clear()
        res = "MultiSet([])"
        self.assertEqual(repr(self.test1), res, "repr method in empty set")
    
    def test_compare_method_emptyll(self):
        """ test __eq__, __le__ method in empty set.
        """
        self.assertTrue(self.test1 == self.test2, "__eq__ in two empty set")
        self.assertTrue(self.test1 <= self.test2, "__le__ in two empty set")
        
    def test_sub_method(self):
        """ test sub method in empty list.
        """
        self.assertEqual(len(self.test1 - self.test2), 0, \
                         "__sub__ in two empty set")
    def test_isub_method(self):
        """ test isub method in empty set.
        """
        self.test1 -= self.test2
        self.assertEqual(len(self.test1), 0, "__isub__ in two empty set")
    
    def test_add_method(self):
        """ test add method in empty set
        """        
        self.assertEqual(len(self.test1+self.test2), 0, "add in two empty set")
       
    def test_iadd_method(self):
        """ test iadd method in empty set.
        """        
        self.test1 += self.test2
        self.assertEqual(len(self.test1), 0, "iadd in two empty set")
        
    def test_and_method(self):
        """ test and method in empty set.
        """        
        self.assertEqual(len(self.test1&self.test2), 0, \
                         "and method in two empty set")
   
    def test_iand_method(self):
        """ test iand method in empty set.
        """        
        self.test1 &= self.test2
        self.assertEqual(len(self.test1), 0, "iand in two empty set")
    
    def test_isdisjoint_method(self):
        """ test isdisjoint method in empty set.
        """        
        self.assertTrue(self.test1.isdisjoint(self.test2), \
                        "isdisjoint in two empty set")


class Test_Oneelement_MultiSet(unittest.TestCase):
    """ A class test one element multiset.
    """
    
    def setUp(self):
        self.test1 = MultiSet()
        self.test1.insert(5)
        self.test2 = MultiSet()
        self.test2.insert(5)
        self.test3 = MultiSet()
        self.test3.insert(6)
        
    def tearDown(self):
        self.test1 = None
        self.test2 = None
        self.test3 = None
    
    def test_oneelement(self):
        """ test __contains__, count, len, remove insert 
            clear repr method in one element multiset.
        """
        self.assertTrue(self.test1.__contains__(5), \
                        "check contains method which the element in set")
        self.assertFalse(self.test1.__contains__(6), \
                        "check contains method which the element in set")        
        self.assertEqual(self.test1.count(5), 1, \
                         "count method which element in list")
        self.assertEqual(len(self.test1), 1, "len method when set has element")
        self.assertEqual(self.test1.__repr__(), "MultiSet([5])", \
                         "repr method when set has element")
        #check remove method
        self.test1.remove(5)
        self.assertFalse(self.test1.__contains__(5), \
                         "contains method which element not in set")
        self.assertEqual(self.test1.count(5), 0, \
                         "count method which element not in set")
        self.assertEqual(len(self.test1), 0)
        self.assertEqual(self.test1.__repr__(), "MultiSet([])", \
                         "repr method when set has no element")
        #check insert method and clear method
        self.test1.insert(1)
        self.test1.clear()
        self.assertEqual(self.test1.__repr__(), "MultiSet([])", \
                         "repr method when set has no element")
    
    def test_compare_method_emptyll(self):
        """ test __eq__, __le__ method.
        """
        self.assertTrue(self.test1 == self.test2, "__eq__ in two same set")
        self.assertFalse(self.test1 == self.test3, \
                         "__eq__ in two difference set")
        self.assertTrue(self.test1 <= self.test2, "__le__ in two same set")
        self.assertFalse(self.test1 == self.test3, \
                         "__le__ in two difference set")
    
    def test_sub_method(self):
        self.assertEqual(len(self.test1 - self.test2), 0)
        self.assertEqual(len(self.test3 - self.test2), 1)
    
    def test_isub_method(self):
        self.test1 -= self.test2
        self.assertEqual(len(self.test1), 0)
    
    def test_isub_method2(self):
        self.test1 -= self.test3
        self.assertEqual(len(self.test1), 1)
     
    def test_add_method(self):
        self.assertEqual(len(self.test1+self.test2), 2)
       
    def test_isadd_method(self):
        self.test1 += self.test2
        self.assertEqual(len(self.test1), 2)
    
    def test_and_method(self):
        self.assertEqual(len(self.test1&self.test2), 1)
    
    def test_and_method2(self):
        self.assertEqual(len(self.test1&self.test3), 0)
        self.assertEqual(len(self.test1), 1)
        
    def test_iand_method(self):
        self.test1 &= self.test2
        self.assertEqual(len(self.test1), 1)
    
    def test_iand_method2(self):
        self.test1 &= self.test3
        self.assertEqual(len(self.test1), 0)    
     
    def test_isdisjoint_method(self):
        self.assertTrue(self.test1.isdisjoint(self.test3))
    
    def test_isdisjoint_method2(self):
        self.assertFalse(self.test1.isdisjoint(self.test2))


class Test_Multielement_MultiSet(unittest.TestCase):
    
    def setUp(self):
        self.test1 = MultiSet()
        self.test1.insert(1)
        self.test1.insert(1)
        self.test1.insert(1)
        self.test1.insert(2)
        self.test1.insert(3)
        self.test2 = MultiSet()
        self.test2.insert(1)
        self.test2.insert(3)
        self.test3 = MultiSet()
        self.test3.insert(1)
        self.test3.insert(2)
        self.test3.insert(3)
        self.test4 = MultiSet()
        test = None
        
    def tearDown(self):
        self.test1 = None
        self.test2 = None
        self.test3 = None
        self.test4 = None
        test = None
    
    def test_element(self):
        self.assertTrue(self.test1.__contains__(1))
        self.assertFalse(self.test1.__contains__(5))
        self.assertEqual(self.test1.count(1), 3)
        self.assertEqual(len(self.test1), 5)
        self.assertEqual(self.test1.__repr__(), "MultiSet([1, 1, 1, 2, 3])")
        self.test1.remove(5)
        self.assertEqual(len(self.test1), 5)
        self.test1.remove(1)
        self.test1.remove(3)
        self.assertEqual(len(self.test1), 3)
        self.test1.clear()
        self.assertEqual(len(self.test1), 0)
        self.assertEqual(self.test1.__repr__(), "MultiSet([])")
   
    def test_compare_method_emptyll(self):
        self.assertFalse(self.test1 == self.test2)
        self.assertFalse(self.test1 <= self.test2)
        self.assertTrue(self.test2 <= self.test1)
        self.assertFalse(self.test1 <= self.test3)
        
    def test_sub_method(self):
        self.assertEqual(len(self.test1 - self.test2), 3)
        self.assertEqual(len(self.test2 - self.test1), 0)
    
    def test_isub_method(self):
        self.test1 -= self.test2
        self.assertEqual(len(self.test1), 3)
    
    def test_isub_method2(self):
        self.test2 -= self.test1
        self.assertEqual(len(self.test2), 0)
     
    def test_add_method(self):
        test = self.test1 + self.test2
        self.assertEqual(len(test), 7)
       
    def test_isadd_method(self):
        self.test1 += self.test2
        self.assertEqual(len(self.test1), 7)
    
    def test_and_method(self):
        self.assertEqual(len(self.test1&self.test2), 2)
    
    def test_iand_method(self):
        self.test1 &= self.test2
        self.assertEqual(len(self.test1), 2)
    
    def test_iand__method2(self):
        self.test1 &= self.test4
        self.assertEqual(len(self.test1), 0)
        
    def test_isdisjoint_method2(self):
        self.assertFalse(self.test1.isdisjoint(self.test2))


class Test_Multielement_Str_MultiSet(unittest.TestCase):
    
    def setUp(self):
        self.test1 = MultiSet()
        self.test1.insert('a')
        self.test1.insert('z')
        self.test1.insert('c')
        self.test2 = MultiSet()
        self.test2.insert('c')
        self.test2.insert('a')
        self.test2.insert('z')
        self.test2.insert('b')
        self.test2.insert('a')
        self.test2.insert('d')
        self.test3 = MultiSet()
        self.test3.insert('n')
        self.test3.insert('m')
        self.test4 = MultiSet()
                
    def tearDown(self):
        self.test1 = None
        self.test2 = None
        self.test3 = None
        self.test4 = None
    
    def test_element(self):
        self.assertTrue(self.test1.__contains__('a'))
        self.assertFalse(self.test1.__contains__('b'))
        self.assertEqual(self.test1.count('a'), 1)
        self.assertEqual(self.test2.count('a'), 2)
        self.assertEqual(len(self.test1), 3)
        self.assertEqual(len(self.test2), 6)
        self.assertEqual(self.test1.__repr__(), "MultiSet(['a', 'c', 'z'])")
        self.test1.remove('b')
        self.assertEqual(len(self.test1), 3)
        self.test1.remove('a')
        self.assertEqual(len(self.test1), 2)
        self.test1.clear()
        self.assertEqual(len(self.test1), 0)
        self.assertEqual(self.test1.__repr__(), "MultiSet([])")
    
    def test_compare_method_emptyll(self):
        self.assertFalse(self.test1 == self.test2)
        self.assertFalse(self.test3 <= self.test2)
        self.assertTrue(self.test1 <= self.test2)
    
    def test_compare_method_emptyll_2(self):
        self.assertFalse(self.test1 == self.test4)
        self.assertFalse(self.test1 <= self.test4)
        self.assertFalse(self.test3 <= self.test4)    
        
    def test_sub_method(self):
        self.assertEqual(len(self.test2 - self.test1), 3)
        self.assertEqual(len(self.test3 - self.test2), 2)
    
    def test_sub_method_2(self):
        self.assertEqual(len(self.test4 - self.test1), 0)
        self.assertEqual(len(self.test4 - self.test2), 0)    
    
    def test_isub_method(self):
        self.test2 -= self.test1
        self.assertEqual(len(self.test1), 3)
    
    def test_isub_method_2(self):
        self.test4 -= self.test1
        self.assertEqual(len(self.test4), 0)    
    
    def test_isub_method_3(self):
        self.test3 -= self.test2
        self.assertEqual(len(self.test3), 2)
    
    def test_add_method(self):
        self.assertEqual(len(self.test1+self.test2), 9)
        self.assertEqual(len(self.test3+self.test2), 8)
       
    def test_isadd_method(self):
        self.test1 += self.test2
        self.assertEqual(len(self.test1), 9)
    
    def test_and_method(self):
        self.assertEqual(len(self.test1&self.test2), 3)
        self.assertEqual(len(self.test3&self.test2), 0)
    
    def test_and_method_2(self):
        self.assertEqual(len(self.test1&self.test4), 0)
        self.assertEqual(len(self.test3&self.test4), 0)    
    
    def test_iand_method(self):
        self.test1 &= self.test2
        self.assertEqual(len(self.test1), 3)  
    
    def test_iand_method_2(self):
        self.test3 &= self.test2
        self.assertEqual(len(self.test3), 0)     
        
    def test_isdisjoint_method(self):
        self.assertFalse(self.test1.isdisjoint(self.test2))
        self.assertTrue(self.test3.isdisjoint(self.test2))
        self.assertTrue(self.test1.isdisjoint(self.test4))

if __name__ == "__main__":
    unittest.main(exit = False)