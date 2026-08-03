# Security policy

## What is in this repository

Markdown catalogues, and one Python script (`tools/validate.py`) that reads them
and reports structural problems. There is no service, no database, no user
accounts, no runtime dependencies, and nothing here processes input from anyone
except the person who runs the script.

So the honest attack surface is small, and worth stating rather than dressing up:

| Thing | Exposure |
|---|---|
| `catalogs/*.md`, `RULES.md`, `ROSTER.md`, `CONSISTENCY.md` | Text. Rendered by GitHub, which sanitises it. |
| `tools/validate.py` | Reads files under this repo and prints findings. No network, no subprocesses, no writes. |
| `.github/workflows/validate.yml` | Runs that script on push and pull request with a read-only token and no secrets. |

There are no credentials, keys or tokens in the working tree or anywhere in the
history, and none are needed to use anything here.

## Reporting a vulnerability

Use **[private vulnerability reporting](https://github.com/Jonaaaa/Unique_Console_Games/security/advisories/new)**,
which is enabled on this repository. That keeps the report between us until
there is a fix. Please do not open a public issue for a security problem.

Useful things to include: what you did, what happened, and what you expected.
A proof of concept helps but is not required.

This is a personal project, not a product with an on-call rotation. Expect a
reply within a week or so, and a fix or an explanation of why something is not
a problem shortly after.

### In scope

- Anything in `tools/validate.py` that a crafted catalogue file could exploit,
  such as path traversal out of the repository, or resource exhaustion.
- Anything in the workflow that would let a pull request from a fork obtain
  write access, exfiltrate a token, or run with more permission than intended.
- Credentials or personal data found anywhere in the repository or its history.

### Not security issues

- **A wrong release year, publisher, or status.** Those are data corrections.
  Please [open an issue](https://github.com/Jonaaaa/Unique_Console_Games/issues);
  they are welcome and they are the main reason this repository is public.
- **A broken or redirected link to a third-party site.** Also an issue, not a
  vulnerability.
- **Anything about the games themselves.** Nothing is hosted or distributed
  here. There are no ROMs, no binaries, no downloads, and no links to any.

## What is done to keep it clean

- Every push and pull request runs `tools/validate.py`, with `contents: read`
  and no secrets available to the job.
- `actions/checkout` is pinned to a commit rather than a tag, because a tag can
  be moved to point at different code and a commit cannot.
- Secret scanning and push protection are enabled, so a credential committed by
  accident is caught on the way in rather than after the fact.
