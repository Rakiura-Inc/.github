# Rakiura-Inc/.github

Shared engineering setup for every Rakiura-Inc repository:

- **Reusable GitHub Actions workflows** (`.github/workflows/`), called by each repository's own
  small workflow files, so a fix to CI lands everywhere through one Renovate pull request.
- **The Renovate preset** (`renovate-config.json5`) every repository extends.
- **Default community files**: `SECURITY.md` applies to every repository that has none of its own.

New repositories are generated from [Rakiura-Inc/python-template](https://github.com/Rakiura-Inc/python-template),
which already calls these workflows and extends the preset.

## Why this repository, and not a `workflows` repository

A reusable workflow can live in any repository, so this was a choice. `.github` is GitHub's
conventional home for an organization's shared setup: it is the only repository whose
`SECURITY.md`, `CONTRIBUTING.md` and issue templates GitHub applies to the other repositories,
and where organization workflow templates live. Keeping the workflows and the Renovate preset
here too puts all organization-wide defaults in one public repository with one history and one
set of reviewers, and gives callers an unsurprising path
(`Rakiura-Inc/.github/.github/workflows/<name>.yml`). It must stay public, because public
repositories can only call workflows from public repositories.

## The workflows

| Workflow | What it does | Permissions the calling job grants |
|---|---|---|
| `python-tests.yml` | `uv sync`, optional `ty check`, `pytest` on a matrix of Python versions; optionally builds the wheel, imports it on its own and re-runs the tests against it | `contents: read` |
| `git-hooks.yml` | every hook in `.pre-commit-config.yaml` on every file, with prek | `contents: read` |
| `notebooks-execute.yml` | executes every teaching notebook headless on Colab's Python (3.13 today); uploads the executed copies | `contents: read` |
| `pip-audit.yml` | checks every locked dependency for known vulnerabilities | `contents: read` |
| `release.yml` | on a `v*` tag: builds the sdist and wheel (read-only job), then records build provenance and attaches them to a GitHub Release | `contents: write`, `id-token: write`, `attestations: write` |
| `scorecard.yml` | OpenSSF Scorecard on the default branch, uploaded as SARIF to the Security tab | `contents: read`, `security-events: write` |

Each file starts with a short calling example, and every input has a description and a default.
All of them run on `ubuntu-26.04` with a timeout, check out with `persist-credentials: false`,
start from `permissions: {}` and pin every action to a full commit SHA.

### Calling a workflow

```yaml
jobs:
  tests:
    name: Tests
    permissions:
      contents: read  # check out the repository
    uses: Rakiura-Inc/.github/.github/workflows/python-tests.yml@<full commit SHA>  # v1.0.0
    with:
      import-check: "import mypackage; print(mypackage.__version__)"
```

Always pin to the commit SHA of a release tag, with the tag in a comment. Renovate then proposes
each new release as one pull request ("Rakiura shared workflows").

### Releasing a change to the workflows

1. Open a pull request. The **Self test** workflow runs the changed workflows, from that commit,
   against the small project in `tests/fixture/`, and the git hooks run zizmor on every file.
2. Merge it, then tag the merge commit: `git tag v1.1.0 && git push origin v1.1.0`. Use a new
   major version for a change that breaks callers (a removed or renamed input).

### Scorecard results

The shared Scorecard workflow uploads its results to each repository's Security tab but does not
publish them to api.scorecard.dev, so there is no public Scorecard badge. The Scorecard API only
accepts results from a workflow that runs `ossf/scorecard-action` itself; a repository that wants
the badge can copy `scorecard.yml` in as its own workflow and set `publish_results: true` (and
`id-token: write`).

## The Renovate preset

A repository's `renovate.json5`:

```json5
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["github>Rakiura-Inc/.github:renovate-config.json5"],
}
```

It pins actions to digests and dev tools to exact versions, updates pre-commit hooks, refreshes
`uv.lock` weekly, follows `# renovate: datasource=... depName=...` comments in workflows, and
waits three days before proposing a third-party release.

## Development

You need [uv](https://docs.astral.sh/uv/) and [prek](https://prek.j178.dev/) (or pre-commit).

```sh
prek install            # run the hooks (zizmor, workflow schema checks, yamlfmt...) on every commit
prek run --all-files    # run them now
```

## Licence

MIT, copyright 2026 Rakiura Inc. See [LICENSE](LICENSE).
