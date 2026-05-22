"""50 remaining tasks: numerical (20) + strings (15) + ds_graph (15)."""

from builder import Task

REMAINING_TASKS = []


def add_num(task_id, name, n, body, main):
    REMAINING_TASKS.append(Task(task_id, name, "numerical", n, body, main))


def add_str(task_id, name, n, body, main):
    REMAINING_TASKS.append(Task(task_id, name, "strings", n, body, main))


def add_ds(task_id, name, n, body, main):
    REMAINING_TASKS.append(Task(task_id, name, "ds_graph", n, body, main))


# ============================================================
# NUMERICAL COMPUTING (20)
# ============================================================

# Task 51: Sieve of Eratosthenes
add_num(51, "prime_sieve", 5_000_000, '''
def sieve(limit):
    """Return primes up to limit using Sieve of Eratosthenes."""
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]
''', '''
primes = sieve(N)
return checksum(primes)
''')


# Task 52: Fibonacci DP (modular to keep ints bounded)
add_num(52, "fibonacci_dp", 5000, '''
MOD = 1_000_000_007

def fib_n(n):
    """Return nth Fibonacci number mod MOD."""
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, (a + b) % MOD
    return b

def fib_many(ks):
    return [fib_n(k) for k in ks]
''', '''
ks = list(range(N))
results = fib_many(ks)
return checksum(results[::10])
''')


# Task 53: Matrix multiply
add_num(53, "matrix_multiply", 150, '''
def matmul(A, B, n):
    """Multiply two n×n matrices."""
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C

def make_matrix(n, seed):
    import random
    rng = random.Random(seed)
    return [[rng.randint(0, 100) for _ in range(n)] for _ in range(n)]
''', '''
n = N
A = make_matrix(n, TASK_ID)
B = make_matrix(n, TASK_ID + 1)
C = matmul(A, B, n)
flat = [v for row in C for v in row]
return checksum(flat)
''')


# Task 54: Matrix transpose
add_num(54, "matrix_transpose", 200, '''
def transpose(M, n):
    """Transpose n×n matrix."""
    return [[M[j][i] for j in range(n)] for i in range(n)]

def make_matrix(n, seed):
    import random
    rng = random.Random(seed)
    return [[rng.randint(0, 1000) for _ in range(n)] for _ in range(n)]
''', '''
n = N
results = []
for k in range(20):
    M = make_matrix(n, TASK_ID + k)
    T = transpose(M, n)
    results.append(T[0][0] + T[n-1][n-1])
return checksum(results)
''')


# Task 55: Dot product batch
add_num(55, "dot_product_batch", 5000, '''
def dot(a, b):
    """Dot product of two equal-length vectors."""
    s = 0
    for i in range(len(a)):
        s += a[i] * b[i]
    return s

def batch_dot(pairs):
    return [dot(a, b) for a, b in pairs]
''', '''
import random
rng = random.Random(TASK_ID)
size = 500
pairs = []
for _ in range(N):
    a = [rng.randint(-100, 100) for _ in range(size)]
    b = [rng.randint(-100, 100) for _ in range(size)]
    pairs.append((a, b))
results = batch_dot(pairs)
return checksum(results)
''')


# Task 56: Monte Carlo pi
add_num(56, "monte_carlo_pi", 1_500_000, '''
def monte_carlo_pi(n, seed):
    """Estimate pi using Monte Carlo method."""
    import random
    rng = random.Random(seed)
    inside = 0
    for _ in range(n):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / n

def multi_estimate(samples, seeds):
    return [monte_carlo_pi(samples, s) for s in seeds]
''', '''
seeds = [TASK_ID + i for i in range(5)]
estimates = multi_estimate(N // 5, seeds)
return checksum([int(e * 1_000_000) for e in estimates])
''')


# Task 57: GCD batch
add_num(57, "gcd_batch", 200000, '''
def gcd(a, b):
    """Euclidean GCD."""
    while b:
        a, b = b, a % b
    return a

def gcd_many(pairs):
    return [gcd(a, b) for a, b in pairs]
''', '''
pairs = get_int_pairs(TASK_ID, N)
results = gcd_many(pairs)
return checksum(results)
''')


# Task 58: Modular exponentiation
add_num(58, "modular_exponent", 50000, '''
def mod_pow(base, exp, mod):
    """Compute (base^exp) mod mod."""
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

def mod_pow_many(triples):
    return [mod_pow(b, e, m) for b, e, m in triples]
''', '''
import random
rng = random.Random(TASK_ID)
triples = [(rng.randint(2, 10**9), rng.randint(10**6, 10**8), 10**9 + 7) for _ in range(N)]
results = mod_pow_many(triples)
return checksum(results)
''')


