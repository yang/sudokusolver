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

mat=[[None if c == ' ' else int(c) for c in line] for line in input.split('\n')]
nums=range(1,10)

dim = range(9)
dims = [(r,c) for r in xrange(9) for c in xrange(9)]

def Set(xs): return set(x for x in xs if x is not None)
grps=[[(r,c) for r in range(g/3*3, g/3*3+3) for c in range(g%3*3, g%3*3+3)] for g in xrange(9)]
grpof=dict(((r,c), r/3*3+c/3) for r,c in dims)

def refresh():
  inrow=[Set(mat[r][c] for c in dim) for r in dim]
  incol=[Set(mat[r][c] for r in dim) for c in dim]
  ingrp=[Set(mat[r][c] for r,c in grp) for grp in grps]
  return inrow, incol, ingrp

def update(r,c,n):
  mat[r][c] = n
  incol[c].add(n)
  inrow[r].add(n)
  ingrp[grpof[r,c]].add(n)

inrow, incol, ingrp = refresh()
while 1:
  def do(spots, label):
    updated = False
    for n in nums:
      poss = [(r,c) for r,c in spots if not mat[r][c] and n not in inrow[r] | incol[c] | ingrp[grpof[r,c]]]
      if len(poss)==1:
        print 'the %s in %s can go in %s' % (n,label,poss)
        [(r,c)] = poss
        update(r,c,n)
        updated |= True
    return updated
  updated = False
  for r in dim:
    updated |= do([(r,c) for c in dim], 'row %s' % r)
  for c in dim:
    updated |= do([(r,c) for r in dim], 'col %s' % c)
  for g, grp in enumerate(grps):
    updated |= do(grp, 'grp %s' % g)
  if not updated: break

# vim: et sw=2 ts=2
