# Q124 supplement: classification in Desarguesian planes

Let q≥3 be a prime power. In PG(2,q), there are exactly q³(q+1)(q²+q+1) sets of q+1 incident point–line flags with noncollinear point entries, nonconcurrent line entries, and no common opposite flag. They all come from the construction below. This strengthens the [conjecture's disproof](https://arxiv.org/html/2602.01110v2#S5) but does not classify non-Desarguesian planes.

## Construction

Choose a line m, a point B off m, a point X on m, and another point A on m. Select the flags (A,m), (B,BA), and (Y,BY) for all Y on m except X,A. The selected points are B and the q points of m other than X; the selected lines are m and the q lines through B other than BX. These are noncollinear and nonconcurrent. A point y outside the union of the selected lines lies on BX off B and X. Its joins to the q selected points on m are pairwise distinct, and the line yB=BX is another. Thus every line through y contains a selected point. A candidate flag with point on a selected line or line through a selected point is not opposite every selected flag, proving the claim. This direction uses only the finite projective plane axioms and also works for q=2.

## Union bound and its equality case

At most q lines do not cover a plane: the first line contributes q+1 points and each additional line at most q, for at most 1+q². For q+1 distinct nonconcurrent lines, let k be the largest number of them concurrent. The k concurrent lines cover 1+kq points. Each other line meets these k lines at k distinct points and adds at most q+1−k points. The resulting union is at most
```
1+kq+(q+1−k)^2 = q²+2−(k−2)(q−k).
```
Here 2≤k≤q. When k=2, all pairwise crossings are distinct, so the union size is (q+1)(q+2)/2, strictly less than q²+2 for q≥3. Thus there are at least q−1 uncovered points, with equality only if k=q. Conversely when k=q, those q lines form a pencil missing one line and the extra line is off the pencil center, giving exactly q−1 uncovered points.

## Classification

Write P and L for the sets of point and line entries of the q+1 flags. The nonconcurrency and noncollinearity assumptions plus the union bounds and their dual give a point outside the union of L and a line disjoint from P, even if entries repeat. For each uncovered point y, every line through y meets P, or it would supply a common opposite. Since these q+1 lines are disjoint off y and y is outside P, this requires q+1 distinct members of P, exactly one on each line through y. Such a point is called a nucleus of P. By duality, L also has q+1 members and every line disjoint from P is a nucleus of L in the dual plane.

Use the Blokhuis–Wilbrink theorem: an affine set of q+1 points in AG(2,q) has at most q−1 nuclei. See [Blokhuis, On nuclei and affine blocking sets](https://research.tue.nl/en/publications/on-nuclei-and-affine-blocking-sets/) and the explicit statement as Result 1.2 in [Blokhuis–Mazzocca, Lifts of nuclei in finite projective spaces](https://doi.org/10.1017/CBO9780511526336.005). A line disjoint from P provides the affine chart; any projective nucleus is affine because its line at infinity cannot be disjoint from P. Thus the union bound for L is an equality. Its dual is also an equality, since the same theorem applies in the dual chart. Consequently L consists of a line m off B and all lines through B except one h. Dually P consists of q points on m' and one point B' off m'. Let X=h∩m and let X' be the missing point of m'.

The uncovered points are all of h except B and X. The nuclei of P are precisely the points of B'X' except B' and X': these q−1 points are nuclei by exactly the joins argument of the construction, and there are no more by the theorem. Since the uncovered points are nuclei and both sets have q−1 members, they are equal. As q−1≥2, h=B'X' and the two unordered excluded pairs coincide. The swapped possibility B'=X and X'=B is impossible: a selected line through B other than m' meets m' only at the missing point B, and cannot contain X since h is not selected, so it would contain no point of P to pair with. Therefore B'=B and X'=X. In this case m must equal m': otherwise m meets m' only at the missing point X and does not contain B, again impossible for a selected line. This identifies P and L. Since no entries repeat, a point A on m must pair with m, forcing B to pair with BA and every other point on m to pair with its own line through B.

For q≥3 the line m through the q collinear selected points is unique (any other line contains at most two selected points). Then B, X, and the point A paired with m are determined. There are q²+q+1 choices of m, q² choices of B off m, q+1 choices of X on m, and q choices of A. Multiplying yields the stated count.

No priority or external peer-review claim. The classification invokes a known theorem specific to Desarguesian planes, unlike the original construction. The optional finite replay is not a premise.