# Task 59: Newton's sqrt
add_num(59, "newton_sqrt", 200000, '''
def newton_sqrt(x):
    """Square root via Newton's method."""
    if x < 0:
        return 0.0
    if x == 0:
        return 0.0
    g = x
    for _ in range(50):
        g = (g + x / g) / 2
    return g

def sqrt_many(values):
    return [newton_sqrt(v) for v in values]
''', '''
values = get_float_array(TASK_ID, N)
results = sqrt_many(values)
return checksum([int(r * 1000) for r in results])
''')


# Task 60: Polynomial eval (Horner)
add_num(60, "polynomial_eval", 30000, '''
def horner(coeffs, x):
    """Evaluate polynomial at x using Horner's method."""
    result = 0
    for c in coeffs:
        result = result * x + c
    return result

def eval_many(polys, xs):
    return [horner(p, x) for p, x in zip(polys, xs)]
''', '''
import random
rng = random.Random(TASK_ID)
polys = [[rng.randint(-10, 10) for _ in range(100)] for _ in range(N)]
xs = [rng.random() * 2 - 1 for _ in range(N)]
results = eval_many(polys, xs)
return checksum([int(r * 1000) for r in results])
''')


# Task 61: Simpson's rule integration
add_num(61, "integral_simpson", 10000, '''
def simpson(f_coeffs, a, b, n):
    """Simpson's rule for polynomial defined by coefficients."""
    def evaluate(x):
        result = 0
        for c in f_coeffs:
            result = result * x + c
        return result
    if n % 2:
        n += 1
    h = (b - a) / n
    s = evaluate(a) + evaluate(b)
    for i in range(1, n):
        x = a + i * h
        s += 4 * evaluate(x) if i % 2 else 2 * evaluate(x)
    return s * h / 3

def integrate_many(polys, ranges):
    return [simpson(p, a, b, 500) for p, (a, b) in zip(polys, ranges)]
''', '''
import random
rng = random.Random(TASK_ID)
polys = [[rng.randint(-5, 5) for _ in range(5)] for _ in range(N)]
ranges = [(rng.random(), 1.0 + rng.random()) for _ in range(N)]
results = integrate_many(polys, ranges)
return checksum([int(r * 1000) for r in results])
''')


# Task 62: Linear regression
add_num(62, "linear_regression", 500, '''
def linear_regression(xs, ys):
    """Closed-form simple linear regression."""
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    denom = n * sxx - sx * sx
    if denom == 0:
        return (0.0, 0.0)
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    return (slope, intercept)

def fit_many(datasets):
    return [linear_regression(xs, ys) for xs, ys in datasets]
''', '''
import random
rng = random.Random(TASK_ID)
datasets = []
for _ in range(N):
    xs = [rng.random() * 10 for _ in range(1000)]
    ys = [2.5 * x + 1.0 + rng.gauss(0, 0.1) for x in xs]
    datasets.append((xs, ys))
results = fit_many(datasets)
return checksum([(int(s*1000), int(i*1000)) for s, i in results])
''')


# Task 63: K-means 1D
add_num(63, "kmeans_1d", 30, '''
def kmeans_1d(points, k, iters=50):
    """K-means on 1D points."""
    points = sorted(points)
    n = len(points)
    centroids = [points[i * n // k] for i in range(k)]
    for _ in range(iters):
        clusters = [[] for _ in range(k)]
        for p in points:
            best = 0
            bd = abs(p - centroids[0])
            for c in range(1, k):
                d = abs(p - centroids[c])
                if d < bd:
                    bd = d
                    best = c
            clusters[best].append(p)
        new_centroids = []
        for i, cl in enumerate(clusters):
            if cl:
                new_centroids.append(sum(cl) / len(cl))
            else:
                new_centroids.append(centroids[i])
        if all(abs(a - b) < 1e-6 for a, b in zip(centroids, new_centroids)):
            break
        centroids = new_centroids
    return centroids
''', '''
import random
rng = random.Random(TASK_ID)
results = []
for _ in range(N):
    points = [rng.gauss(0, 1) + (rng.randint(0, 4) * 5) for _ in range(5000)]
    cents = kmeans_1d(points, 5)
    results.append(sorted(cents))
return checksum([int(c * 1000) for cents in results for c in cents])
''')


