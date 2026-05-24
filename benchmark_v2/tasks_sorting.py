"""25 sorting & searching tasks. Only clean_body provided; medium and bad auto-generated."""

from builder import Task

SORTING_TASKS = []

def add(task_id, name, n, clean_body, main_body):
    SORTING_TASKS.append(Task(task_id, name, "sorting", n, clean_body, main_body))


# Task 1: Bubble sort
add(1, "bubble_sort", 4000, '''
def bubble_sort(arr):
    """Sort using bubble sort."""
    result = list(arr)
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(bubble_sort(data))
''')


# Task 2: Insertion sort
add(2, "insertion_sort", 6000, '''
def insertion_sort(arr):
    """Sort using insertion sort."""
    result = list(arr)
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(insertion_sort(data))
''')


# Task 3: Selection sort
add(3, "selection_sort", 4500, '''
def selection_sort(arr):
    """Sort using selection sort."""
    result = list(arr)
    n = len(result)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(selection_sort(data))
''')


# Task 4: Merge sort
add(4, "merge_sort", 200000, '''
def merge_sort(arr):
    """Sort using merge sort."""
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result
''', '''
import sys
sys.setrecursionlimit(300000)
data = get_int_array(TASK_ID, N)
return checksum(merge_sort(data))
''')


# Task 5: Quick sort
add(5, "quick_sort", 150000, '''
def quick_sort(arr):
    """Sort using quick sort (in-place)."""
    result = list(arr)
    _qs(result, 0, len(result) - 1)
    return result

def _qs(a, lo, hi):
    if lo < hi:
        p = _partition(a, lo, hi)
        _qs(a, lo, p - 1)
        _qs(a, p + 1, hi)

def _partition(a, lo, hi):
    mid_idx = (lo + hi) // 2
    a[mid_idx], a[hi] = a[hi], a[mid_idx]
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i
''', '''
import sys
sys.setrecursionlimit(300000)
data = get_int_array(TASK_ID, N)
return checksum(quick_sort(data))
''')


# Task 6: Heap sort
add(6, "heap_sort", 100000, '''
def heap_sort(arr):
    """Sort using heap sort."""
    result = list(arr)
    n = len(result)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(result, n, i)
    for i in range(n - 1, 0, -1):
        result[0], result[i] = result[i], result[0]
        _heapify(result, i, 0)
    return result

def _heapify(a, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and a[left] > a[largest]:
        largest = left
    if right < n and a[right] > a[largest]:
        largest = right
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        _heapify(a, n, largest)
''', '''
import sys
sys.setrecursionlimit(300000)
data = get_int_array(TASK_ID, N)
return checksum(heap_sort(data))
''')


# Task 7: Counting sort
add(7, "counting_sort", 500000, '''
def counting_sort(arr):
    """Sort using counting sort (assumes non-negative ints)."""
    if not arr:
        return []
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1
    result = []
    for v in range(max_val + 1):
        for _ in range(count[v]):
            result.append(v)
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(counting_sort(data))
''')


# Task 8: Radix sort
add(8, "radix_sort", 200000, '''
def radix_sort(arr):
    """Sort using LSD radix sort."""
    result = list(arr)
    if not result:
        return result
    max_val = max(result)
    exp = 1
    while max_val // exp > 0:
        result = _counting_sort_by_digit(result, exp)
        exp *= 10
    return result

def _counting_sort_by_digit(a, exp):
    n = len(a)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        d = (a[i] // exp) % 10
        count[d] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        d = (a[i] // exp) % 10
        output[count[d] - 1] = a[i]
        count[d] -= 1
    return output
''', '''
data = get_int_array(TASK_ID, N)
return checksum(radix_sort(data))
''')


