import unittest
from numpy.testing import assert_array_almost_equal
import numpy as np
from findiff.vector import Gradient, Divergence


class TestGradient(unittest.TestCase):

    def test_3d_gradient_on_scalar_func(self):
        axes, h, [X, Y, Z] = init_mesh(3, (50, 50, 50))
        f = np.sin(X) * np.sin(Y) * np.sin(Z)
        grad_f_ex = np.array([
          np.cos(X) * np.sin(Y) * np.sin(Z),
          np.sin(X) * np.cos(Y) * np.sin(Z),
          np.sin(X) * np.sin(Y) * np.cos(Z),
        ])
        grad = Gradient(h=h, acc=4)
        grad_f = grad(f)
        assert_array_almost_equal(grad_f, grad_f_ex)

    def test_3d_gradient_on_vector_func_should_fail(self):
        axes, h, [X, Y, Z] = init_mesh(3, (50, 50, 50))
        f = np.array([np.sin(X) * np.sin(Y) * np.sin(Z),
                      np.sin(X) * np.sin(Y) * np.sin(Z)
                     ])
        grad = Gradient(h=h, acc=4)
        self.assertRaises(ValueError, grad, f)


class TestDivergence(unittest.TestCase):

    def test_3d_divergence_on_vector_func(self):
        axes, h, [X, Y, Z] = init_mesh(3, (50, 50, 50))
        f = np.array([np.sin(X) * np.sin(Y) * np.sin(Z)] * 3)
        assert f.shape == (3, 50, 50, 50)
        div_f_ex = \
          np.cos(X) * np.sin(Y) * np.sin(Z) +\
          np.sin(X) * np.cos(Y) * np.sin(Z) +\
          np.sin(X) * np.sin(Y) * np.cos(Z)

        div = Divergence(h=h, acc=4)
        div_f = div(f)
        assert_array_almost_equal(div_f, div_f_ex)

    def test_3d_divergence_on_vector_func_of_wrong_dim(self):
        axes, h, [X, Y, Z] = init_mesh(3, (50, 50, 50))
        f = np.array([np.sin(X) * np.sin(Y) * np.sin(Z)] * 3)
        assert f.shape == (3, 50, 50, 50)
        div = Divergence(h=[1, 1], acc=4)
        self.assertRaises(ValueError, div, f)



def init_mesh(ndims, npoints):
    axes = [np.linspace(-1, 1, npoints[k]) for k in range(ndims)]
    h = [x[1] - x[0] for x in axes]
    mesh = np.meshgrid(*axes, indexing="ij")
    return axes, h, mesh


if __name__ == '__main__':
    unittest.main()