# Task 64: Histogram
add_num(64, "histogram_compute", 100, '''
def histogram(values, n_bins):
    """Build histogram of values."""
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if lo == hi:
        return [len(values)] + [0] * (n_bins - 1)
    width = (hi - lo) / n_bins
    bins = [0] * n_bins
    for v in values:
        idx = min(int((v - lo) / width), n_bins - 1)
        bins[idx] += 1
    return bins
''', '''
import random
rng = random.Random(TASK_ID)
results = []
for _ in range(N):
    values = [rng.gauss(0, 1) for _ in range(50000)]
    h = histogram(values, 50)
    results.extend(h)
return checksum(results)
''')


# Task 65: Online running stats
add_num(65, "running_stats", 5_000_000, '''
def running_stats(values):
    """Welford's online mean/variance."""
    n = 0
    mean = 0.0
    m2 = 0.0
    for x in values:
        n += 1
        delta = x - mean
        mean += delta / n
        delta2 = x - mean
        m2 += delta * delta2
    if n < 2:
        return mean, 0.0
    return mean, m2 / (n - 1)
''', '''
import random
rng = random.Random(TASK_ID)
values = [rng.gauss(5, 2) for _ in range(N)]
m, v = running_stats(values)
return checksum([int(m * 1000), int(v * 1000)])
''')


# Task 66: 1D convolution
add_num(66, "discrete_convolution", 2000, '''
def convolve(a, b):
    """Discrete 1D convolution."""
    n = len(a)
    m = len(b)
    result = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            result[i + j] += a[i] * b[j]
    return result
''', '''
import random
rng = random.Random(TASK_ID)
a = [rng.randint(-10, 10) for _ in range(N)]
b = [rng.randint(-5, 5) for _ in range(N // 4)]
result = convolve(a, b)
return checksum(result[::10])
''')


# Task 67: LCM batch
add_num(67, "lcm_batch", 150000, '''
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)

def lcm_many(pairs):
    return [lcm(a, b) for a, b in pairs]
''', '''
pairs = get_int_pairs(TASK_ID, N, max_val=10000)
results = lcm_many(pairs)
return checksum(results)
''')


# Task 68: Prime factorization
add_num(68, "prime_factorization", 30000, '''
def factor(n):
    """Trial-division factorization."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def factor_many(values):
    return [factor(v) for v in values]
''', '''
import random
rng = random.Random(TASK_ID)
values = [rng.randint(2, 10**9) for _ in range(N)]
results = factor_many(values)
return checksum([sum(f) for f in results])
''')


# Task 69: Catalan numbers
add_num(69, "catalan_numbers", 500, '''
def catalan(n):
    """First n Catalan numbers via DP."""
    if n <= 0:
        return []
    c = [0] * n
    c[0] = 1
    for i in range(1, n):
        c[i] = 0
        for j in range(i):
            c[i] += c[j] * c[i - 1 - j]
    return c
''', '''
results = catalan(N)
return checksum([r % 1_000_000_007 for r in results])
''')


# Task 70: Vector L2 norm batch
add_num(70, "vector_norm", 20000, '''
def l2_norm(v):
    """L2 (Euclidean) norm."""
    s = 0.0
    for x in v:
        s += x * x
    return s ** 0.5

def norm_many(vectors):
    return [l2_norm(v) for v in vectors]
''', '''
import random
rng = random.Random(TASK_ID)
vectors = [[rng.random() * 10 for _ in range(500)] for _ in range(N)]
results = norm_many(vectors)
return checksum([int(r * 1000) for r in results])
''')


# ============================================================
# STRING ALGORITHMS (15)
# ============================================================

# Task 71: Edit distance
add_str(71, "edit_distance", 100, '''
def edit_distance(a, b):
    """Levenshtein edit distance."""
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            t = dp[j]
            if a[i-1] == b[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])
            prev = t
    return dp[n]

def dist_many(pairs):
    return [edit_distance(a, b) for a, b in pairs]
''', '''
strs = get_string_array(TASK_ID, N * 2, max_len=200)
pairs = list(zip(strs[::2], strs[1::2]))
results = dist_many(pairs)
return checksum(results)
''')


# Task 72: LCS
add_str(72, "longest_common_sub", 100, '''
def lcs(a, b):
    """Longest common subsequence length."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])
    return dp[m][n]

def lcs_many(pairs):
    return [lcs(a, b) for a, b in pairs]
''', '''
strs = get_string_array(TASK_ID, N * 2, max_len=150)
pairs = list(zip(strs[::2], strs[1::2]))
results = lcs_many(pairs)
return checksum(results)
''')


