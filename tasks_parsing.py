"""25 parsing & string-processing tasks."""

from builder import Task

PARSING_TASKS = []

def add(task_id, name, n, clean_body, main_body):
    PARSING_TASKS.append(Task(task_id, name, "parsing", n, clean_body, main_body))


# Task 26: CSV parser
add(26, "csv_parser", 500, '''
def parse_csv_line(line):
    """Parse single CSV line (handles quotes)."""
    fields = []
    cur = []
    in_quote = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == '"':
            if in_quote and i + 1 < len(line) and line[i + 1] == '"':
                cur.append('"')
                i += 2
                continue
            in_quote = not in_quote
        elif c == ',' and not in_quote:
            fields.append(''.join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    fields.append(''.join(cur))
    return fields

def parse_csv(text):
    """Parse CSV text into list of rows."""
    rows = []
    for line in text.split('\\n'):
        if line:
            rows.append(parse_csv_line(line))
    return rows

def make_csv(n):
    lines = []
    for i in range(n):
        lines.append(f'"row{i}",{i*7 % 1000},"text,{i}","quoted ""value""",{i*13}')
    return '\\n'.join(lines)
''', '''
text = make_csv(N * 200)
rows = parse_csv(text)
flat = [f for row in rows for f in row]
return checksum(flat)
''')


# Task 27: JSON flatten
add(27, "json_flatten", 5000, '''
def flatten(obj, prefix=""):
    """Flatten nested dict/list to dotted keys."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (dict, list)):
                out.update(flatten(v, key))
            else:
                out[key] = v
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            key = f"{prefix}[{i}]"
            if isinstance(v, (dict, list)):
                out.update(flatten(v, key))
            else:
                out[key] = v
    else:
        out[prefix] = obj
    return out

def make_nested(depth, fan):
    if depth == 0:
        return 42
    return {f"k{i}": make_nested(depth - 1, fan) for i in range(fan)}
''', '''
import sys
sys.setrecursionlimit(100000)
results = []
for _ in range(N):
    obj = make_nested(4, 5)
    flat = flatten(obj)
    results.append(len(flat))
return checksum(results)
''')


# Task 28: URL parser
add(28, "url_parser", 1500, '''
def parse_url(url):
    """Parse URL into (scheme, host, port, path, query)."""
    scheme = ""
    if "://" in url:
        scheme, rest = url.split("://", 1)
    else:
        rest = url
    host = ""
    port = 0
    path = "/"
    query = ""
    if "?" in rest:
        rest, query = rest.split("?", 1)
    if "/" in rest:
        host_part, path = rest.split("/", 1)
        path = "/" + path
    else:
        host_part = rest
    if ":" in host_part:
        host, port_s = host_part.split(":", 1)
        try:
            port = int(port_s)
        except ValueError:
            port = 0
    else:
        host = host_part
    return (scheme, host, port, path, query)

def parse_many(urls):
    return [parse_url(u) for u in urls]

def make_urls(n):
    return [
        f"https://host{i % 100}.example.com:{8000 + i % 100}/path/to/resource{i}?key{i}=val{i}&q={i*7}"
        for i in range(n)
    ]
''', '''
urls = make_urls(N * 100)
results = parse_many(urls)
return checksum(results)
''')


# Task 29: INI config parser
add(29, "ini_config_parser", 2000, '''
def parse_ini(text):
    """Parse INI text into dict-of-dicts."""
    result = {}
    section = "DEFAULT"
    result[section] = {}
    for raw in text.split('\\n'):
        line = raw.strip()
        if not line or line.startswith('#') or line.startswith(';'):
            continue
        if line.startswith('[') and line.endswith(']'):
            section = line[1:-1]
            result[section] = {}
        elif '=' in line:
            key, val = line.split('=', 1)
            result[section][key.strip()] = val.strip()
    return result

def make_ini(n):
    parts = []
    for s in range(n // 50):
        parts.append(f"[section{s}]")
        for k in range(50):
            parts.append(f"key{k} = value{s}_{k}")
        parts.append("")
    return '\\n'.join(parts)
''', '''
text = make_ini(N * 50)
parsed = parse_ini(text)
sizes = [len(v) for v in parsed.values()]
return checksum(sizes)
''')