# Task 9: Shell sort
add(9, "shell_sort", 50000, '''
def shell_sort(arr):
    """Sort using shell sort."""
    result = list(arr)
    n = len(result)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = result[i]
            j = i
            while j >= gap and result[j - gap] > temp:
                result[j] = result[j - gap]
                j -= gap
            result[j] = temp
        gap //= 2
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(shell_sort(data))
''')


# Task 10: Binary search batch
add(10, "binary_search", 50, '''
def binary_search(arr, target):
    """Return index of target or -1."""
    lo = 0
    hi = len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def search_many(arr, targets):
    """Return indices for each target."""
    results = []
    for t in targets:
        results.append(binary_search(arr, t))
    return results
''', '''
data = sorted(get_int_array(TASK_ID, 500000))
targets = get_int_array(TASK_ID, N, seed_offset=1)
# Repeat lookups to fill time budget
all_results = []
for _ in range(20000):
    all_results.extend(search_many(data, targets))
return checksum(all_results)
''')


# Task 11: Ternary search batch
add(11, "ternary_search", 40, '''
def ternary_search(arr, target):
    """Return index of target or -1 using ternary search."""
    lo = 0
    hi = len(arr) - 1
    while lo <= hi:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3
        if arr[m1] == target:
            return m1
        if arr[m2] == target:
            return m2
        if target < arr[m1]:
            hi = m1 - 1
        elif target > arr[m2]:
            lo = m2 + 1
        else:
            lo = m1 + 1
            hi = m2 - 1
    return -1

def search_many(arr, targets):
    results = []
    for t in targets:
        results.append(ternary_search(arr, t))
    return results
''', '''
data = sorted(get_int_array(TASK_ID, 400000))
targets = get_int_array(TASK_ID, N, seed_offset=1)
all_results = []
for _ in range(15000):
    all_results.extend(search_many(data, targets))
return checksum(all_results)
''')


# Task 12: Exponential search
add(12, "exponential_search", 40, '''
def exponential_search(arr, target):
    """Find target using exponential search."""
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0
    bound = 1
    while bound < n and arr[bound] < target:
        bound *= 2
    lo = bound // 2
    hi = min(bound, n - 1)
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def search_many(arr, targets):
    return [exponential_search(arr, t) for t in targets]
''', '''
data = sorted(get_int_array(TASK_ID, 300000))
targets = get_int_array(TASK_ID, N, seed_offset=1)
all_results = []
for _ in range(15000):
    all_results.extend(search_many(data, targets))
return checksum(all_results)
''')


# Task 13: Jump search
add(13, "jump_search", 40, '''
import math as _math

def jump_search(arr, target):
    """Find target using jump search."""
    n = len(arr)
    if n == 0:
        return -1
    block = max(1, int(_math.sqrt(n)))
    prev = 0
    step = block
    while step < n and arr[step - 1] < target:
        prev = step
        step += block
    end = min(step, n)
    while prev < end:
        if arr[prev] == target:
            return prev
        prev += 1
    return -1

def search_many(arr, targets):
    return [jump_search(arr, t) for t in targets]
''', '''
data = sorted(get_int_array(TASK_ID, 200000))
targets = get_int_array(TASK_ID, N, seed_offset=1)
all_results = []
for _ in range(10000):
    all_results.extend(search_many(data, targets))
return checksum(all_results)
''')


# Task 14: Interpolation search
add(14, "interpolation_search", 40, '''
def interpolation_search(arr, target):
    """Find target via interpolation search."""
    lo = 0
    hi = len(arr) - 1
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if arr[hi] == arr[lo]:
            if arr[lo] == target:
                return lo
            return -1
        pos = lo + ((hi - lo) * (target - arr[lo])) // (arr[hi] - arr[lo])
        if pos < 0 or pos >= len(arr):
            return -1
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1

def search_many(arr, targets):
    return [interpolation_search(arr, t) for t in targets]
''', '''
data = sorted(get_int_array(TASK_ID, 400000))
targets = get_int_array(TASK_ID, N, seed_offset=1)
all_results = []
for _ in range(15000):
    all_results.extend(search_many(data, targets))
return checksum(all_results)
''')