# Task 73: KMP search
add_str(73, "kmp_search", 1000, '''
def kmp_table(pat):
    """Build KMP failure function."""
    t = [0] * len(pat)
    k = 0
    for i in range(1, len(pat)):
        while k > 0 and pat[k] != pat[i]:
            k = t[k-1]
        if pat[k] == pat[i]:
            k += 1
        t[i] = k
    return t

def kmp_search(text, pat):
    """Return all match positions."""
    if not pat:
        return []
    t = kmp_table(pat)
    matches = []
    k = 0
    for i, c in enumerate(text):
        while k > 0 and pat[k] != c:
            k = t[k-1]
        if pat[k] == c:
            k += 1
        if k == len(pat):
            matches.append(i - k + 1)
            k = t[k-1]
    return matches

def search_many(text, pats):
    return [len(kmp_search(text, p)) for p in pats]
''', '''
import random
rng = random.Random(TASK_ID)
chars = "abc"
text = ''.join(rng.choices(chars, k=100000))
pats = [''.join(rng.choices(chars, k=5)) for _ in range(N)]
counts = search_many(text, pats)
return checksum(counts)
''')


# Task 74: Rabin-Karp
add_str(74, "rabin_karp", 800, '''
def rabin_karp(text, pat, base=257, mod=10**9 + 7):
    """Find pattern using rolling hash."""
    n, m = len(text), len(pat)
    if m == 0 or m > n:
        return []
    matches = []
    h = 1
    for _ in range(m - 1):
        h = (h * base) % mod
    p_hash = 0
    t_hash = 0
    for i in range(m):
        p_hash = (p_hash * base + ord(pat[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i+m] == pat:
            matches.append(i)
        if i < n - m:
            t_hash = ((t_hash - ord(text[i]) * h) * base + ord(text[i + m])) % mod
            if t_hash < 0:
                t_hash += mod
    return matches

def search_many(text, pats):
    return [len(rabin_karp(text, p)) for p in pats]
''', '''
import random
rng = random.Random(TASK_ID)
chars = "abc"
text = ''.join(rng.choices(chars, k=80000))
pats = [''.join(rng.choices(chars, k=5)) for _ in range(N)]
counts = search_many(text, pats)
return checksum(counts)
''')


# Task 75: Z algorithm
add_str(75, "z_algorithm", 1000, '''
def z_function(s):
    """Z-function: z[i] = length of longest substring starting at i that matches prefix."""
    n = len(s)
    z = [0] * n
    z[0] = n
    l, r = 0, 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

def z_many(strings):
    return [sum(z_function(s)) for s in strings]
''', '''
strs = get_string_array(TASK_ID, N, max_len=500)
results = z_many(strs)
return checksum(results)
''')


# Task 76: Manacher's
add_str(76, "manacher_palindrome", 1000, '''
def manacher(s):
    """Find longest palindromic substring using Manacher's algorithm."""
    if not s:
        return ""
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    center = 0
    right = 0
    for i in range(n):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        a = i + p[i] + 1
        b = i - p[i] - 1
        while a < n and b >= 0 and t[a] == t[b]:
            p[i] += 1
            a += 1
            b -= 1
        if i + p[i] > right:
            center = i
            right = i + p[i]
    mx = max(p)
    return mx

def manacher_many(strs):
    return [manacher(s) for s in strs]
''', '''
strs = get_string_array(TASK_ID, N, max_len=400)
results = manacher_many(strs)
return checksum(results)
''')


# Task 77: Suffix array (naive)
add_str(77, "suffix_array_naive", 60, '''
def suffix_array(s):
    """Build suffix array by sorting all suffixes."""
    suffixes = sorted(range(len(s)), key=lambda i: s[i:])
    return suffixes
''', '''
strs = get_string_array(TASK_ID, N, max_len=2000)
all_sa = []
for s in strs:
    sa = suffix_array(s)
    all_sa.extend(sa[:20])
return checksum(all_sa)
''')


# Task 78: Anagram groups
add_str(78, "anagram_groups", 30000, '''
def group_anagrams(words):
    """Group words by anagram (sorted-char key)."""
    groups = {}
    for w in words:
        key = ''.join(sorted(w))
        if key not in groups:
            groups[key] = []
        groups[key].append(w)
    return groups
''', '''
words = get_string_array(TASK_ID, N, max_len=10)
groups = group_anagrams(words)
sizes = sorted([len(v) for v in groups.values()])
return checksum(sizes)
''')


# Task 79: Longest repeated substring
add_str(79, "longest_repeated_sub", 50, '''
def longest_repeated(s):
    """Find longest repeated substring (naive O(n^2) compare)."""
    n = len(s)
    suffixes = sorted([s[i:] for i in range(n)])
    longest = ""
    for i in range(len(suffixes) - 1):
        a, b = suffixes[i], suffixes[i + 1]
        k = 0
        while k < min(len(a), len(b)) and a[k] == b[k]:
            k += 1
        if k > len(longest):
            longest = a[:k]
    return longest

def lr_many(strs):
    return [len(longest_repeated(s)) for s in strs]
''', '''
strs = get_string_array(TASK_ID, N, max_len=1500)
results = lr_many(strs)
return checksum(results)
''')