# Task 30: Log line parser
add(30, "log_line_parser", 200, '''
def parse_log_line(line):
    """Parse Apache-style log line: IP - - [date] "method URL proto" status size."""
    parts = line.split(' ')
    if len(parts) < 9:
        return None
    return {
        'ip': parts[0],
        'method': parts[5].lstrip('"'),
        'url': parts[6],
        'status': int(parts[8]) if parts[8].isdigit() else 0,
    }

def count_status_codes(lines):
    counts = {}
    for line in lines:
        rec = parse_log_line(line)
        if rec:
            s = rec['status']
            counts[s] = counts.get(s, 0) + 1
    return counts

def make_logs(n):
    statuses = [200, 200, 200, 301, 404, 500]
    methods = ['GET', 'POST', 'PUT']
    return [
        f'192.168.1.{i % 256} - - [10/Oct/2024:13:55:36 +0000] "{methods[i%3]} /path/{i} HTTP/1.1" {statuses[i%6]} {i*7}'
        for i in range(n)
    ]
''', '''
logs = make_logs(N * 5000)
counts = count_status_codes(logs)
return checksum(list(counts.items()))
''')


# Task 31: Email extractor
add(31, "email_extractor", 500, '''
def extract_emails(text):
    """Extract emails using a simple state machine."""
    emails = []
    n = len(text)
    i = 0
    while i < n:
        if text[i] == '@':
            # Walk back to start of local part
            start = i - 1
            while start >= 0 and (text[start].isalnum() or text[start] in '._-+'):
                start -= 1
            start += 1
            # Walk forward to find domain
            end = i + 1
            while end < n and (text[end].isalnum() or text[end] in '.-'):
                end += 1
            if start < i and end > i + 1 and '.' in text[i+1:end]:
                emails.append(text[start:end])
            i = end
        else:
            i += 1
    return emails

def make_text(n):
    parts = []
    for i in range(n):
        parts.append(f"Contact user{i}@example{i%50}.com about issue {i}. Also see admin_{i}@test.org for details.")
    return ' '.join(parts)
''', '''
text = make_text(N * 20)
emails = extract_emails(text)
return checksum(emails)
''')


# Task 32: Tokenizer
add(32, "tokenizer_simple", 300, '''
def tokenize(text):
    """Tokenize text into identifiers, numbers, operators, strings."""
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
        elif c.isalpha() or c == '_':
            start = i
            while i < n and (text[i].isalnum() or text[i] == '_'):
                i += 1
            tokens.append(('ID', text[start:i]))
        elif c.isdigit():
            start = i
            while i < n and text[i].isdigit():
                i += 1
            tokens.append(('NUM', text[start:i]))
        elif c == '"':
            start = i
            i += 1
            while i < n and text[i] != '"':
                i += 1
            i += 1
            tokens.append(('STR', text[start:i]))
        else:
            tokens.append(('OP', c))
            i += 1
    return tokens

def make_code(n):
    return ' '.join([f'x{i} = func{i}(y{i}, "str{i}") + {i*7}' for i in range(n)])
''', '''
code = make_code(N * 200)
tokens = tokenize(code)
return checksum([t[1] for t in tokens])
''')


# Task 33: HTML tag stripper
add(33, "html_tag_stripper", 400, '''
def strip_tags(html):
    """Remove HTML tags, keep text content."""
    out = []
    in_tag = False
    for c in html:
        if c == '<':
            in_tag = True
        elif c == '>':
            in_tag = False
        elif not in_tag:
            out.append(c)
    return ''.join(out)

def make_html(n):
    parts = []
    for i in range(n):
        parts.append(f'<div class="item{i}"><p>Text{i} <b>bold{i}</b></p></div>')
    return ''.join(parts)
''', '''
html = make_html(N * 800)
stripped = strip_tags(html)
return checksum(list(stripped[::100]))
''')


