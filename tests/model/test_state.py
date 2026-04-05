import unittest
from model.state import State
from model.piece import Piece
from model.placement import Placement
from model.layer import Layer

class TestState(unittest.TestCase):
    def setUp(self):
        # El ancho y largo parecen estar invertidos en tu lógica previa de tests, 
        # asegúrate de que Layer(ancho, largo) coincida con tus p_points.
        layer = Layer(6, 11) 
        self.state = State(layer, [])

    def test_consecutive_placements(self):
        # First piece (2x3)
        p1 = Piece(2, 3, False)
        pl1 = Placement(p1, (0, 0))
        self.state = self.state.commit_placement(pl1)

        # Check first placement
        p_points = self.state.get_p_points()
        self.assertIn((2, 0), p_points)
        self.assertIn((0, 3), p_points)
        self.assertEqual(len(p_points), 2) 
        
        # Second piece (2x2)
        p2 = Piece(2, 2, False)
        pl2 = Placement(p2, (2, 0))
        self.state = self.state.commit_placement(pl2)
        
        # Check second placement
        p_points = self.state.get_p_points()
        self.assertIn((4, 0), p_points)
        self.assertIn((2, 2), p_points)
        self.assertIn((0, 3), p_points)
        self.assertEqual(len(p_points), 3)

        # Third piece (2x4)
        p3 = Piece(2, 4, False)
        pl3 = Placement(p3, (4, 0))
        self.state = self.state.commit_placement(pl3)

        # Check third placement
        p_points = self.state.get_p_points()
        self.assertIn((2, 2), p_points)
        self.assertIn((0, 3), p_points)
        self.assertEqual(len(p_points), 2) 

        # Fourth piece (2x1)
        p4 = Piece(2, 1, False)
        pl4 = Placement(p4, (2, 2))
        self.state = self.state.commit_placement(pl4)
        
        # Check fourth placement
        p_points = self.state.get_p_points()
        self.assertIn((0, 3), p_points)
        self.assertEqual(len(p_points), 1) 

        # Fifth piece (4x1)
        p5 = Piece(4, 1, False)
        pl5 = Placement(p5, (0, 3))
        self.state = self.state.commit_placement(pl5)

        # Check fifth placement
        p_points = self.state.get_p_points()
        self.assertIn((0, 4), p_points)
        self.assertEqual(len(p_points), 1) 

        # Sixth piece (1x1)
        p6 = Piece(1, 1, False)
        pl6 = Placement(p6, (0, 4))
        self.state = self.state.commit_placement(pl6)

        # Check sixth placement
        p_points = self.state.get_p_points()
        self.assertIn((1, 4), p_points)
        self.assertIn((0, 5), p_points)
        self.assertEqual(len(p_points), 2) 

        # Seventh piece (4x1)
        p7 = Piece(4, 1, False)
        pl7 = Placement(p7, (0, 5))
        self.state = self.state.commit_placement(pl7)

        # Check seventh placement
        p_points = self.state.get_p_points()
        self.assertIn((1, 4), p_points)
        self.assertIn((0, 6), p_points)
        self.assertEqual(len(p_points), 2) 

        # Eighth piece (5x1)
        p8 = Piece(5, 1, False)
        pl8 = Placement(p8, (1, 4))
        self.state = self.state.commit_placement(pl8)

        # Check eighth placement
        p_points = self.state.get_p_points()
        self.assertIn((0, 6), p_points)
        self.assertEqual(len(p_points), 1) 

        # Ninth piece (2x2)
        p9 = Piece(2, 2, False)
        pl9 = Placement(p9, (0, 6))
        self.state = self.state.commit_placement(pl9)

        # Check ninth placement
        p_points = self.state.get_p_points()
        self.assertIn((0, 8), p_points)
        self.assertIn((2, 6), p_points)
        self.assertEqual(len(p_points), 2) 

        # Tenth piece (2x3)
        p10 = Piece(2, 3, False)
        pl10 = Placement(p10, (2, 6))
        self.state = self.state.commit_placement(pl10)

        # Check tenth placement
        p_points = self.state.get_p_points()
        self.assertIn((0, 8), p_points)
        self.assertEqual(len(p_points), 1) 

        # Eleventh piece (3x2 rotated)
        p11 = Piece(3, 2, True)
        pl11 = Placement(p11, (0, 8))
        self.state = self.state.commit_placement(pl11)

        # Check eleventh placement
        p_points = self.state.get_p_points()
        self.assertEqual(len(p_points), 0) 

        # Check num_packed
        self.assertEqual(self.state.get_num_packed(), 11) 
        # Check packed_value
        self.assertEqual(self.state.get_packed_value(), 50) 
    
    def test_is_feasible(self):
        p = Piece(4, 4, False)
        pl = Placement(p, (0, 0))
        self.assertTrue(self.state.is_feasible(pl))
        
if __name__ == '__main__':
    unittest.main()