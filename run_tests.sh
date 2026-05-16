#!/usr/bin/env bash
# Convenience wrapper: macOS homebrew Python ships linked against a newer
# libexpat than /usr/lib/libexpat.1.dylib on some systems, so we point
# DYLD_LIBRARY_PATH at the brewed expat before running pytest.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
expat_lib="$(brew --prefix expat 2>/dev/null)/lib"
if [ -d "$expat_lib" ]; then
    export DYLD_LIBRARY_PATH="$expat_lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
fi
exec "$here/.venv/bin/pytest" "$@"
