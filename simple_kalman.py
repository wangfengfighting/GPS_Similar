__author__ = 'WangFeng'
# coding: utf-8
import  numpy
def Kalman(Z):
    n_iter = len(Z)
    sz = (n_iter,)
    Q = 1e-5
    xhat=numpy.zeros(sz)      # a posteri estimate of x
    P=numpy.zeros(sz)         # a posteri error estimate
    xhatminus=numpy.zeros(sz) # a priori estimate of x
    Pminus=numpy.zeros(sz)    # a priori error estimate
    K=numpy.zeros(sz)         # gain or blending factor
#    R = 0.1**2
#    R = numpy.std(numpy.array(Z)) * 1
    R = 1
    xhat[0] = Z[0]
    P[0] = 0.5
    for k in range(1,n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q
        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(Z[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]
    return xhat