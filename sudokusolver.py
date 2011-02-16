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
def grpof(r,c): return r/3*3+c/3
taken=set(xrange(1,10))

debug=0
from cProfile import *
inrow=[Set(mat[r][c] for c in dim) for r in dim]
incol=[Set(mat[r][c] for r in dim) for c in dim]
ingrp=[Set(mat[r][c] for r,c in grp) for grp in grps]
def rec(nfilled, sure):
  if nfilled == 9**2: return copy.deepcopy(mat)
  def indent(): return ' '*(2*(nfilled-nfilled0)-1)
  incell=[[taken if mat[r][c] else inrow[r] | incol[c] | ingrp[grpof(r,c)] for c in dim] for r in dim]
  def genopts():
    for n in nums:
      def do(gen, label):
        return [(r,c,n) for r,c in gen if n not in incell[r][c]]
      yield (do(((r,c) for c in dim), 'row %s' % r) for r in dim if n not in inrow[r])
      yield (do(((r,c) for r in dim), 'col %s' % c) for c in dim if n not in incol[c])
      yield (do(grp, 'grp %s' % g) for g, grp in enumerate(grps) if n not in ingrp[g])
  opts = filter(lambda opts: opts != [], chain.from_iterable(genopts()))
  if opts == []: return None # when does this happen?
  bestopts = min(opts, key=len)
  if bestopts == []: return None
  if debug and len(bestopts) > 1: print indent(), bestopts
  for r,c,n in bestopts:
    if debug: print indent(), 'trying', (r,c,n), 'nfilled', nfilled, 'sure' if sure else ''
    mat[r][c] = n
    incol[c].add(n)
    inrow[r].add(n)
    ingrp[grpof(r,c)].add(n)
    res = rec(nfilled+1, sure and len(bestopts)==1)
    mat[r][c] = None
    incol[c].remove(n)
    inrow[r].remove(n)
    ingrp[grpof(r,c)].remove(n)
    if res is not None: return res
nfilled0 = sum(sum(1 if x is not None else 0 for x in row) for row in mat)
mat = rec(nfilled0, True)
print '\n'.join(''.join(' ' if c is None else str(c) for c in line) for line in mat)

# vim: et sw=2 ts=2