# Task 34: Markdown to text
add(34, "markdown_to_text", 600, '''
def md_to_text(md):
    """Convert markdown to plain text."""
    out = []
    for line in md.split('\\n'):
        s = line.strip()
        # Strip headers
        while s.startswith('#'):
            s = s[1:].lstrip()
        # Strip bold/italic
        s = s.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
        # Strip links [text](url)
        result = []
        i = 0
        while i < len(s):
            if s[i] == '[':
                end_text = s.find(']', i)
                end_url = s.find(')', end_text) if end_text != -1 else -1
                if end_text != -1 and end_url != -1:
                    result.append(s[i+1:end_text])
                    i = end_url + 1
                    continue
            result.append(s[i])
            i += 1
        out.append(''.join(result))
    return '\\n'.join(out)

def make_md(n):
    parts = []
    for i in range(n):
        parts.append(f"# Header {i}")
        parts.append(f"This is **bold {i}** and *italic {i}* with [link{i}](http://x.com/{i})")
        parts.append("")
    return '\\n'.join(parts)
''', '''
md = make_md(N * 100)
text = md_to_text(md)
return checksum(list(text[::50]))
''')


# Task 35: Query string parser
add(35, "query_string_parser", 2000, '''
def percent_decode(s):
    """Decode percent-encoded string."""
    out = []
    i = 0
    while i < len(s):
        if s[i] == '%' and i + 2 < len(s):
            try:
                out.append(chr(int(s[i+1:i+3], 16)))
                i += 3
                continue
            except ValueError:
                pass
        elif s[i] == '+':
            out.append(' ')
        else:
            out.append(s[i])
        i += 1
    return ''.join(out)

def parse_qs(qs):
    """Parse query string into dict."""
    result = {}
    if qs.startswith('?'):
        qs = qs[1:]
    for pair in qs.split('&'):
        if not pair:
            continue
        if '=' in pair:
            k, v = pair.split('=', 1)
            result[percent_decode(k)] = percent_decode(v)
        else:
            result[percent_decode(pair)] = ''
    return result

def make_qs(n):
    return [f"key{i}=value%20{i}&q=hello%2Bworld&n={i}" for i in range(n)]
''', '''
qs_list = make_qs(N * 100)
parsed = [parse_qs(qs) for qs in qs_list]
sizes = [len(p) for p in parsed]
return checksum(sizes)
''')


# Task 36: CSV to JSON
add(36, "csv_to_json", 500, '''
def csv_to_json(text):
    """Convert CSV (first line headers) to list of dicts."""
    lines = text.split('\\n')
    if not lines:
        return []
    headers = lines[0].split(',')
    result = []
    for line in lines[1:]:
        if not line:
            continue
        values = line.split(',')
        row = {}
        for i, h in enumerate(headers):
            row[h] = values[i] if i < len(values) else ''
        result.append(row)
    return result

def make_csv(n):
    parts = ["id,name,value,category"]
    for i in range(n):
        parts.append(f"{i},name{i},{i*7},cat{i%10}")
    return '\\n'.join(parts)
''', '''
text = make_csv(N * 200)
rows = csv_to_json(text)
ids = [int(r['id']) for r in rows]
return checksum(ids)
''')


# Task 37: XML lite parser
add(37, "xml_lite_parser", 500, '''
def parse_xml(text):
    """Parse simple XML, return tree as nested dicts."""
    pos = [0]
    return _parse_node(text, pos)

def _parse_node(text, pos):
    while pos[0] < len(text) and text[pos[0]] != '<':
        pos[0] += 1
    if pos[0] >= len(text):
        return None
    pos[0] += 1
    end_tag = text.find('>', pos[0])
    if end_tag == -1:
        return None
    tag = text[pos[0]:end_tag].strip().split()[0]
    pos[0] = end_tag + 1
    children = []
    while pos[0] < len(text):
        if text[pos[0]] == '<':
            if pos[0] + 1 < len(text) and text[pos[0]+1] == '/':
                close_end = text.find('>', pos[0])
                pos[0] = close_end + 1
                return {'tag': tag, 'children': children}
            child = _parse_node(text, pos)
            if child:
                children.append(child)
        else:
            pos[0] += 1
    return {'tag': tag, 'children': children}

def count_nodes(node):
    if node is None:
        return 0
    return 1 + sum(count_nodes(c) for c in node.get('children', []))

def make_xml(depth, fan):
    if depth == 0:
        return "<leaf>x</leaf>"
    inner = ''.join(make_xml(depth - 1, fan) for _ in range(fan))
    return f"<n>{inner}</n>"
''', '''
import sys
sys.setrecursionlimit(100000)
results = []
for _ in range(N):
    xml = make_xml(5, 3)
    tree = parse_xml(xml)
    results.append(count_nodes(tree))
return checksum(results)
''')


