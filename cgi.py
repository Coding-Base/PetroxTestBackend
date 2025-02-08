# cgi.py - Minimal replacement for the missing standard library module in Python 3.13

def escape(s, quote=True):
    """
    Replace special characters "&", "<", and ">" with HTML-safe sequences.
    """
    if not isinstance(s, str):
        s = str(s)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
    return s

def parse_header(line):
    """
    A minimal header parser that splits a header line into a value and parameters.
    Returns a tuple (value, params) where params is a dictionary.
    """
    parts = [part.strip() for part in line.split(";")]
    key = parts[0]
    params = {}
    for param in parts[1:]:
        if "=" in param:
            k, v = param.split("=", 1)
            params[k.strip()] = v.strip().strip('"')
    return key, params

# For testing: if run directly, print a test escape.
if __name__ == "__main__":
    print(escape("Test"))