# Task 80: Boyer-Moore (bad-char heuristic only)
add_str(80, "boyer_moore_lite", 800, '''
def bm_bad_char(pat):
    """Build bad character table."""
    table = {}
    for i, c in enumerate(pat):
        table[c] = i
    return table

def bm_search(text, pat):
    """Boyer-Moore with bad-character heuristic."""
    m = len(pat)
    n = len(text)
    if m == 0 or m > n:
        return []
    bc = bm_bad_char(pat)
    matches = []
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pat[j] == text[s + j]:
            j -= 1
        if j < 0:
            matches.append(s)
            s += 1
        else:
            s += max(1, j - bc.get(text[s + j], -1))
    return matches

def search_many(text, pats):
    return [len(bm_search(text, p)) for p in pats]
''', '''
import random
rng = random.Random(TASK_ID)
chars = "abcd"
text = ''.join(rng.choices(chars, k=80000))
pats = [''.join(rng.choices(chars, k=6)) for _ in range(N)]
counts = search_many(text, pats)
return checksum(counts)
''')


# Task 81: String rotation
add_str(81, "string_rotation", 100000, '''
def is_rotation(a, b):
    """Check if b is rotation of a."""
    if len(a) != len(b):
        return False
    if not a:
        return True
    return b in (a + a)

def check_many(pairs):
    return [1 if is_rotation(a, b) else 0 for a, b in pairs]
''', '''
strs = get_string_array(TASK_ID, N * 2, max_len=50)
pairs = list(zip(strs[::2], strs[1::2]))
results = check_many(pairs)
return checksum(results)
''')


# Task 82: RLE encode/decode
add_str(82, "run_length_encoding", 100000, '''
def rle_encode(s):
    """Run-length encode a string."""
    if not s:
        return ""
    out = []
    cur = s[0]
    cnt = 1
    for c in s[1:]:
        if c == cur:
            cnt += 1
        else:
            out.append(f"{cnt}{cur}")
            cur = c
            cnt = 1
    out.append(f"{cnt}{cur}")
    return ''.join(out)

def encode_many(strs):
    return [rle_encode(s) for s in strs]
''', '''
strs = get_string_array(TASK_ID, N, max_len=60)
results = encode_many(strs)
return checksum([len(s) for s in results])
''')


# Task 83: Soundex
add_str(83, "soundex", 200000, '''
def soundex(name):
    """Soundex encoding."""
    if not name:
        return "0000"
    name = name.upper()
    code = name[0]
    mapping = {'B':'1','F':'1','P':'1','V':'1',
               'C':'2','G':'2','J':'2','K':'2','Q':'2','S':'2','X':'2','Z':'2',
               'D':'3','T':'3','L':'4','M':'5','N':'5','R':'6'}
    prev = mapping.get(code, '')
    for c in name[1:]:
        d = mapping.get(c, '')
        if d and d != prev:
            code += d
            if len(code) == 4:
                break
        if c not in 'HW':
            prev = d
    return (code + "000")[:4]

def soundex_many(names):
    return [soundex(n) for n in names]
''', '''
names = get_string_array(TASK_ID, N, max_len=15)
results = soundex_many(names)
return checksum(results)
''')


# Task 84: Longest common prefix
add_str(84, "longest_prefix", 5000, '''
def longest_common_prefix(strs):
    """Find longest common prefix of all strings."""
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        i = 0
        while i < len(prefix) and i < len(s) and prefix[i] == s[i]:
            i += 1
        prefix = prefix[:i]
        if not prefix:
            break
    return prefix

def lcp_batch(groups):
    return [longest_common_prefix(g) for g in groups]
''', '''
import random
rng = random.Random(TASK_ID)
groups = []
for _ in range(N):
    base = ''.join(rng.choices("abcdef", k=20))
    group = [base[:rng.randint(5, 20)] + rng.choice("xyz") + ''.join(rng.choices("abcdef", k=10))
             for _ in range(20)]
    groups.append(group)
results = lcp_batch(groups)
return checksum([len(p) for p in results])
''')