# Task 38: Regex match count
add(38, "regex_match_count", 200, '''
import re as _re

def count_matches(pattern, lines):
    """Count regex matches across lines."""
    rx = _re.compile(pattern)
    total = 0
    for line in lines:
        total += len(rx.findall(line))
    return total

def make_lines(n):
    return [
        f"User user{i} logged in at {i % 24}:{i % 60}:{i % 60} from IP 10.0.{i % 256}.{(i*7) % 256}"
        for i in range(n)
    ]
''', '''
lines = make_lines(N * 100)
patterns = [r'user\\d+', r'\\d+:\\d+:\\d+', r'IP\\s+[\\d.]+', r'\\b[a-z]{2,5}\\b']
counts = [count_matches(p, lines) for p in patterns]
return checksum(counts)
''')


# Task 39: Date format converter
add(39, "date_format_converter", 5000, '''
def parse_iso(s):
    """Parse YYYY-MM-DD."""
    parts = s.split('-')
    return (int(parts[0]), int(parts[1]), int(parts[2]))

def format_us(y, m, d):
    """Format as MM/DD/YYYY."""
    return f"{m:02d}/{d:02d}/{y}"

def format_eu(y, m, d):
    """Format as DD.MM.YYYY."""
    return f"{d:02d}.{m:02d}.{y}"

def convert_dates(dates, fmt):
    out = []
    for s in dates:
        y, m, d = parse_iso(s)
        if fmt == 'us':
            out.append(format_us(y, m, d))
        else:
            out.append(format_eu(y, m, d))
    return out

def make_dates(n):
    return [f"{2000 + i % 25}-{1 + i % 12:02d}-{1 + i % 28:02d}" for i in range(n)]
''', '''
dates = make_dates(N * 50)
us = convert_dates(dates, 'us')
eu = convert_dates(dates, 'eu')
return checksum(us + eu)
''')


# Task 40: IPv4 validator
add(40, "ipv4_validator", 5000, '''
def parse_ipv4(s):
    """Validate and parse IPv4. Returns tuple of 4 ints or None."""
    parts = s.split('.')
    if len(parts) != 4:
        return None
    nums = []
    for p in parts:
        if not p or not p.isdigit():
            return None
        n = int(p)
        if n < 0 or n > 255:
            return None
        nums.append(n)
    return tuple(nums)

def parse_many(ips):
    return [parse_ipv4(s) for s in ips if parse_ipv4(s) is not None]

def make_ips(n):
    return [f"{i % 256}.{(i*7) % 256}.{(i*13) % 256}.{(i*19) % 256}" for i in range(n)]
''', '''
ips = make_ips(N * 100)
parsed = parse_many(ips)
return checksum(parsed)
''')


# Task 41: Color hex parser
add(41, "color_hex_parser", 8000, '''
def parse_hex(s):
    """Parse #RRGGBB or #RGB to (r, g, b)."""
    if s.startswith('#'):
        s = s[1:]
    if len(s) == 3:
        return (int(s[0]*2, 16), int(s[1]*2, 16), int(s[2]*2, 16))
    if len(s) == 6:
        return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
    return (0, 0, 0)

def parse_many(colors):
    return [parse_hex(c) for c in colors]

def make_colors(n):
    return [f"#{(i*7919) % 0xFFFFFF:06x}" for i in range(n)]
''', '''
colors = make_colors(N * 100)
parsed = parse_many(colors)
return checksum(parsed)
''')


