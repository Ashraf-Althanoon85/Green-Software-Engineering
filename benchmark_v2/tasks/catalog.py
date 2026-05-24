"""
Master task catalog - 100 computational tasks for benchmark v2.

Distribution:
  - 25 Sorting & Searching
  - 25 Parsing & String Processing
  - 20 Numerical Computing
  - 15 String Algorithms
  - 15 Data Structures & Graph Algorithms

Each task has:
  - id: pNN (matches v1_clean / v2_medium / v3_bad file names)
  - name: snake_case identifier
  - category: one of 5 categories
  - description: what the task computes
  - workload_size: tuned so V1 takes ~2-15 seconds
"""

TASKS = [
    # ========== SORTING & SEARCHING (25) ==========
    (1,  "bubble_sort",          "sorting", "Sort N integers using bubble sort"),
    (2,  "insertion_sort",       "sorting", "Sort N integers using insertion sort"),
    (3,  "selection_sort",       "sorting", "Sort N integers using selection sort"),
    (4,  "merge_sort",           "sorting", "Sort N integers using merge sort"),
    (5,  "quick_sort",           "sorting", "Sort N integers using quick sort"),
    (6,  "heap_sort",            "sorting", "Sort N integers using heap sort"),
    (7,  "counting_sort",        "sorting", "Sort N bounded integers using counting sort"),
    (8,  "radix_sort",           "sorting", "Sort N integers using LSD radix sort"),
    (9,  "shell_sort",           "sorting", "Sort N integers using shell sort"),
    (10, "binary_search",        "sorting", "Find K targets in sorted array of N"),
    (11, "ternary_search",       "sorting", "Find K targets via ternary search"),
    (12, "exponential_search",   "sorting", "Find K targets via exponential search"),
    (13, "jump_search",          "sorting", "Find K targets via jump search"),
    (14, "interpolation_search", "sorting", "Find K targets via interpolation search"),
    (15, "linear_scan_max",      "sorting", "Find max of N values across K passes"),
    (16, "kth_smallest",         "sorting", "K-th smallest via quickselect"),
    (17, "median_of_medians",    "sorting", "Median via deterministic selection"),
    (18, "topk_heap",            "sorting", "Top-K largest via min-heap"),
    (19, "bucket_sort",          "sorting", "Sort N floats using bucket sort"),
    (20, "comb_sort",            "sorting", "Sort N integers using comb sort"),
    (21, "cocktail_sort",        "sorting", "Sort N integers using cocktail sort"),
    (22, "gnome_sort",           "sorting", "Sort N integers using gnome sort"),
    (23, "pancake_sort",         "sorting", "Sort N integers using pancake sort"),
    (24, "stooge_sort",          "sorting", "Sort small array using stooge sort"),
    (25, "tim_sort_manual",      "sorting", "Sort N integers using simplified Timsort"),

    # ========== PARSING & STRING PROCESSING (25) ==========
    (26, "csv_parser",           "parsing", "Parse CSV with quotes/escapes, return row count and field sum"),
    (27, "json_flatten",         "parsing", "Flatten nested JSON object to dotted keys"),
    (28, "url_parser",           "parsing", "Parse URLs into components (scheme, host, path, query)"),
    (29, "ini_config_parser",    "parsing", "Parse INI config text"),
    (30, "log_line_parser",      "parsing", "Parse Apache-style log lines, count by status code"),
    (31, "email_extractor",      "parsing", "Extract emails from text using state machine"),
    (32, "tokenizer_simple",     "parsing", "Tokenize source-code-like text into tokens"),
    (33, "html_tag_stripper",    "parsing", "Strip HTML tags from text"),
    (34, "markdown_to_text",     "parsing", "Convert markdown to plain text"),
    (35, "query_string_parser",  "parsing", "Parse query strings with URL-decoding"),
    (36, "csv_to_json",          "parsing", "Convert CSV to list-of-dicts JSON"),
    (37, "xml_lite_parser",      "parsing", "Parse simple XML and count nested elements"),
    (38, "regex_match_count",    "parsing", "Count regex matches across many lines"),
    (39, "date_format_converter","parsing", "Convert dates between formats"),
    (40, "ipv4_validator",       "parsing", "Validate and parse IPv4 addresses"),
    (41, "color_hex_parser",     "parsing", "Parse hex colors to RGB tuples"),
    (42, "phone_normalizer",     "parsing", "Normalize phone numbers to E.164"),
    (43, "csv_aggregator",       "parsing", "Group-by aggregation on CSV columns"),
    (44, "config_merger",        "parsing", "Merge multiple key=value config strings"),
    (45, "diff_lines",           "parsing", "Compute simple line-by-line diff"),
    (46, "word_frequency",       "parsing", "Word frequency from large text"),
    (47, "sentence_splitter",    "parsing", "Split text into sentences"),
    (48, "csv_pivot",            "parsing", "Pivot CSV table"),
    (49, "json_path_resolver",   "parsing", "Resolve dotted-path queries on JSON"),
    (50, "template_renderer",    "parsing", "Render {{var}} templates"),

    # ========== NUMERICAL COMPUTING (20) ==========
    (51, "prime_sieve",          "numerical", "Sieve of Eratosthenes up to N"),
    (52, "fibonacci_dp",         "numerical", "Compute Fibonacci(N) iteratively"),
    (53, "matrix_multiply",      "numerical", "Multiply two NxN matrices"),
    (54, "matrix_transpose",     "numerical", "Transpose K NxN matrices"),
    (55, "dot_product_batch",    "numerical", "Compute dot product for K vector pairs"),
    (56, "monte_carlo_pi",       "numerical", "Estimate pi via Monte Carlo with N samples"),
    (57, "gcd_batch",            "numerical", "GCD of K integer pairs (Euclidean)"),
    (58, "modular_exponent",     "numerical", "Modular exponentiation for K queries"),
    (59, "newton_sqrt",          "numerical", "Square root via Newton's method for K values"),
    (60, "polynomial_eval",      "numerical", "Horner's method for K polynomials"),
    (61, "integral_simpson",     "numerical", "Numerical integration via Simpson's rule"),
    (62, "linear_regression",    "numerical", "Closed-form linear regression on N points"),
    (63, "kmeans_1d",            "numerical", "K-means on 1D points"),
    (64, "histogram_compute",    "numerical", "Build histogram of N values"),
    (65, "running_stats",        "numerical", "Online mean/variance for N stream values"),
    (66, "discrete_convolution", "numerical", "1D convolution of two arrays"),
    (67, "lcm_batch",            "numerical", "LCM of K integer pairs"),
    (68, "prime_factorization",  "numerical", "Factorize K integers"),
    (69, "catalan_numbers",      "numerical", "Compute first N Catalan numbers"),
    (70, "vector_norm",          "numerical", "L2 norm of K vectors"),

    # ========== STRING ALGORITHMS (15) ==========
    (71, "edit_distance",        "strings", "Levenshtein distance between K string pairs"),
    (72, "longest_common_sub",   "strings", "LCS of K string pairs"),
    (73, "kmp_search",           "strings", "KMP substring search"),
    (74, "rabin_karp",           "strings", "Rabin-Karp substring search"),
    (75, "z_algorithm",          "strings", "Z-function for K strings"),
    (76, "manacher_palindrome",  "strings", "Longest palindromic substring (Manacher)"),
    (77, "suffix_array_naive",   "strings", "Build suffix array for K strings"),
    (78, "anagram_groups",       "strings", "Group anagrams from N words"),
    (79, "longest_repeated_sub", "strings", "Longest repeated substring"),
    (80, "boyer_moore_lite",     "strings", "Boyer-Moore substring search (bad-char)"),
    (81, "string_rotation",      "strings", "Check string rotation for K pairs"),
    (82, "run_length_encoding",  "strings", "RLE encode/decode K strings"),
    (83, "soundex",              "strings", "Soundex codes for N names"),
    (84, "longest_prefix",       "strings", "Longest common prefix of N strings"),
    (85, "palindrome_partition", "strings", "Min palindrome partitions of K strings"),

    # ========== DATA STRUCTURES & GRAPHS (15) ==========
    (86, "bst_operations",       "ds_graph", "BST insert/search/delete N keys"),
    (87, "avl_tree_ops",         "ds_graph", "AVL tree insert/lookup N keys"),
    (88, "heap_operations",      "ds_graph", "Heap push/pop on N elements"),
    (89, "hashmap_chaining",     "ds_graph", "Hash table with chaining, N ops"),
    (90, "trie_operations",      "ds_graph", "Trie insert/prefix-search N words"),
    (91, "union_find",           "ds_graph", "Union-Find with path compression, N ops"),
    (92, "bfs_traversal",        "ds_graph", "BFS over generated graph (V vertices)"),
    (93, "dfs_traversal",        "ds_graph", "DFS over generated graph"),
    (94, "dijkstra_path",        "ds_graph", "Dijkstra shortest path from source"),
    (95, "topological_sort",     "ds_graph", "Topological sort of DAG"),
    (96, "connected_components", "ds_graph", "Connected components via BFS"),
    (97, "cycle_detect",         "ds_graph", "Detect cycle in directed graph"),
    (98, "linked_list_reverse",  "ds_graph", "Reverse and merge K linked lists"),
    (99, "queue_stack_simulator","ds_graph", "Simulate N queue/stack operations"),
    (100,"lru_cache",            "ds_graph", "LRU cache with N hit/miss ops"),
]

assert len(TASKS) == 100
assert all(t[0] == i + 1 for i, t in enumerate(TASKS))

CATEGORIES = {
    "sorting":   25,
    "parsing":   25,
    "numerical": 20,
    "strings":   15,
    "ds_graph":  15,
}

for cat, expected in CATEGORIES.items():
    actual = sum(1 for t in TASKS if t[2] == cat)
    assert actual == expected, f"{cat}: expected {expected}, got {actual}"

if __name__ == "__main__":
    print(f"Total tasks: {len(TASKS)}")
    for cat, count in CATEGORIES.items():
        print(f"  {cat:12s}: {count}")