# Task 15: Linear scan max (multiple passes)
add(15, "linear_scan_max", 800, '''
def find_max(arr):
    """Find max value via linear scan."""
    m = arr[0]
    for x in arr[1:]:
        if x > m:
            m = x
    return m

def find_max_k_passes(arr, k):
    """Run find_max k times (simulating repeated queries)."""
    results = []
    for _ in range(k):
        results.append(find_max(arr))
    return results
''', '''
data = get_int_array(TASK_ID, 100000)
return checksum(find_max_k_passes(data, N))
''')


# Task 16: K-th smallest via quickselect
add(16, "kth_smallest", 1500, '''
def quickselect(arr, k):
    """Return the k-th smallest element (0-indexed)."""
    a = list(arr)
    lo = 0
    hi = len(a) - 1
    while lo < hi:
        p = _partition(a, lo, hi)
        if p == k:
            return a[p]
        elif p < k:
            lo = p + 1
        else:
            hi = p - 1
    return a[lo]

def _partition(a, lo, hi):
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i

def many_queries(arr, ks):
    return [quickselect(arr, k) for k in ks]
''', '''
data = get_int_array(TASK_ID, 5000)
ks = [(i * 7) % 5000 for i in range(N)]
return checksum(many_queries(data, ks))
''')


# Task 17: Median of medians (deterministic selection)
add(17, "median_of_medians", 80, '''
def select_median(arr, k):
    """Median of medians selection."""
    if len(arr) <= 5:
        return sorted(arr)[k]
    chunks = [sorted(arr[i:i+5]) for i in range(0, len(arr), 5)]
    medians = [c[len(c)//2] for c in chunks]
    pivot = select_median(medians, len(medians) // 2)
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]
    if k < len(lows):
        return select_median(lows, k)
    elif k < len(lows) + len(pivots):
        return pivot
    else:
        return select_median(highs, k - len(lows) - len(pivots))

def many_queries(arr, ks):
    return [select_median(arr, k) for k in ks]
''', '''
import sys
sys.setrecursionlimit(200000)
data = get_int_array(TASK_ID, 1000)
ks = [(i * 7) % 1000 for i in range(N)]
return checksum(many_queries(data, ks))
''')


# Task 18: Top-K via heap
add(18, "topk_heap", 50, '''
import heapq as _hq

def top_k(arr, k):
    """Return top-k largest elements (sorted desc)."""
    if k <= 0:
        return []
    heap = arr[:k]
    _hq.heapify(heap)
    for x in arr[k:]:
        if x > heap[0]:
            _hq.heapreplace(heap, x)
    return sorted(heap, reverse=True)

def many_queries(arr, ks):
    return [top_k(arr, k) for k in ks]
''', '''
data = get_int_array(TASK_ID, 100000)
ks = [50, 100, 200, 500, 1000] * N
return checksum(many_queries(data, ks))
''')


# Task 19: Bucket sort
add(19, "bucket_sort", 200000, '''
def bucket_sort(arr):
    """Sort floats in [0,1) range using bucket sort. Normalizes arbitrary floats."""
    if not arr:
        return []
    n = len(arr)
    min_v = min(arr)
    max_v = max(arr)
    if max_v == min_v:
        return list(arr)
    buckets = [[] for _ in range(n)]
    for x in arr:
        idx = int((x - min_v) / (max_v - min_v) * (n - 1))
        buckets[idx].append(x)
    result = []
    for b in buckets:
        b.sort()
        result.extend(b)
    return result
''', '''
data = get_float_array(TASK_ID, N)
return checksum(bucket_sort(data))
''')