# Task 42: Phone normalizer
add(42, "phone_normalizer", 5000, '''
def normalize_phone(s):
    """Normalize phone number to E.164 (digits-only with optional +)."""
    out = []
    if s.startswith('+'):
        out.append('+')
    for c in s:
        if c.isdigit():
            out.append(c)
    return ''.join(out)

def normalize_many(phones):
    return [normalize_phone(p) for p in phones]

def make_phones(n):
    formats = [
        "+1 (555) {n:03d}-{m:04d}",
        "(555) {n:03d}.{m:04d}",
        "555-{n:03d}-{m:04d}",
        "+44 20 {n:04d} {m:04d}",
    ]
    return [formats[i % 4].format(n=i % 1000, m=(i * 7) % 10000) for i in range(n)]
''', '''
phones = make_phones(N * 100)
normalized = normalize_many(phones)
return checksum(normalized)
''')


# Task 43: CSV aggregator (group-by)
add(43, "csv_aggregator", 300, '''
def aggregate(rows, group_col, value_col):
    """Sum value_col grouped by group_col."""
    result = {}
    for row in rows:
        if len(row) <= max(group_col, value_col):
            continue
        key = row[group_col]
        try:
            val = float(row[value_col])
        except ValueError:
            continue
        result[key] = result.get(key, 0.0) + val
    return result

def make_rows(n):
    return [(f"cat{i % 100}", str(i % 1000), f"name{i}", str(i * 1.5)) for i in range(n)]
''', '''
rows = make_rows(N * 500)
result = aggregate(rows, 0, 3)
items = sorted(result.items())
return checksum(items)
''')


# Task 44: Config merger
add(44, "config_merger", 8000, '''
def parse_kv(s):
    """Parse key=value pairs separated by ;."""
    result = {}
    for pair in s.split(';'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            result[k.strip()] = v.strip()
    return result

def merge_configs(configs):
    result = {}
    for c in configs:
        d = parse_kv(c)
        for k, v in d.items():
            result[k] = v
    return result

def make_configs(n):
    return [f"key{i % 100}=val{i}; common=shared{i}; flag{i % 50}=on" for i in range(n)]
''', '''
configs = make_configs(N * 50)
merged = merge_configs(configs)
return checksum(sorted(merged.items()))
''')


# Task 45: Diff lines
add(45, "diff_lines", 100, '''
def diff_lines(a, b):
    """Return list of operations: ('eq', l), ('add', l), ('del', l)."""
    m, n = len(a), len(b)
    # LCS DP
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])
    # Backtrack
    ops = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i-1] == b[j-1]:
            ops.append(('eq', a[i-1]))
            i -= 1; j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            ops.append(('del', a[i-1]))
            i -= 1
        else:
            ops.append(('add', b[j-1]))
            j -= 1
    while i > 0:
        ops.append(('del', a[i-1]))
        i -= 1
    while j > 0:
        ops.append(('add', b[j-1]))
        j -= 1
    return list(reversed(ops))

def make_lines(n):
    a = [f"line_{i}" for i in range(n)]
    b = [f"line_{i}" if i % 3 != 0 else f"changed_{i}" for i in range(n)]
    return a, b
''', '''
a, b = make_lines(N)
ops = diff_lines(a, b)
return checksum([f"{op[0]}_{op[1]}" for op in ops])
''')


# Task 46: Word frequency
add(46, "word_frequency", 200, '''
def word_freq(text):
    """Count word frequencies (case-insensitive)."""
    freq = {}
    word = []
    for c in text:
        if c.isalpha():
            word.append(c.lower())
        else:
            if word:
                w = ''.join(word)
                freq[w] = freq.get(w, 0) + 1
                word = []
    if word:
        w = ''.join(word)
        freq[w] = freq.get(w, 0) + 1
    return freq

def make_text(n):
    words = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog', 'and', 'cat']
    return ' '.join(words[i % len(words)] for i in range(n))
''', '''
text = make_text(N * 5000)
freq = word_freq(text)
return checksum(sorted(freq.items()))
''')


# Task 47: Sentence splitter
add(47, "sentence_splitter", 600, '''
def split_sentences(text):
    """Split text into sentences."""
    sentences = []
    cur = []
    i = 0
    n = len(text)
    while i < n:
        cur.append(text[i])
        if text[i] in '.!?':
            # Skip subsequent whitespace
            j = i + 1
            while j < n and text[j].isspace():
                j += 1
            if j >= n or text[j].isupper():
                sentences.append(''.join(cur).strip())
                cur = []
            i = j
        else:
            i += 1
    if cur:
        s = ''.join(cur).strip()
        if s:
            sentences.append(s)
    return sentences

def make_text(n):
    return '. '.join([f"Sentence number {i} contains some words" for i in range(n)]) + '.'
''', '''
text = make_text(N * 200)
sentences = split_sentences(text)
return checksum([len(s) for s in sentences])
''')


