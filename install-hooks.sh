#!/usr/bin/env bash
# Install the local git hooks. Hooks live in .git/hooks/, which git does not
# track, so this must be re-run on a fresh clone.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
mkdir -p .git/hooks

cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
# Run the structural validator, because a malformed table renders fine on GitHub
# and is wrong in the data: a row with a missing cell shows with a column gone,
# a heading glued to a row disappears from the outline.
#
# When tools/validate.py is itself being committed, also prove the checks still
# fire. A check that reports nothing looks exactly like a check that cannot
# fire, and three drafts of R18 shipped in that state.
#
# Skip once with:  git commit --no-verify
cd "$(git rev-parse --show-toplevel)" || exit 0

./tools/validate.py --quiet || {
  echo "pre-commit: fix the problems above, or skip with git commit --no-verify." >&2
  exit 1
}

if git diff --cached --name-only | grep -qx "tools/validate.py"; then
  # selftest writes to the tree and restores it. Unstaged edits are the hazard:
  # a crash mid-case would be indistinguishable from your own work. Staged ones
  # are safe, and are the ordinary case when a check and its data change together.
  if ! git diff --quiet -- catalogs README.md; then
    echo "pre-commit: validate.py is staged but there are unstaged data changes;" >&2
    echo "            run ./tools/selftest.py yourself once it is clean." >&2
  else
    ./tools/selftest.py >/dev/null || {
      echo "pre-commit: a check no longer fires; run ./tools/selftest.py." >&2
      exit 1
    }
  fi
fi
HOOK

chmod +x .git/hooks/pre-commit
echo "Installed .git/hooks/pre-commit"
