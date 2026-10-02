import sys

# paper titles are often non-ASCII; don't let a log line crash the pipeline
# when stdout isn't UTF-8 (e.g. redirected output on Windows)
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(errors="backslashreplace")