# Task 85: Palindrome partition (min cuts)
add_str(85, "palindrome_partition", 200, '''
def min_palindrome_cuts(s):
    """Min cuts to partition s into palindromes."""
    n = len(s)
    if n <= 1:
        return 0
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length == 2 or is_pal[i+1][j-1]:
                    is_pal[i][j] = True
    cuts = [0] * n
    for i in range(n):
        if is_pal[0][i]:
            cuts[i] = 0
        else:
            cuts[i] = i
            for j in range(1, i + 1):
                if is_pal[j][i] and cuts[j-1] + 1 < cuts[i]:
                    cuts[i] = cuts[j-1] + 1
    return cuts[n-1]

def cuts_many(strs):
    return [min_palindrome_cuts(s) for s in strs]
''', '''
strs = get_string_array(TASK_ID, N, max_len=100)
results = cuts_many(strs)
return checksum(results)
''')


# ============================================================
# DATA STRUCTURES & GRAPHS (15)
# ============================================================

# Task 86: BST operations
add_ds(86, "bst_operations", 50000, '''
class BSTNode:
    __slots__ = ('key', 'left', 'right')
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def bst_insert(root, key):
    if root is None:
        return BSTNode(key)
    if key < root.key:
        root.left = bst_insert(root.left, key)
    elif key > root.key:
        root.right = bst_insert(root.right, key)
    return root

def bst_search(root, key):
    if root is None:
        return False
    if key == root.key:
        return True
    if key < root.key:
        return bst_search(root.left, key)
    return bst_search(root.right, key)

def bst_inorder(root, out):
    if root:
        bst_inorder(root.left, out)
        out.append(root.key)
        bst_inorder(root.right, out)
''', '''
import sys
sys.setrecursionlimit(200000)
root = None
keys = get_int_array(TASK_ID, N)
for k in keys:
    root = bst_insert(root, k)
queries = get_int_array(TASK_ID, N // 2, seed_offset=1)
found = [bst_search(root, q) for q in queries]
return checksum([1 if f else 0 for f in found])
''')


# Task 87: AVL tree
add_ds(87, "avl_tree_ops", 30000, '''
class AVL:
    __slots__ = ('key', 'h', 'left', 'right')
    def __init__(self, k):
        self.key = k; self.h = 1; self.left = None; self.right = None

def avl_h(n): return n.h if n else 0

def avl_balance(n):
    return avl_h(n.left) - avl_h(n.right) if n else 0

def avl_rot_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    y.h = 1 + max(avl_h(y.left), avl_h(y.right))
    x.h = 1 + max(avl_h(x.left), avl_h(x.right))
    return x

def avl_rot_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    x.h = 1 + max(avl_h(x.left), avl_h(x.right))
    y.h = 1 + max(avl_h(y.left), avl_h(y.right))
    return y

def avl_insert(root, key):
    if not root:
        return AVL(key)
    if key < root.key:
        root.left = avl_insert(root.left, key)
    elif key > root.key:
        root.right = avl_insert(root.right, key)
    else:
        return root
    root.h = 1 + max(avl_h(root.left), avl_h(root.right))
    b = avl_balance(root)
    if b > 1 and key < root.left.key:
        return avl_rot_right(root)
    if b < -1 and key > root.right.key:
        return avl_rot_left(root)
    if b > 1 and key > root.left.key:
        root.left = avl_rot_left(root.left)
        return avl_rot_right(root)
    if b < -1 and key < root.right.key:
        root.right = avl_rot_right(root.right)
        return avl_rot_left(root)
    return root

def avl_search(root, key):
    while root:
        if key == root.key:
            return True
        root = root.left if key < root.key else root.right
    return False
''', '''
import sys
sys.setrecursionlimit(200000)
root = None
keys = get_int_array(TASK_ID, N)
for k in keys:
    root = avl_insert(root, k)
queries = get_int_array(TASK_ID, N // 2, seed_offset=1)
found = [avl_search(root, q) for q in queries]
return checksum([1 if f else 0 for f in found])
''')


# Task 88: Heap operations
add_ds(88, "heap_operations", 500000, '''
def heap_push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0:
        p = (i - 1) // 2
        if heap[p] > heap[i]:
            heap[p], heap[i] = heap[i], heap[p]
            i = p
        else:
            break

def heap_pop(heap):
    if not heap:
        return None
    top = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i = 0
        n = len(heap)
        while True:
            l = 2 * i + 1
            r = 2 * i + 2
            smallest = i
            if l < n and heap[l] < heap[smallest]:
                smallest = l
            if r < n and heap[r] < heap[smallest]:
                smallest = r
            if smallest != i:
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
            else:
                break
    return top
''', '''
keys = get_int_array(TASK_ID, N)
heap = []
for k in keys:
    heap_push(heap, k)
popped = []
for _ in range(len(heap)):
    popped.append(heap_pop(heap))
return checksum(popped)
''')


