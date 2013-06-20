from datetime import datetime
from layers.utils import *
from unittest import TestCase

class LayerUtilsTest(TestCase):
    
    def test_convert_to_python(self):
        self.assertEqual("example", convert_to_python("example"))
        self.assertEqual(1, convert_to_python(1))
        self.assertEqual((1,2.0,8l), convert_to_python((1,2.0,8l)))
        self.assertEqual(datetime(2001,10,11),
                convert_to_python('2001-10-11'))
        self.assertEqual(["test", "20020304", datetime(2008,7,20)],
                convert_to_python(['test', '20020304', '2008-07-20']))
        self.assertEqual({'some': 3, 'then': datetime(1999,10,21)},
                convert_to_python({'some': 3, 'then': '1999-10-21'}))
