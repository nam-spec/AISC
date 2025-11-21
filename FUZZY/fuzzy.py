# universal_fuzzy.py
# Single-file minimal fuzzy toolkit (tri/trap MF, ops, relations, compositions, FIS, defuzz)

from math import isclose

# -------------------- Membership functions --------------------
class TriMF:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = float(a), float(b), float(c)
    def __call__(self, x):
        x = float(x)
        if x <= self.a or x >= self.c:
            return 0.0
        if self.a < x <= self.b:
            return (x - self.a) / (self.b - self.a) if not isclose(self.b, self.a) else 1.0
        return (self.c - x) / (self.c - self.b) if not isclose(self.c, self.b) else 1.0

class TrapMF:
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = map(float, (a,b,c,d))
    def __call__(self, x):
        x = float(x)
        if x <= self.a or x >= self.d:
            return 0.0
        if self.a < x <= self.b:
            return (x - self.a) / (self.b - self.a) if not isclose(self.b,self.a) else 1.0
        if self.b < x <= self.c:
            return 1.0
        return (self.d - x) / (self.d - self.c) if not isclose(self.d,self.c) else 1.0

# -------------------- Fuzzy variable (universe + named MFs) --------------------
class FuzzyVariable:
    def __init__(self, name, universe):
        self.name = name
        self.universe = list(universe)   # list of sample points (numbers)
        self.terms = {}                  # name -> mf (callable)

    def add_term(self, term_name, mf):
        self.terms[term_name] = mf

    def fuzzify_crisp(self, x):
        """Return membership dict for all terms at crisp x"""
        return {t: mf(x) for t, mf in self.terms.items()}

    def get_membership_vector(self, term_name):
        """Return list of membership degrees of a fuzzy set (term) over universe"""
        mf = self.terms[term_name]
        return [mf(x) for x in self.universe]

# -------------------- Basic fuzzy set operations (on discrete universe) --------------------
class FuzzyOps:
    @staticmethod
    def intersection(A, B):
        # A,B are dicts x->mu (same universe assumed keys)
        return {x: min(A[x], B[x]) for x in A}

    @staticmethod
    def union(A, B):
        return {x: max(A[x], B[x]) for x in A}

    @staticmethod
    def complement(A):
        return {x: 1.0 - A[x] for x in A}

    @staticmethod
    def alpha_cut(A, alpha):
        return [x for x in A if A[x] >= alpha]

# -------------------- Fuzzy relation construction --------------------
class FuzzyRelation:
    def __init__(self, from_var: FuzzyVariable, to_var: FuzzyVariable):
        self.X = from_var.universe
        self.Z = to_var.universe
        # relation matrix R[i][k] corresponds to X[i] -> Z[k] degrees
        self.R = [[0.0 for _ in self.Z] for _ in self.X]

    @staticmethod
    def relation_from_rule(from_var: FuzzyVariable, from_term: str,
                           to_var: FuzzyVariable, to_term: str):
        """
        Builds relation R from IF X is from_term THEN Z is to_term
        using standard Mamdani implication: R(x,z) = min( μ_from_term(x), μ_to_term(z) )
        """
        rel = FuzzyRelation(from_var, to_var)
        muX = from_var.get_membership_vector(from_term)
        muZ = to_var.get_membership_vector(to_term)
        for i, vx in enumerate(muX):
            for k, vz in enumerate(muZ):
                rel.R[i][k] = min(vx, vz)
        return rel

    @staticmethod
    def aggregate_relations(rel_list):
        """Given list of relations with same universes, aggregate by max (elementwise)."""
        if not rel_list:
            return None
        base = FuzzyRelation.__new__(FuzzyRelation)
        base.X = rel_list[0].X
        base.Z = rel_list[0].Z
        rows = len(base.X); cols = len(base.Z)
        base.R = [[0.0]*cols for _ in range(rows)]
        for rel in rel_list:
            for i in range(rows):
                for k in range(cols):
                    base.R[i][k] = max(base.R[i][k], rel.R[i][k])
        return base

    def print_relation(self):
        print("Relation matrix (rows: X, cols: Z):")
        header = "X\\Z\t" + "\t".join(f"{z}" for z in self.Z)
        print(header)
        for i,x in enumerate(self.X):
            row = f"{x}\t" + "\t".join(f"{self.R[i][k]:.2f}" for k in range(len(self.Z)))
            print(row)

# -------------------- Composition operators --------------------
def max_min_comp(R_mat, S_mat):
    # R_mat: m x n, S_mat: n x p => return m x p
    m, n = len(R_mat), len(R_mat[0])
    assert n == len(S_mat)
    p = len(S_mat[0])
    out = [[0.0]*p for _ in range(m)]
    for i in range(m):
        for k in range(p):
            vals = [min(R_mat[i][j], S_mat[j][k]) for j in range(n)]
            out[i][k] = max(vals) if vals else 0.0
    return out