# Task 89: Hashmap with chaining
add_ds(89, "hashmap_chaining", 200000, '''
class HashMap:
    def __init__(self, n_buckets=1024):
        self.n = n_buckets
        self.buckets = [[] for _ in range(n_buckets)]
    def _h(self, k):
        return hash(k) % self.n
    def put(self, k, v):
        b = self.buckets[self._h(k)]
        for i, (kk, _) in enumerate(b):
            if kk == k:
                b[i] = (k, v)
                return
        b.append((k, v))
    def get(self, k):
        for kk, vv in self.buckets[self._h(k)]:
            if kk == k:
                return vv
        return None
''', '''
keys = get_int_array(TASK_ID, N)
m = HashMap()
for k in keys:
    m.put(k, k * 7)
queries = get_int_array(TASK_ID, N // 2, seed_offset=1)
results = [m.get(q) for q in queries]
results = [r if r is not None else 0 for r in results]
return checksum(results)
''')


# Task 90: Trie operations
add_ds(90, "trie_operations", 30000, '''
class Trie:
    def __init__(self):
        self.root = {}
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node:
                node[c] = {}
            node = node[c]
        node['$'] = True
    def search(self, word):
        node = self.root
        for c in word:
            if c not in node:
                return False
            node = node[c]
        return '$' in node
    def starts_with(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node:
                return False
            node = node[c]
        return True
''', '''
words = get_string_array(TASK_ID, N, max_len=15)
t = Trie()
for w in words:
    t.insert(w)
queries = get_string_array(TASK_ID, N // 2, max_len=10)
found = [t.starts_with(q) for q in queries]
return checksum([1 if f else 0 for f in found])
''')


# Task 91: Union-Find
add_ds(91, "union_find", 1_000_000, '''
class UF:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True
''', '''
size = 100000
uf = UF(size)
pairs = get_int_pairs(TASK_ID, N, max_val=size - 1)
unions_done = sum(1 for a, b in pairs if uf.union(a, b))
roots = [uf.find(i) for i in range(0, size, 100)]
return checksum(roots + [unions_done])
''')


# Task 92: BFS
add_ds(92, "bfs_traversal", 5000, '''
from collections import deque as _dq

def build_graph(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    return g

def bfs(g, start):
    visited = [False] * len(g)
    order = []
    q = _dq([start])
    visited[start] = True
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            if not visited[v]:
                visited[v] = True
                q.append(v)
    return order
''', '''
import random
rng = random.Random(TASK_ID)
n_vertices = N
edges = [(rng.randint(0, n_vertices - 1), rng.randint(0, n_vertices - 1)) for _ in range(n_vertices * 3)]
g = build_graph(n_vertices, edges)
order = bfs(g, 0)
return checksum(order)
''')


# Task 93: DFS
add_ds(93, "dfs_traversal", 5000, '''
def build_graph(n, edges):
    g = [[] for _ in range(n)]
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)
    return g

def dfs(g, start):
    visited = [False] * len(g)
    order = []
    stack = [start]
    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        order.append(u)
        for v in g[u]:
            if not visited[v]:
                stack.append(v)
    return order
''', '''
import random
rng = random.Random(TASK_ID)
n_vertices = N
edges = [(rng.randint(0, n_vertices - 1), rng.randint(0, n_vertices - 1)) for _ in range(n_vertices * 3)]
g = build_graph(n_vertices, edges)
order = dfs(g, 0)
return checksum(order)
''')


# Task 94: Dijkstra
add_ds(94, "dijkstra_path", 1500, '''
import heapq as _hq

def build_weighted_graph(n, edges):
    g = [[] for _ in range(n)]
    for a, b, w in edges:
        g[a].append((b, w))
        g[b].append((a, w))
    return g

def dijkstra(g, src):
    n = len(g)
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = _hq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                _hq.heappush(pq, (nd, v))
    return dist
''', '''
import random
rng = random.Random(TASK_ID)
n_vertices = N
edges = [(rng.randint(0, n_vertices - 1), rng.randint(0, n_vertices - 1), rng.randint(1, 100))
         for _ in range(n_vertices * 4)]
g = build_weighted_graph(n_vertices, edges)
d = dijkstra(g, 0)
finite = [x for x in d if x != float('inf')]
return checksum(finite)
''')


