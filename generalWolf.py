import numpy as np
import CHSH
import tools as T
import matplotlib.pyplot as plt
acc = 1e-9
# Pauli matrices:
Gz = np.array([(1,0),(0,-1)])
Gx = np.array([(0,1),(1,0)])
G1 = np.array([(1,0),(0,1)])


def functional(t,r):
    B = [t, t, r, 0, 1, 1, 1, -1]
    return B

def BellOperator(t, r, a, b):
    A0 = np.cos(a/2)*Gz + np.sin(a/2)*Gx
    A1 = np.cos(a/2)*Gz - np.sin(a/2)*Gx
    B0 = Gz
    B1 = np.cos(b)*Gz + np.sin(b)*Gx
    B = t*(np.kron(A0, G1) + np.kron(A1,G1)) + r*np.kron(G1, B0) + np.kron(A0,B0) + np.kron(A0,B1) + np.kron(A1,B0) - np.kron(A1,B1)
    return B

def LValue(t,r):
    L1 = 2*t + r + 2
    L2 = -2*t + r - 2
    L3 = -2*t - r + 2
    L4 = r + 2
    return max([L1,L2,L3,L4])

def NSValue(t,r):
    return max(LValue(t, r), 4)

def bAnal(t,r):
    return np.pi/2

def CosAhalf(t, r):
    if t >= 1:
        print("error: |t|>=1")
        return 0 
    s = (r**2 - 4*t**2 + 4)/(2 - t**2)
    l = r*t + np.sqrt(s) 
    m = 2*(1 - t**2)
    if l/m > 1:
        print("error: cos(a/2) > 1")
        return 0 
    if m < acc:
        print("error: m=0 ")
        return 0 
    
    return l/m

def QValue(t,r):
    s = (4 + r**2 - 4*t**2)*(2 - t**2)
    l = r*t + np.sqrt(s)
    m = 1 - t**2
    QV = l/m
    if np.abs(t) < 1:
        return QV
    else:
        return LValue(t, r)

def cotThetaHalf(t,r):
    # |t| < 1
    if t > 1:
        print("error: t>1")
        return 0
    l = r*np.sqrt(2 - t**2) + np.sqrt(4 + r**2 - 4*t**2)*(1 + t - t**2)
    m1 = -2*r*t*np.sqrt((2 - t**2) * (4 + r**2 - 4*t**2))
    m2 = -r**2 * (1 + 2*t**2 - t**4) - 4*(-1 +4*t**2 -4*t**4 + t**6)
    # print(l,m1+m2)
    if m1+m2 <= acc:
        print("error: m1+m2<=0")
        return 0
    return l/np.sqrt(m1+m2)

def SinTheta(cot):
    return (2*cot)/(1 + cot**2)

def CosTheta(cot):
    return (cot**2 - 1)/(1 + cot**2)

def SinA(t,r):
    cos = CosAhalf(t,r)
    return np.sqrt(1-cos**2)

def quantumPoint(t,r):
    cot = cotThetaHalf(t,r)
    sinT = SinTheta(cot)
    cosT = CosTheta(cot)
    sinA = SinA(t,r)
    cosA = CosAhalf(t,r)
    return (cosA*cosT, cosA*cosT, cosT, 0, cosA, sinA*sinT, cosA, -sinA*sinT)

def testWolfPoint():
    r = 0.1327
    T = np.linspace(0,1,100)
    S1 = []
    S2 = []
    for i,t in enumerate(T):
        print(f'{i+1}/{len(T)}')
        B = functional(t,r)
        P1, _ = T.Best_point(B,0.001)
        P2 = quantumPoint(t,r)
        # print(P2)
        s1 = sum(P1)
        s2 = sum(P2)
        # print(s1,s2)
        S1.append(s1)
        S2.append(s2)
    plt.plot(S1)
    plt.plot(S2)
    plt.show()

def testWolfBQ():
    r = 0.1327
    T = np.linspace(0,1,100)
    BQ1 = []
    BQ2 = []
    for i,t in enumerate(T):
        print(f'{i+1}/{len(T)}')
        B = functional(t,r)
        bq1, _, _, _, _, _, _ = CHSH.chsh2(T.vector_to_matrix(B), 0.0001)
        bq2 = QValue(t,r)
        
        BQ1.append(bq1)
        BQ2.append(bq2)
    plt.plot(BQ1)
    plt.plot(BQ2)
    plt.show()