# Task 48: CSV pivot
add(48, "csv_pivot", 100, '''
def pivot(rows, row_key_idx, col_key_idx, value_idx):
    """Pivot rows into a nested dict[row_key][col_key] = sum(value)."""
    result = {}
    for row in rows:
        if len(row) <= max(row_key_idx, col_key_idx, value_idx):
            continue
        rk = row[row_key_idx]
        ck = row[col_key_idx]
        try:
            v = float(row[value_idx])
        except ValueError:
            continue
        if rk not in result:
            result[rk] = {}
        result[rk][ck] = result[rk].get(ck, 0.0) + v
    return result

def make_rows(n):
    return [(f"r{i % 50}", f"c{i % 30}", "x", str(i * 1.7)) for i in range(n)]
''', '''
rows = make_rows(N * 1000)
piv = pivot(rows, 0, 1, 3)
flat = []
for r, cols in sorted(piv.items()):
    for c, v in sorted(cols.items()):
        flat.append((r, c, v))
return checksum(flat)
''')


# Task 49: JSON path resolver
add(49, "json_path_resolver", 5000, '''
def resolve_path(obj, path):
    """Resolve a dotted path like 'a.b[2].c' on obj."""
    cur = obj
    token = []
    i = 0
    n = len(path)
    while i < n and cur is not None:
        c = path[i]
        if c == '.':
            if token:
                cur = cur.get(''.join(token)) if isinstance(cur, dict) else None
                token = []
            i += 1
        elif c == '[':
            if token:
                cur = cur.get(''.join(token)) if isinstance(cur, dict) else None
                token = []
            j = path.find(']', i)
            if j == -1:
                return None
            try:
                idx = int(path[i+1:j])
                cur = cur[idx] if isinstance(cur, list) and 0 <= idx < len(cur) else None
            except (ValueError, TypeError):
                return None
            i = j + 1
        else:
            token.append(c)
            i += 1
    if token and isinstance(cur, dict):
        cur = cur.get(''.join(token))
    return cur

def make_obj():
    return {f"k{i}": {f"sub{j}": [i*10 + j + k for k in range(5)] for j in range(5)} for i in range(20)}
''', '''
obj = make_obj()
paths = [f"k{i % 20}.sub{(i*7) % 5}[{(i*13) % 5}]" for i in range(N)]
results = [resolve_path(obj, p) for p in paths]
results = [r for r in results if r is not None]
return checksum(results)
''')


# Task 50: Template renderer
add(50, "template_renderer", 3000, '''
def render(template, ctx):
    """Render {{var}} placeholders."""
    out = []
    i = 0
    n = len(template)
    while i < n:
        if i + 1 < n and template[i] == '{' and template[i+1] == '{':
            end = template.find('}}', i + 2)
            if end == -1:
                out.append(template[i])
                i += 1
            else:
                var = template[i+2:end].strip()
                val = ctx.get(var, '')
                out.append(str(val))
                i = end + 2
        else:
            out.append(template[i])
            i += 1
    return ''.join(out)

def make_template():
    return "Hello {{name}}, your order {{id}} for {{item}} totals ${{amount}}. Status: {{status}}."

def make_contexts(n):
    return [
        {'name': f'user{i}', 'id': str(i), 'item': f'product{i % 100}',
         'amount': str(i * 1.5), 'status': 'shipped' if i % 2 else 'pending'}
        for i in range(n)
    ]
''', '''
tmpl = make_template()
ctxs = make_contexts(N * 100)
rendered = [render(tmpl, c) for c in ctxs]
return checksum([len(r) for r in rendered])
''')


assert len(PARSING_TASKS) == 25, f"Expected 25, got {len(PARSING_TASKS)}"

if __name__ == "__main__":
    for t in PARSING_TASKS:
        print(f"Task {t.task_id:>3}: {t.name:<25} N={t.n}")