# Task 95: Topological sort
add_ds(95, "topological_sort", 8000, '''
def build_dag(n, edges):
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in edges:
        if a < b:
            g[a].append(b)
            indeg[b] += 1
    return g, indeg

def topo_sort(n, g, indeg):
    queue = [i for i in range(n) if indeg[i] == 0]
    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return order
''', '''
import random
rng = random.Random(TASK_ID)
n_vertices = N
edges = [(rng.randint(0, n_vertices - 1), rng.randint(0, n_vertices - 1))
         for _ in range(n_vertices * 2)]
g, indeg = build_dag(n_vertices, edges)
order = topo_sort(n_vertices, g, indeg)
return checksum(order)
''')


# Task 96: Connected components
add_ds(96, "connected_components", 10000, '''
from collections import deque as _dq

def connected_components(n, adj):
    visited = [False] * n
    comps = []
    for start in range(n):
        if not visited[start]:
            comp = []
            q = _dq([start])
            visited[start] = True
            while q:
                u = q.popleft()
                comp.append(u)
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)
            comps.append(comp)
    return comps

def build_graph(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj
''', '''
import random
rng = random.Random(TASK_ID)
n_vertices = N
edges = [(rng.randint(0, n_vertices - 1), rng.randint(0, n_vertices - 1))
         for _ in range(n_vertices // 2)]
adj = build_graph(n_vertices, edges)
comps = connected_components(n_vertices, adj)
sizes = sorted([len(c) for c in comps])
return checksum(sizes)
''')


# Task 97: Cycle detection (directed)
add_ds(97, "cycle_detect", 6000, '''
def has_cycle(n, adj):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    def visit(u):
        if color[u] == GRAY:
            return True
        if color[u] == BLACK:
            return False
        color[u] = GRAY
        for v in adj[u]:
            if visit(v):
                return True
        color[u] = BLACK
        return False
    for i in range(n):
        if visit(i):
            return True
    return False

def build_directed(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
    return adj
''', '''
import sys
sys.setrecursionlimit(200000)
import random
rng = random.Random(TASK_ID)
results = []
for k in range(N):
    n_vertices = 100
    edges = [(rng.randint(0, n_vertices - 1), rng.randint(0, n_vertices - 1))
             for _ in range(n_vertices)]
    adj = build_directed(n_vertices, edges)
    results.append(1 if has_cycle(n_vertices, adj) else 0)
return checksum(results)
''')


# Task 98: Linked list reverse + merge
add_ds(98, "linked_list_reverse", 30000, '''
class Node:
    __slots__ = ('val', 'next')
    def __init__(self, v):
        self.val = v
        self.next = None

def build_list(vals):
    if not vals:
        return None
    head = Node(vals[0])
    cur = head
    for v in vals[1:]:
        cur.next = Node(v)
        cur = cur.next
    return head

def reverse(head):
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev

def merge_sorted(a, b):
    dummy = Node(0)
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out
''', '''
import random
rng = random.Random(TASK_ID)
results = []
for _ in range(N):
    a = build_list(sorted([rng.randint(0, 10000) for _ in range(50)]))
    b = build_list(sorted([rng.randint(0, 10000) for _ in range(50)]))
    merged = merge_sorted(a, b)
    rev = reverse(merged)
    results.extend(to_list(rev)[:10])
return checksum(results)
''')


# Task 99: Queue/Stack simulator
add_ds(99, "queue_stack_simulator", 500000, '''
from collections import deque as _dq

def simulate(ops):
    """Simulate a sequence of queue/stack operations."""
    q = _dq()
    stack = []
    results = []
    for op, val in ops:
        if op == 'enqueue':
            q.append(val)
        elif op == 'dequeue':
            results.append(q.popleft() if q else -1)
        elif op == 'push':
            stack.append(val)
        elif op == 'pop':
            results.append(stack.pop() if stack else -1)
    return results
''', '''
import random
rng = random.Random(TASK_ID)
op_types = ['enqueue', 'dequeue', 'push', 'pop']
ops = [(rng.choice(op_types), rng.randint(0, 10000)) for _ in range(N)]
results = simulate(ops)
return checksum(results)
''')


# Task 100: LRU cache
add_ds(100, "lru_cache", 200000, '''
class LRU:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}
        self.order = []
    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.cap:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)
''', '''
import random
rng = random.Random(TASK_ID)
lru = LRU(100)
results = []
for i in range(N):
    if rng.random() < 0.5:
        lru.put(rng.randint(0, 200), i)
    else:
        results.append(lru.get(rng.randint(0, 200)))
return checksum(results)
''')


assert len(REMAINING_TASKS) == 50, f"Expected 50, got {len(REMAINING_TASKS)}"

if __name__ == "__main__":
    for t in REMAINING_TASKS:
        print(f"Task {t.task_id:>3}: {t.name:<25} ({t.category}) N={t.n}")
