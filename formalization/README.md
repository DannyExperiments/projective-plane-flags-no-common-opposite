# Lean check of the flag construction

Lean proves that the constructed family has incident flags, has no common opposite, and has noncollinear point entries and nonconcurrent line entries given a third suitable point on the base line. The proof uses incidence, a chosen join with uniqueness for distinct points and a common point for each pair of lines. It works at arbitrary order. The finite cardinality of the family, the existence of the starting data at each order, the order-two analysis and the Desarguesian classification and count are in the paper.

The file imports only `Std` from Lean 4.30.0. Replay from this directory with the pinned toolchain.

```sh
lean -DwarningAsError=true FlagConstruction.lean > actual-axioms.txt
diff -u expected-axioms.txt actual-axioms.txt
```

The workflow runs the Lean kernel and checks the printed axiom report.
