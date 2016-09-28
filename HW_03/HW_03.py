import sys
import numpy as np

def strassen(a, b):
        n = a.shape[0]
        if (n == 1):
                return a*b

        n = n // 2
        a11 = a[:n,:n]
        a12 = a[:n,n:]
        a21 = a[n:,:n]
        a22 = a[n:,n:]
        b11 = b[:n,:n]
        b12 = b[:n,n:]
        b21 = b[n:,:n]
        b22 = b[n:,n:]

        p1 = strassen(a11+a22, b11+b22)
        p2 = strassen(a21+a22,     b11)
        p3 = strassen(    a11, b12-b22)
        p4 = strassen(    a22, b21-b11)
        p5 = strassen(a11+a12,     b22)
        p6 = strassen(a21-a11, b11+b12)
        p7 = strassen(a12-a22, b21+b22)

        c = np.empty(shape=(2*n, 2*n), dtype=np.int) 
        c[:n,:n] = p1+p4-p5+p7
        c[:n,n:] = p3+p5
        c[n:,:n] = p2+p4
        c[n:,n:] = p1-p2+p3+p6

        return c

if __name__ == "__main__":
        n = int(input())
        
        if n == 1:
                a = int(input())
                b = int(input())
                print(a*b)
                sys.exit(0)
        
        m = 1
        while m < n:
                m *= 2

        a = np.zeros((m,m), dtype=np.int)
        b = np.zeros((m,m), dtype=np.int)

        data = np.loadtxt(sys.stdin)
        a[:n,:n] = data[:n]
        b[:n,:n] = data[n:]

        c = strassen(a, b)
        for row in c[:n,:n]:
                print(' '.join(map(str,row)))