# Task 20: Comb sort
add(20, "comb_sort", 20000, '''
def comb_sort(arr):
    """Sort using comb sort."""
    result = list(arr)
    n = len(result)
    gap = n
    shrink = 1.3
    sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        i = 0
        while i + gap < n:
            if result[i] > result[i + gap]:
                result[i], result[i + gap] = result[i + gap], result[i]
                sorted_flag = False
            i += 1
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(comb_sort(data))
''')


# Task 21: Cocktail sort
add(21, "cocktail_sort", 3000, '''
def cocktail_sort(arr):
    """Sort using cocktail (bidirectional bubble) sort."""
    result = list(arr)
    n = len(result)
    start = 0
    end = n - 1
    swapped = True
    while swapped:
        swapped = False
        for i in range(start, end):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        start += 1
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(cocktail_sort(data))
''')


# Task 22: Gnome sort
add(22, "gnome_sort", 3500, '''
def gnome_sort(arr):
    """Sort using gnome sort."""
    result = list(arr)
    i = 0
    n = len(result)
    while i < n:
        if i == 0 or result[i - 1] <= result[i]:
            i += 1
        else:
            result[i], result[i - 1] = result[i - 1], result[i]
            i -= 1
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(gnome_sort(data))
''')


# Task 23: Pancake sort
add(23, "pancake_sort", 1500, '''
def pancake_sort(arr):
    """Sort using pancake sort (flip operations)."""
    result = list(arr)
    n = len(result)
    for size in range(n, 1, -1):
        max_idx = 0
        for i in range(1, size):
            if result[i] > result[max_idx]:
                max_idx = i
        if max_idx != size - 1:
            _flip(result, max_idx + 1)
            _flip(result, size)
    return result

def _flip(a, k):
    lo = 0
    hi = k - 1
    while lo < hi:
        a[lo], a[hi] = a[hi], a[lo]
        lo += 1
        hi -= 1
''', '''
data = get_int_array(TASK_ID, N)
return checksum(pancake_sort(data))
''')


# Task 24: Stooge sort
add(24, "stooge_sort", 300, '''
def stooge_sort(arr):
    """Sort using stooge sort."""
    result = list(arr)
    _stooge(result, 0, len(result) - 1)
    return result

def _stooge(a, lo, hi):
    if lo >= hi:
        return
    if a[lo] > a[hi]:
        a[lo], a[hi] = a[hi], a[lo]
    if hi - lo + 1 > 2:
        t = (hi - lo + 1) // 3
        _stooge(a, lo, hi - t)
        _stooge(a, lo + t, hi)
        _stooge(a, lo, hi - t)
''', '''
import sys
sys.setrecursionlimit(200000)
data = get_int_array(TASK_ID, N)
return checksum(stooge_sort(data))
''')


# Task 25: Simplified TimSort
add(25, "tim_sort_manual", 100000, '''
RUN = 32

def insertion_run(arr, lo, hi):
    for i in range(lo + 1, hi + 1):
        key = arr[i]
        j = i - 1
        while j >= lo and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_run(arr, lo, mid, hi):
    left = arr[lo:mid + 1]
    right = arr[mid + 1:hi + 1]
    i = 0
    j = 0
    k = lo
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

def tim_sort(arr):
    """Sort using simplified Timsort."""
    result = list(arr)
    n = len(result)
    for start in range(0, n, RUN):
        insertion_run(result, start, min(start + RUN - 1, n - 1))
    size = RUN
    while size < n:
        for start in range(0, n, 2 * size):
            mid = min(start + size - 1, n - 1)
            end = min(start + 2 * size - 1, n - 1)
            if mid < end:
                merge_run(result, start, mid, end)
        size *= 2
    return result
''', '''
data = get_int_array(TASK_ID, N)
return checksum(tim_sort(data))
''')


assert len(SORTING_TASKS) == 25, f"Expected 25, got {len(SORTING_TASKS)}"

if __name__ == "__main__":
    for t in SORTING_TASKS:
        print(f"Task {t.task_id:>3}: {t.name:<25} N={t.n}")
