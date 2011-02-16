import copy
from itertools import *

input='''
159     3
    8   6
 8     1 
  42     
8  694  7
     51  
 3     8 
7   5    
2     549
'''.strip('\n')

input='''
   512 4 
 4       
  5 4 68 
8  9   12
         
37   5  8
 37   8  
    2  6 
 9 638   
'''.strip('\n')

input='''
3  6   84
     5   
   4  629
 9  43   
 8     7 
   87  5 
178  6   
   7     
42   8  7
'''.strip('\n')

mat=[[None if c == ' ' else int(c) for c in line] for line in input.split('\n')]
nums=range(1,10)

dim = range(9)
dims = [(r,c) for r in xrange(9) for c in xrange(9)]

def Set(xs): return set(x for x in xs if x is not None)
grps=[[(r,c) for r in range(g/3*3, g/3*3+3) for c in range(g%3*3, g%3*3+3)] for g in xrange(9)]
grpof=dict(((r,c), r/3*3+c/3) for r,c in dims)

def update(r,c,n):
  mat[r][c] = n
  incol[c].add(n)
  inrow[r].add(n)
  ingrp[grpof[r,c]].add(n)

def take(n, xs):
  for i in xrange(n):
    yield xs.next()

def rec(mat, opt, depth, sure):
  def indent(): return ' '*(2*depth-1)
  mat = copy.deepcopy(mat)
  if opt is not None:
    print indent(), 'trying', opt, 'depth', depth, 'sure' if sure else ''
    r,c,n = opt
    mat[r][c] = n
    if depth == 55:
       print '\n'.join(''.join(' ' if c is None else str(c) for c in line) for line in mat)
  if all(all(row) for row in mat): return [mat]
  inrow=[Set(mat[r][c] for c in dim) for r in dim]
  incol=[Set(mat[r][c] for r in dim) for c in dim]
  ingrp=[Set(mat[r][c] for r,c in grp) for grp in grps]
  def Gen():
    for n in nums:
      def do(gen, label):
        return [(r,c,n) for r,c in gen if not mat[r][c] and n not in inrow[r] | incol[c] | ingrp[grpof[r,c]]]
      yield (do(((r,c) for c in dim), 'row %s' % r) for r in dim if n not in inrow[r])
      yield (do(((r,c) for r in dim), 'col %s' % c) for c in dim if n not in incol[c])
      yield (do(grp, 'grp %s' % g) for g, grp in enumerate(grps) if n not in ingrp[g])
  opts = filter(lambda opts: opts != [], chain.from_iterable(Gen()))
  if opts == []:
    return []
  else:
    bestopts = min(opts, key=len)
    if bestopts == []:
      return []
    if len(bestopts) > 1: print indent(), bestopts
    return islice(chain.from_iterable(rec(mat, opt, depth+1, sure and len(bestopts)==1) for opt in bestopts), 1)
print list(rec(mat, None, 0, True))

# vim: et sw=2 ts=2
