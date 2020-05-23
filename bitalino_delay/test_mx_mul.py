import unittest
from unittest import mock

import mx_mul
from unittest.mock import patch


class TestMatrixMultiplication(unittest.TestCase):

    @patch('builtins.input', side_effect=[1, 5])
    def test_matrix_size(self, mock_inputs):
        width, height = mx_mul.matrix_size('A')
        self.assertEqual(width, 1)
        self.assertEqual(height, 5)

    @patch('builtins.input', side_effect=[-5, 3])
    def test_matrix_size_2(self, mock_inputs):
        with self.assertRaises(SyntaxError):
            mx_mul.matrix_size('A')

    @patch('builtins.input', side_effect=[2, 0])
    def test_matrix_size_3(self, mock_inputs):
        with self.assertRaises(SyntaxError):
            mx_mul.matrix_size('A')

    @patch('builtins.input', side_effect=['1', '2 3'])
    def test_matrix_input(self, mock_inputs):
        with self.assertRaises(Exception):
            mx_mul.matrix_input('A', 2, 2)

    @patch('builtins.input', side_effect=['1 2 3', '2 -6 5'])
    def test_matrix_input_2(self, mock_inputs):
        self.assertEqual(mx_mul.matrix_input('A', 3, 2), [[1, 2, 3], [2, -6, 5]])

    @patch('builtins.input', side_effect=['1.1 2.01', '2 3', '0 0.5'])
    def test_matrix_input_3(self, mock_inputs):
        self.assertEqual(mx_mul.matrix_input('A', 2, 3), [[1.1, 2.01], [2, 3], [0, 0.5]])

    def test_multiplication(self):
        self.assertEqual(mx_mul.multiplication([[1, 2], [5, 3], [6, 7]], [[5], [1]]), [[7], [28], [37]])
        self.assertEqual(mx_mul.multiplication([[4, 5, 6, 0], [-5, 1, 0, 5]],
                                               [[7, 8, 9, -1, 0], [4, 5, 0, 1, -9], [4, 5, 6, 3, 2], [0, 0, 0, 0, 0]]),
                         [[72, 87, 72, 19, -33], [-31, -35, -45, 6, -9]])
        self.assertEqual(mx_mul.multiplication([[-5, 8], [6, 9]], [[1, -5], [0, 6]]), [[-5, 73], [6, 24]])
        self.assertEqual(mx_mul.multiplication([[0, 0]], [[0], [0]]), [[0]])


if __name__ == '__main__':
    unittest.main()
