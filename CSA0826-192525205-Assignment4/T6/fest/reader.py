"""Reading: yields (line number, text) from one department file, one line at a time."""

def read_lines(path):
    # errors="replace": an undecodable byte becomes U+FFFD instead of aborting the whole file
    with open(path, encoding="utf-8", errors="replace") as f:
        for number, line in enumerate(f, start=1):
            line = line.strip()
            if line:                       # skip blank lines
                yield number, line
