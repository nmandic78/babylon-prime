import numpy as np
from mayavi import mlab
import math


def spiral(dim):

    seq_num = 0
    arr_spiral = np.zeros((dim, dim), dtype='uint')

    sequence = [np.arange(1, dim + 1).tolist()]
    for i in range(1, dim):
        sequence.append(np.arange(sequence[-1][-1] + 1, sequence[-1][-1] + dim + 1 - i).tolist())
        sequence.append(np.arange(sequence[-1][-1] + 1, sequence[-1][-1] + dim + 1 - i).tolist())

    arr_spiral[0:1, 0:len(sequence[0])] = sequence[0]

    for s in range(0, round((dim - 1) / 2)):
        seq_num += 1
        seq_len = len(sequence[seq_num])
        arr_spiral[s + 1:dim - s, dim - s - 1:dim - s] = np.asarray(sequence[seq_num]).reshape((seq_len, 1))
        seq_num += 1
        arr_spiral[dim - s - 1:dim - s, s:dim - s - 1] = np.asarray(list(reversed(sequence[seq_num])))
        if seq_num >= len(sequence) - 1:
            break
        seq_num += 1
        seq_len = len(sequence[seq_num])
        arr_spiral[s + 1:dim - s - 1, s:s + 1] = np.asarray(list(reversed(sequence[seq_num]))).reshape((seq_len, 1))
        seq_num += 1
        arr_spiral[s + 1:s + 2, s + 1:dim - s - 1] = np.asarray(sequence[seq_num])

    return arr_spiral


def zigzag(dim):

    arr_zigzag = np.zeros((dim, dim), dtype='uint')
    start = 0
    row = 0
    odd = True

    for i in range(dim, dim * dim + 1, dim):
        if odd:
            arr_zigzag[row, :] = np.arange(start, i).tolist()
        else:
            arr_zigzag[row, :] = np.asarray(list(reversed(np.arange(start, i).tolist())))
        odd = not odd
        start = i
        row += 1

    return arr_zigzag


# Credit for primesfrom2to function goes to Robert William Hanks:
# https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n/3035188#3035188
def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = np.ones(n//3 + (n % 6 == 2), dtype=np.bool)
    for i in range(1, int(n**0.5)//3+1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3::2*k] = False
            sieve[k*(k-2*(i & 1) + 4) // 3::2 * k] = False
    return np.r_[2, 3, ((3*np.nonzero(sieve)[0][1:]+1) | 1)]


# find primes
p1 = primesfrom2to(10000)[1:]

# make it square compatible
n = len(p1)
n_side = int(math.sqrt(n))
p1 = p1[:n_side * n_side]
n = len(p1)
n_side = int(math.sqrt(n))

# zigzag_idx = zigzag(n_side)     # make zigzag index
# prime_digits = p1[zigzag_idx]    # put primes sequence in zigzag

# uncomment one; this or zizzag(above) for differnet arrangement 
spiral_idx = spiral(n_side) - 1     # make spiral index
prime_digits = p1[spiral_idx]    # put primes sequence in spiral

x = np.arange(0, n_side, 1)
xs = np.tile(x, n_side)

y = np.arange(1, n_side+1, 1)
ys = np.repeat(y, n_side)

dz = np.ravel(prime_digits)

fig = mlab.figure(bgcolor=(0, 0, 0), size=(1280, 1024))

s = mlab.barchart(xs, ys, dz, opacity=1, colormap='spectral', extent=(0, 2, 0, 2, 0, 0.001))
s.glyph.color_mode = 'color_by_vector'

mlab.show()
