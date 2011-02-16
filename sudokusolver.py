import copy

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
while 1:
  mat2 = copy.deepcopy(mat)
  def refresh():
    inrow=[Set(mat[r][c] for c in dim) for r in dim]
    incol=[Set(mat[r][c] for r in dim) for c in dim]
    ingrp=[Set(mat[r][c] for r,c in grp) for grp in grps]
    return inrow, incol, ingrp
  inrow, incol, ingrp = refresh()

  for r in dim:
    for n in nums:
      poss = [(r,c) for c in dim if not mat[r][c] and n not in inrow[r] | incol[c] | ingrp[grpof[r,c]]]
      if len(poss)==1:
        print 'for row %s, %s can go in %s' % (r,n,poss)
        [(r,c)] = poss
        mat[r][c] = n
        inrow, incol, ingrp = refresh()
  for c in dim:
    for n in nums:
      poss = [(r,c) for r in dim if not mat[r][c] and n not in inrow[r] | incol[c] | ingrp[grpof[r,c]]]
      if len(poss)==1:
        print 'for col %s, %s can go in %s' % (c,n,poss)
        [(r,c)] = poss
        mat[r][c] = n
        inrow, incol, ingrp = refresh()
  for g, grp in enumerate(grps):
    for n in nums:
      poss = [(r,c) for r,c in grp if not mat[r][c] and n not in incol[c] | inrow[r] | ingrp[grpof[r,c]]]
      if len(poss)==1:
        print 'for grp %s, %s can go in %s' % (g,n,poss)
        if n == 9: import pdb; pdb.set_trace()
        [(r,c)] = poss
        mat[r][c] = n
        inrow, incol, ingrp = refresh()
  if mat2 == mat: break

# vim: et sw=2 ts=2
