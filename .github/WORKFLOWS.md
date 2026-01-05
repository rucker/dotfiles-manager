# GitHub Actions CI/CD Guide

This document explains the GitHub Actions workflows configured for this repository.

## Overview

This repository uses GitHub Actions for continuous integration and deployment. All workflows are **completely free** for public repositories.

## Workflows

### 1. Tests Workflow (`test.yml`)

**Triggers:** Every push and pull request to `master` or `main` branches

**What it does:**
- Runs the full test suite across multiple Python versions (3.10, 3.11, 3.12, 3.13)
- Generates code coverage reports
- Uploads coverage to Codecov (optional integration)

**Jobs:**
```
test (3.10) - Ubuntu Latest
test (3.11) - Ubuntu Latest
test (3.12) - Ubuntu Latest
test (3.13) - Ubuntu Latest
```

All jobs run in parallel, typically completing in 2-3 minutes total.

**When it passes:**
- ✅ All 33 tests pass across all Python versions
- ✅ No import errors or dependency issues

**When it fails:**
- ❌ Any test fails on any Python version
- ❌ Package installation fails
- ❌ Dependencies can't be resolved

### 2. Code Quality Workflow (`quality.yml`)

**Triggers:** Every push and pull request to `master` or `main` branches

**What it does:**
- Checks code formatting with `black`
- Checks import sorting with `isort`
- Runs static type checking with `mypy`
- Lints code with `ruff`

**Jobs:**
```
quality - Ubuntu Latest (Python 3.13)
```

Typically completes in 1-2 minutes.

**When it passes:**
- ✅ All code is formatted according to black standards
- ✅ All imports are sorted correctly
- ✅ All type hints are valid
- ✅ No linting errors

**When it fails:**
- ❌ Code needs formatting (`black dotfilesmanager/ tests/`)
- ❌ Imports need sorting (`isort dotfilesmanager/ tests/`)
- ❌ Type checking errors detected
- ❌ Linting issues found

## Viewing Workflow Results

### In the GitHub UI

1. Navigate to your repository on GitHub
2. Click the **"Actions"** tab
3. See all workflow runs with their status

**Direct link:** `https://github.com/rucker/dotfiles-manager/actions`

### On Pull Requests

- Workflow status appears at the bottom of every PR
- Click "Details" next to each check to view logs
- PRs show ✅ or ❌ for each workflow

### Status Badges

The README displays live status badges:

