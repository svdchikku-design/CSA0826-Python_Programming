"""Runs lines through a real interactive interpreter and prints a >>> transcript."""
import code, io, contextlib, sys
def run_session(lines):
    console = code.InteractiveConsole()
    more = False
    for line in lines:
        print(("... " if more else ">>> ") + line)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            more = console.push(line)
        out = buf.getvalue()
        if out:
            print(out, end="")
