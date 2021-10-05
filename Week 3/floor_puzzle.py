import itertools
from time import process_time_ns

#L != 5
#M != 0
#N != 0 and N != 5 and N != M + 1 and N != M - 1
#E == M + x
#J != N + 1 and J != N - 1

floors = ('M','J','N','E','L')
count = 0

t1_start = process_time_ns() 
for f in list(itertools.permutations(floors)):
    if (f[4] != 'L' and f[4] != 'N' and
        f[0] != 'M' and f[0] != 'N' and
        f.index('E') > f.index('M') and
        f.index('J') != f.index('N') - 1 and
        f.index('J') != f.index('N') + 1  and
        f.index('N') != f.index('M') - 1 and
        f.index('N') != f.index('M') + 1 ):
        print(f)

t1_stop = process_time_ns()
   
print("Elapsed time:", t1_stop, t1_start) 
   
print("Elapsed time during the whole program in seconds:",
                                         t1_stop-t1_start) 