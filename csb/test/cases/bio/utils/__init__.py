
import numpy
import multiprocessing

import csb.test as test
import csb.bio.utils as cbu

X1 = numpy.array([
    [ 0.,  0.,  0.],
    [ 1.,  0.,  0.],
    [ 0.,  1.,  0.]])

X2 = numpy.array([
    [ 0.,  0.,  0.],
    [ 1.,  2.,  0.],
    [-2., -1.,  0.]])

X3 = numpy.array([
    [ 0.,  0.,  0.],
    [ 2., -1.,  0.],
    [-1.,  2.,  0.]])

RZ = numpy.array([
    [ 0.,  1.,  0.],
    [-1.,  0.,  0.],
    [ 0.,  0.,  1.]])

X4 = numpy.array([
    [ 0.,  0.,  0.],
    [ 1.,  0.,  0.],
    [ 0.,  1.,  0.],
    [ 1.,  1.,  0.]])

X5 = numpy.array([
    [   0.,    0.,    0.],
    [ 100.,    0.,    0.],
    [   0.,  100.,    0.],
    [  50.,   50.,    0.]])

X6 = numpy.array([
    [   0.,    0.,    0.],
    [ 100.,    0.,    0.],
    [   0.,  100.,    0.],
    [  60.,   60.,    0.]])

@test.regression
class Regressions(test.Case):

    def testTMSuperimpose(self):
        """
        @see: [CSB 0000058]
        """
        def timeouttest():
            cbu.tm_superimpose([[1, 1, 1]], [[1, 1, 1]])

        p = multiprocessing.Process(target=timeouttest)
        p.start()
        p.join(timeout=0.1)

        if p.is_alive():
            p.terminate()
            self.fail('Timeout expired')

@test.functional
class TestUtils(test.Case):

    def assertArrayEqual(self, first, second, eps=1e-7):
        diff = numpy.asarray(first) - numpy.asarray(second)
        self.assertTrue((abs(diff) < eps).all())

    def testFit(self):
        R, t = cbu.fit(X1, X2)
        Y = numpy.dot(X2, R.T) + t

        self.assertArrayEqual(R, RZ)
        self.assertArrayEqual(t, [0., 0., 0.])
        self.assertArrayEqual(Y, X3)

    def testWFit(self):
        w = numpy.array([1., 1., 0.])
        R, t = cbu.wfit(X1, X2, w)

        d = 5.0**0.5
        self.assertArrayEqual(t, [-d / 2.0 + 0.5, 0., 0.])

    def testFitWellordered(self):
        R, t = cbu.fit_wellordered(X5, X6, 10, 1.0)

        self.assertArrayEqual(t, [0., 0., 0.])

    def testRmsd(self):
        rmsd = cbu.rmsd(X1, X2)

        self.assertAlmostEqual(rmsd, (4./3.)**0.5)

    def testWrmsd(self):
        w = numpy.array([1., 1., 0.])
        rmsd = cbu.wrmsd(X1, X2, w)

        d = 5.0**0.5
        self.assertAlmostEqual(rmsd, d / 2.0 - 0.5)

    def testTorsionRmsd(self):
        rmsd = cbu.torsion_rmsd(X1[:,:2], X1[:,:2])

        self.assertAlmostEqual(rmsd, 0.0)

    def testTmScore(self):
        score = cbu.tm_score(X1, X3)

        self.assertAlmostEqual(score, 0.4074, 4)

    def testTmSuperimpose(self):
        R, t, score = cbu.tm_superimpose(X1, X2)

        self.assertAlmostEqual(score, 0.4074, 4)

    def testCenterOfMass(self):
        com = cbu.center_of_mass(X4)

        self.assertArrayEqual(com, [0.5, 0.5, 0.0])

    def testRadiusOfGyration(self):
        gyradius = cbu.radius_of_gyration(X4)

        s2 = 2.0**0.5
        self.assertArrayEqual(gyradius, s2 / 2.0)

    def testSecondMoments(self):
        sm = cbu.second_moments(X1)

        # TODO: correct?
        sm_test = numpy.array([
            [ 2./3., -1./3., 0.    ],
            [-1./3.,  2./3., 0.    ],
            [ 0.,     0.,    0.    ]])
        self.assertArrayEqual(sm, sm_test)

    def testInertiaTensor(self):
        it = cbu.inertia_tensor(X1)

        # TODO: correct?
        it_test = numpy.array([
            [ 2./3.,  1./3., 0.    ],
            [ 1./3.,  2./3., 0.    ],
            [ 0.,     0.,    4./3. ]])
        self.assertArrayEqual(it, it_test)

    def testDistanceMatrix(self):
        d = cbu.distance_matrix(X1)

        s2 = 2.0**0.5
        d_test = [
            [ 0., 1., 1. ],
            [ 1., 0., s2 ],
            [ 1., s2, 0. ]]
        self.assertArrayEqual(d, d_test)

if __name__ == '__main__':

    test.Console()

# vi:expandtab:smarttab