def max_product_comp(R_mat, S_mat):
    m, n = len(R_mat), len(R_mat[0])
    assert n == len(S_mat)
    p = len(S_mat[0])
    out = [[0.0]*p for _ in range(m)]
    for i in range(m):
        for k in range(p):
            vals = [R_mat[i][j] * S_mat[j][k] for j in range(n)]
            out[i][k] = max(vals) if vals else 0.0
    return out

# -------------------- Evaluate input fuzzy (μ_X over X) through relation R to get μ_Z --------------------
def evaluate_input_via_relation(mu_X_vector, R_mat, method="max-min"):
    # mu_X_vector: length m, R_mat: m x p
    m = len(mu_X_vector)
    p = len(R_mat[0])
    mu_Z = [0.0]*p
    if method == "max-min":
        for k in range(p):
            vals = [min(mu_X_vector[i], R_mat[i][k]) for i in range(m)]
            mu_Z[k] = max(vals) if vals else 0.0
    else:  # max-product
        for k in range(p):
            vals = [mu_X_vector[i] * R_mat[i][k] for i in range(m)]
            mu_Z[k] = max(vals) if vals else 0.0
    return mu_Z

# -------------------- Mamdani FIS (multiple antecedent vars -> consequent var) --------------------
class MamdaniFIS:
    def __init__(self, antecedent_vars, consequent_var, rule_list):
        """
        antecedent_vars: list of FuzzyVariable (in order of antecedents in rule)
        consequent_var: FuzzyVariable (output var)
        rule_list: list of rules, each rule = ( [('var_index','term'), ...], ('out_term') )
           e.g., [ ( [(0,'Negative'), (1,'Decreasing')], 'Increase'), ... ]
        """
        self.ants = antecedent_vars
        self.cons = consequent_var
        self.rules = rule_list

    def evaluate(self, crisp_inputs, method="max-min"):
        """
        crisp_inputs: list of crisp values corresponding to antecedent_vars order
        method: when combining antecedent degrees, use 'min' (Mamdani). Composition 'max-min' or 'max-product' applies when chaining relations - here for rule strength we use min.
        Returns aggregated output membership on consequent universe (list aligned with consequent_var.universe).
        """
        # fuzzify each input
        fuzz_inputs = [var.fuzzify_crisp(x) for var,x in zip(self.ants, crisp_inputs)]
        # initialize zero membership across output universe
        agg = [0.0]*len(self.cons.universe)

        for rule in self.rules:
            ant_spec, out_term = rule  # ant_spec: list of (var_index, term)
            # compute rule strength = min of antecedent term memberships
            degrees = []
            for var_idx, term in ant_spec:
                deg = fuzz_inputs[var_idx].get(term, 0.0)
                degrees.append(deg)
            if degrees:
                rule_strength = min(degrees)
            else:
                rule_strength = 0.0

            # implication: clip consequent MF by rule_strength (Mamdani)
            cons_mf_values = self.cons.get_membership_vector(out_term)
            clipped = [min(rule_strength, v) for v in cons_mf_values]

            # aggregate via max
            agg = [max(agg[k], clipped[k]) for k in range(len(agg))]

        return agg  # a list of membership degrees aligned to cons.universe

# -------------------- Defuzzification --------------------
def centroid_defuzz(universe, mu):
    num = sum(u * m for u, m in zip(universe, mu))
    den = sum(mu)
    return (num / den) if den != 0 else 0.0

def weighted_singleton_defuzz(singleton_values, weights):
    """
    singleton_values: list of scalar representatives (same length as weights)
    weights: membership degrees
    """
    num = sum(s * w for s, w in zip(singleton_values, weights))
    den = sum(weights)
    return (num / den) if den != 0 else 0.0

# -------------------- Small utils --------------------
def print_fuzzy_vector(universe, mu, label="Fuzzy set"):
    print(label)
    print("x\tmu")
    for x,m in zip(universe, mu):
        print(f"{x}\t{m:.3f}")
    print()

# -------------------- End of toolkit --------------------

Dim = {0:1, 60:0.6, 120:0.2}
Normal = {0:0.2, 60:0.7, 120:1.0}

A = FuzzyOps.union(Dim, Normal)
B = FuzzyOps.intersection(Dim, Normal)
C = FuzzyOps.complement(Dim)
D = FuzzyOps.alpha_cut(Dim, 0.5)

print(A)
print(B)
print(C)
print(D)




