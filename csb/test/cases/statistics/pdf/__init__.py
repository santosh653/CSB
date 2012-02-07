
import numpy
import numpy.random

import csb.test as test

from csb.statistics.pdf import Normal, GeneralizedNormal, Laplace, Gamma, MultivariateGaussian


@test.functional
class TestParameterEstimation(test.Case):
        
    def testNormal(self):
        
        mu, sigma = 2.2, 0.3
        data = numpy.random.normal(mu, sigma, 100000)
        
        pdf = Normal(1, 1)
        pdf.estimate(data)
        
        self.assertAlmostEqual(pdf.mu, mu, places=2)
        self.assertAlmostEqual(pdf.sigma, sigma, places=2)

    def testGeneralizedNormal(self):
        
        mu, alpha, beta = -0.04, 2.11, 1.90
        data = [-1.1712, -2.5608, -0.7143, 2.6218, -2.0655, 0.7544, 1.208, -0.5289, 0.0045, 1.1746, -1.0766, 1.1198, 1.2785, -0.6051, 2.2913, -3.6672, -0.2525, 0.8782, -0.0617, -0.0239]
        
        pdf = GeneralizedNormal(1, 1, 1)
        pdf.estimate(data)
        
        self.assertAlmostEqual(pdf.mu, mu, places=2)
        self.assertAlmostEqual(pdf.alpha, alpha, places=2)
        self.assertAlmostEqual(pdf.beta, beta, places=1)
        
    def testLaplace(self):
        
        mu, b = 2.2, 2
        data = numpy.random.laplace(mu, b, 100000)
        
        pdf = Laplace(1, 1)
        pdf.estimate(data)
        
        self.assertAlmostEqual(pdf.mu, mu, places=1)
        self.assertAlmostEqual(pdf.b, b, places=1)

    def testGamma(self):

        alpha = 0.1
        beta = 0.1

        data = numpy.random.gamma(alpha, 1. / beta, 10000)
        pdf = Gamma(1, 1)
        pdf.estimate(data)
        
        self.assertAlmostEqual(pdf.alpha, alpha, places=2)
        self.assertAlmostEqual(pdf.beta, beta, places=1)


    def testMultivariateGaussian(self):
        d = 3
        mu = numpy.ones(d)
        sigma = numpy.eye(d)

        pdf = MultivariateGaussian(mu, sigma)
        samples = pdf.random(100000)
        pdf.estimate(samples)

        for i in range(d):
            self.assertAlmostEqual(pdf.mu[i], mu[i], delta = 1e-1)
            for j in range(d):
                self.assertAlmostEqual(pdf.sigma[i,j], sigma[i,j], delta = 1e-1)
                

        d = 3
        mu = numpy.array([0.,1.,2.])
        sigma = numpy.random.random((d,d))
        sigma = numpy.dot(sigma, sigma.T)
        pdf = MultivariateGaussian(mu, sigma)
        samples = pdf.random(1000000)
        pdf.estimate(samples)

        for i in range(d):
            self.assertAlmostEqual(pdf.mu[i], mu[i], delta = 1e-1)
            for j in range(d):
                self.assertAlmostEqual(pdf.sigma[i,j], sigma[i,j], delta = 1e-1)

        

if __name__ == '__main__':
    
    test.Console()
        