[![Tests](https://github.com/rucker/dotfiles-manager/workflows/Tests/badge.svg)](https://github.com/rucker/dotfiles-manager/actions/workflows/test.yml)
[![Code Quality](https://github.com/rucker/dotfiles-manager/workflows/Code%20Quality/badge.svg)](https://github.com/rucker/dotfiles-manager/actions/workflows/quality.yml)

- Click badges to view workflow runs
- Badges update automatically after each run

## Branch Protection (Recommended)

Require workflows to pass before merging PRs:

### Setup Steps

1. Go to **Settings** → **Branches** → **Branch protection rules**
2. Click **"Add rule"**
3. Branch name pattern: `master` (or `main`)
4. Check: ☑️ **"Require status checks to pass before merging"**
5. Search and select these status checks:
   - `test (3.10)`
   - `test (3.11)`
   - `test (3.12)`
   - `test (3.13)`
   - `quality`
6. Check: ☑️ **"Require branches to be up to date before merging"**
7. Click **"Create"** or **"Save changes"**

### What This Does

- ❌ Prevents merging PRs with failing tests
- ❌ Prevents merging PRs with code quality issues
- ✅ Ensures all code in `master` passes all checks
- ✅ Forces contributors to fix issues before merge

## Fixing Failures

### Test Failures

If tests fail on a specific Python version:

1. **View the logs:**
   - Click "Details" on the failed check
   - Expand the "Run tests with coverage" step
   - Review the test failure output

2. **Reproduce locally:**
   ```bash
   # Use pyenv or similar to test specific version
   pyenv install 3.10.0
   pyenv local 3.10.0
   python -m pip install -e .[dev]
   pytest
   ```

3. **Fix and push:**
   ```bash
   # Fix the issue
   git add .
   git commit -m "Fix test failure on Python 3.10"
   git push
   ```
   - Workflows re-run automatically on push

### Code Quality Failures

If quality checks fail:

1. **Format code:**
   ```bash
   black dotfilesmanager/ tests/
   isort dotfilesmanager/ tests/
   ```

2. **Fix type errors:**
   ```bash
   mypy dotfilesmanager/
   # Fix reported errors
   ```

3. **Fix linting issues:**
   ```bash
   ruff check dotfilesmanager/ tests/ --fix
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Fix code quality issues"
   git push
   ```

## Running Checks Locally

Always run checks locally before pushing:

```bash
# Run all tests
pytest

# Check formatting
black --check dotfilesmanager/ tests/
isort --check-only dotfilesmanager/ tests/

# Type check
mypy dotfilesmanager/

# Lint
ruff check dotfilesmanager/ tests/

# Or run everything that CI runs:
pytest --cov=dotfilesmanager --cov-report=term && \
  black --check dotfilesmanager/ tests/ && \
  isort --check-only dotfilesmanager/ tests/ && \
  mypy dotfilesmanager/ && \
  ruff check dotfilesmanager/ tests/
```

## Codecov Integration (Optional)

The test workflow uploads coverage to [Codecov](https://codecov.io), a free service for public repos.

### Setup (One-time)

1. Go to https://codecov.io
2. Sign in with GitHub
3. Enable the repository
4. Add a badge to README (optional):
   ```markdown
   [![codecov](https://codecov.io/gh/rucker/dotfiles-manager/branch/master/graph/badge.svg)](https://codecov.io/gh/rucker/dotfiles-manager)
   ```

No configuration needed - it works automatically via the workflow.

### What You Get

- Visual coverage reports
- Coverage trends over time
- PR comments showing coverage changes
- Coverage badges

## Workflow Costs

### Free Tier (Public Repositories)

- ✅ **Unlimited** minutes
- ✅ **Unlimited** workflow runs
- ✅ **No credit card** required
- ✅ **$0.00** cost

### Private Repositories

If you made this repo private:
- 2,000 free minutes/month
- $0.008 per minute after that
- Ubuntu runners: 1x multiplier

Our workflows use ~5 minutes total per run, so you'd get ~400 runs/month free.

## Troubleshooting

### Workflows Don't Trigger

**Problem:** Pushed code but workflows didn't run

**Solutions:**
- Check the "Actions" tab isn't disabled (Settings → Actions → General)
- Verify branch name matches trigger (`master` or `main`)
- Ensure `.github/workflows/*.yml` files were pushed

### Dependency Installation Fails

**Problem:** `python -m pip install -e .[dev]` fails in workflow

**Solutions:**
- Test locally: `python -m pip install -e .[dev]`
- Check `pyproject.toml` for syntax errors
- Verify all dependencies are available on PyPI
- Check for Python version incompatibilities

### Tests Pass Locally, Fail on CI

**Common causes:**
- **Timezone differences:** CI runs in UTC
- **File permissions:** CI has different permissions
- **Path separators:** Use `pathlib.Path` not hardcoded `/` or `\`
- **Missing files:** Ensure test data is committed
- **Randomness:** Use fixed seeds or deterministic tests

**Debug:**
```bash
# Add this to your test to see environment
import os, sys
print(f"Python: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"CWD: {os.getcwd()}")
```

### Workflow Takes Too Long

**Problem:** Tests take more than 5 minutes

**Solutions:**
- Use `pytest -n auto` for parallel testing (requires `pytest-xdist`)
- Cache pip dependencies:
  ```yaml
  - name: Cache pip dependencies
    uses: actions/cache@v3
    with:
      path: ~/.cache/pip
      key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
  ```

## Advanced Configuration

### Running on Schedule

Add a cron trigger to run tests nightly:

```yaml
on:
  push:
    branches: [master, main]
  pull_request:
    branches: [master, main]
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily
```

### Testing on Multiple OS

Add Windows and macOS:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.10", "3.11", "3.12", "3.13"]
runs-on: ${{ matrix.os }}
```

Note: This increases run time 3x (Linux, Windows, macOS).

### Manual Workflow Trigger

Allow manual workflow runs:

```yaml
on:
  push:
    branches: [master, main]
  pull_request:
    branches: [master, main]
  workflow_dispatch:  # Enables "Run workflow" button
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Codecov Documentation](https://docs.codecov.com/)

## Support

If you encounter issues:

1. Check the [Actions tab](https://github.com/rucker/dotfiles-manager/actions) for error details
2. Review workflow logs for the specific failing step
3. Try reproducing locally with the same Python version
4. Open an issue if you suspect a workflow configuration problem
