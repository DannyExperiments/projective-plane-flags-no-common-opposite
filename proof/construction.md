# Q124: A counterexample in every finite projective plane

The [pinned catalog entry](https://github.com/10m-u/open-problems-catalog/blob/ca8d4d44ba3db527f19f28928c240168f545ecfe/problems/mathematics/geometry-differential-geometry-part-1.md#q124) asks whether the three cyclic triangle flags in the projective plane of order 2 are the only set of s+1 flags without a common opposite whose point entries are not a line and whose line entries are not a pencil. This is the question as posed in [Busch and Van Maldeghem, Remark 5.4](https://arxiv.org/html/2602.01110#S5.SS1). The answer is no, in every projective plane of order s≥3.

In any finite projective plane of order s≥2, choose a line m, distinct points R,A on m, and a point B off m. For distinct points U,V write UV for their joining line. Take these flags:
* (A,m);
* (B,BA);
* (X,BX) for all X on m other than R and A.

The count is 2+(s−1)=s+1, each flag is incident, and the point and line entries are each distinct. The points comprise the s points of m other than R, together with B, so they are not collinear. The lines comprise m and all lines through B except BR. At least two of these lines through B are selected, and m does not pass through B, so the line entries are not concurrent.

Now take any incident flag (y,n). If y is on any selected line, (y,n) is not opposite the flag with that line as its line entry. Otherwise, consider the unique join yB. It cannot be a selected line, and all lines through B other than BR are selected; consequently y∈BR and y∉m. In particular y≠B and y≠R. For every selected point X∈m, the line yX meets m at X; these s distinct lines are different from BR, which meets m at R. Adding the line BR=yB gives all s+1 lines through y. Thus n meets some selected point and again (y,n) is not opposite the flag with that point as its point entry. This proves there is no common opposite.

For a concrete order-3 example in homogeneous coordinates over F3, write [a,b,c] for the line ax+by+cz=0, and choose m=[0,1,0], R=(1,0,2), A=(1,0,0), B=(0,1,0). The four flags are
[
((1,0,0),[0,1,0]),quad
((0,1,0),[0,0,1]),quad
((0,0,1),[1,0,0]),quad
((1,0,1),[1,0,2]).
]
The candidate point y outside all four selected lines is one of (1,1,2),(1,2,2); every line through either passes through some selected point.

No claim of priority or of a classification of all counterexamples is made. The replay is optional; the argument uses only the axioms of a finite projective plane. For s=2 the construction reduces to cyclic triangle flags.
