#!/usr/bin/env bash
# Claude Code Stop hook: run the CI gate (`mkdocs build --strict`) once Claude
# is done, if the site sources changed. Exit 2 keeps Claude working and sends
# the build errors back to it.
set -uo pipefail

cd "$(dirname "$0")/../.." || exit 0

# already continuing because of this hook: do not loop
[[ $(jq -r '.stop_hook_active // false') == "true" ]] && exit 0

# nothing to build if no site source changed (tracked or new files)
[[ -n $(git status --porcelain -- src mkdocs.yml overrides hooks requirements.txt) ]] || exit 0

out=$(mktemp -d)
trap 'rm -rf "${out}"' EXIT
# no -q: it hides the warnings that --strict turns into a failure
if ! log=$(mkdocs build --strict -f mkdocs.yml -d "${out}/site" 2>&1); then
    # drop Material's boxed banner and colour codes, keep the errors
    printf 'mkdocs build --strict failed:\n%s\n' \
        "$(sed -E 's/\x1b\[[0-9;]*m//g' <<<"${log}" | grep -v '│' | grep -v '^\s*$')" >&2
    exit 2
fi
exit 0
