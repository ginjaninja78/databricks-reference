# LibrAIrian Fork Management System - Testing Guide

This document provides instructions for testing the LibrAIrian fork management system to ensure all workflows are functioning correctly.

## Pre-Testing Checklist

Before running tests, ensure:

- [ ] All workflows are present in `.github/workflows/`
- [ ] Configuration file `.github/librairian-config.yml` exists
- [ ] GitHub Actions are enabled in repository settings
- [ ] Required labels are created (run `setup-labels.yml`)
- [ ] Workflow permissions are correctly configured

## Testing Methodology

### 1. YAML Validation

Validate all workflow files for syntax errors:

```bash
# Install yamllint
pip install yamllint

# Validate all YAML files
yamllint -d relaxed .github/workflows/*.yml .github/librairian-config.yml
```

Expected: No errors (warnings about line length are acceptable)

### 2. Python YAML Parser Test

```bash
cd /home/runner/work/databricks-reference/databricks-reference
python3 << 'EOF'
import yaml
import glob

for file in glob.glob('.github/workflows/*.yml') + glob.glob('.github/*.yml'):
    with open(file, 'r') as f:
        yaml.safe_load(f)
    print(f"✅ {file}: Valid")
EOF
```

Expected: All files marked as valid

### 3. Fork Detection Test

**Test Case**: Verify fork detection logic

**Setup**:
1. Create a test fork of the repository
2. Create a test branch in the fork
3. Make a small change (e.g., update README)
4. Open a PR from fork to main repository

**Expected Behavior**:
- [ ] PR is detected as coming from a fork
- [ ] `detect-fork` job runs successfully
- [ ] `is-fork` output is `true`
- [ ] User and repo outputs are correct

**Validation**:
```bash
# Check workflow run logs
gh run list --workflow=librairian-fork-manager.yml --limit 5
gh run view <run-id> --log
```

### 4. Welcome Message Test

**Test Case**: Verify welcome message is posted

**Setup**: Open a PR from a fork (same as Fork Detection Test)

**Expected Behavior**:
- [ ] Welcome message posted within 2 minutes
- [ ] Message contains contributor's username
- [ ] Message includes checklist
- [ ] Message includes resource links
- [ ] Message is posted only once

**Manual Verification**:
1. Check PR comments for welcome message
2. Verify message formatting
3. Confirm links are correct and working

### 5. Auto-Labeling Test

**Test Case**: Verify automatic label application

**Setup**: Open PRs with changes in different pillars

**Test Cases**:

#### 5a. Pillar I Changes
- Create PR modifying `pillar_i/` files
- Expected labels: `pillar-i-core-concepts`, `documentation`, `fork-contribution`

#### 5b. Pillar II Changes
- Create PR modifying `pillar_ii/` files
- Expected labels: `pillar-ii-developer-toolkit`, `documentation`, `fork-contribution`

#### 5c. Code Example Changes
- Create PR adding files to `sample_code/`
- Expected labels: `code-example`, `fork-contribution`, plus relevant pillar

#### 5d. Notebook Changes
- Create PR adding `.ipynb` files to `sample_notebooks/`
- Expected labels: `notebook`, `fork-contribution`, plus relevant pillar

**Validation**:
```bash
# Check labels on PR
gh pr view <pr-number> --json labels
```

### 6. Quality Check Test

**Test Case**: Verify quality checks run correctly

**Setup**: Open PR with various file types

**Expected Behavior**:
- [ ] Markdown files are checked
- [ ] YAML files are validated
- [ ] File structure is analyzed
- [ ] Quality report is posted

**Test Files**:
```bash
# Create test files with various issues
echo "# Test markdown" > test.md
echo "key: value" > test.yml
echo "print('test')" > sample_code/python/test.py
```

**Validation**:
1. Check for quality check comment on PR
2. Verify report includes all file types
3. Confirm recommendations are relevant

### 7. Guidance System Test

**Test Case**: Verify contextual guidance is provided

**Setup**: Create PR with common issues

**Test Scenarios**:

#### 7a. File Naming Issue
- Add file with spaces: `my file.py`
- Expected: Warning about spaces in filename

#### 7b. File Location Issue
- Add notebook to root directory
- Expected: Suggestion to move to `sample_notebooks/`

#### 7c. Documentation Missing
- Add code without documentation
- Expected: Suggestion to add documentation

**Validation**: Check for guidance comment with appropriate suggestions

### 8. Issue Triage Test

**Test Case**: Verify issue auto-triage

**Setup**: Create issues with different keywords

**Test Cases**:

#### 8a. Bug Report
- Title: "Bug: Error in code example"
- Expected labels: `bug`

#### 8b. Feature Request
- Title: "Add new PySpark example"
- Expected labels: `enhancement`

#### 8c. Question
- Title: "How to use Delta Lake?"
- Expected labels: `question`

#### 8d. Pillar Reference
- Body contains: "pillar_ii"
- Expected labels: `pillar-ii-developer-toolkit`

**Validation**:
```bash
# Check issue labels
gh issue view <issue-number> --json labels
```

### 9. Fork Sync Reminder Test

**Test Case**: Verify sync reminders work

**Setup**:
1. Create fork
2. Open PR from fork
3. Let upstream get ahead by 5+ commits
4. Wait for scheduled run or trigger manually

**Expected Behavior**:
- [ ] Sync reminder comment appears on PR
- [ ] Comment includes commit count
- [ ] Comment provides sync instructions
- [ ] Instructions cover multiple methods

**Manual Trigger**:
```bash
# Trigger sync check manually
gh workflow run fork-sync-helper.yml
```

### 10. Permission Safety Test

**Test Case**: Verify workflows don't modify fork repositories

**Setup**: Monitor workflow permissions and actions

**Validation**:
```yaml
# Check workflow permissions
permissions:
  contents: read          # Should be read-only for repo
  pull-requests: write    # Write for comments only
  issues: write          # Write for comments only
```

**Expected Behavior**:
- [ ] No `git push` to fork repositories
- [ ] No branch creation in forks
- [ ] No file modifications in forks
- [ ] All actions scoped to PR comments

**Verification**:
1. Review workflow logs for git operations
2. Check fork repository for unexpected changes
3. Verify all automation is comment-based

### 11. Rate Limiting Test

**Test Case**: Verify rate limits are enforced

**Setup**: Configure strict rate limits

```yaml
rate_limits:
  max_comments_per_pr: 2
  min_time_between_comments: 60
```

**Expected Behavior**:
- [ ] Maximum 2 comments posted
- [ ] No comments within 60 seconds of each other
- [ ] Workflow respects limits

**Validation**: Monitor PR comment timestamps

### 12. Label Setup Test

**Test Case**: Verify label creation/update workflow

**Setup**: Run label setup workflow

```bash
# Manual trigger
gh workflow run setup-labels.yml

# Or push config change
git add .github/librairian-config.yml
git commit -m "Update label config"
git push
```

**Expected Behavior**:
- [ ] All labels from config are created
- [ ] Existing labels are updated
- [ ] Colors and descriptions match config
- [ ] No errors in workflow logs

**Validation**:
```bash
# List all labels
gh label list

# Check specific label
gh label list | grep pillar-i-core-concepts
```

### 13. End-to-End Test

**Test Case**: Complete contribution workflow

**Scenario**: New contributor opens first PR

**Steps**:
1. Fork repository
2. Create feature branch
3. Add code example to `sample_code/python/`
4. Add documentation to `pillar_ii/`
5. Create PR

**Expected Workflow**:
1. [ ] Welcome message posted (< 1 min)
2. [ ] Labels applied (< 2 min)
3. [ ] Quality checks run (< 3 min)
4. [ ] Guidance provided (< 5 min)
5. [ ] All comments are helpful and accurate

**Validation**: Review entire PR timeline and comments

### 14. Multi-Pillar Test

**Test Case**: PR affecting multiple pillars

**Setup**: Create PR with changes across pillars

```bash
# Modify files in multiple pillars
touch pillar_i/test1.md
touch pillar_ii/test2.md
touch pillar_iii/test3.md
```

**Expected Behavior**:
- [ ] Multiple pillar labels applied
- [ ] Analysis mentions all affected areas
- [ ] Guidance is comprehensive

### 15. Configuration Change Test

**Test Case**: Verify config changes take effect

**Setup**: Modify `.github/librairian-config.yml`

```yaml
fork_management:
  auto_welcome: false  # Disable welcome
```

**Expected Behavior**:
- [ ] New PRs don't receive welcome messages
- [ ] Other features still work
- [ ] No errors in workflow

**Validation**: Open test PR and verify no welcome

### 16. Scheduled Workflow Test

**Test Case**: Verify scheduled workflows run

**Setup**: Check cron schedule

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
```

**Validation**:
```bash
# Check recent scheduled runs
gh run list --workflow=fork-sync-helper.yml --event=schedule
```

**Expected**: Weekly executions visible in history

## Integration Testing

### Test Suite Runner Script

Create a test runner script:

```bash
#!/bin/bash
# test-librairian.sh

echo "🧪 LibrAIrian Testing Suite"
echo "=========================="

# 1. YAML Validation
echo "✓ Running YAML validation..."
yamllint -d relaxed .github/workflows/*.yml .github/librairian-config.yml
if [ $? -eq 0 ]; then
    echo "  ✅ YAML validation passed"
else
    echo "  ❌ YAML validation failed"
    exit 1
fi

# 2. Check workflows exist
echo "✓ Checking workflow files..."
WORKFLOWS=(
    "librairian-fork-manager.yml"
    "fork-sync-helper.yml"
    "librairian-pr-review.yml"
    "setup-labels.yml"
)
for workflow in "${WORKFLOWS[@]}"; do
    if [ -f ".github/workflows/$workflow" ]; then
        echo "  ✅ $workflow exists"
    else
        echo "  ❌ $workflow missing"
        exit 1
    fi
done

# 3. Check documentation exists
echo "✓ Checking documentation..."
DOCS=(
    "pillar_iii/the_librairian/fork_management.md"
    "pillar_iii/the_librairian/maintainer_guide.md"
    "pillar_iii/the_librairian/contributor_quickstart.md"
)
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✅ $doc exists"
    else
        echo "  ❌ $doc missing"
        exit 1
    fi
done

# 4. Check config file
echo "✓ Checking configuration..."
if [ -f ".github/librairian-config.yml" ]; then
    echo "  ✅ Configuration file exists"
else
    echo "  ❌ Configuration file missing"
    exit 1
fi

echo ""
echo "🎉 All checks passed!"
echo ""
echo "Next steps:"
echo "1. Create a test fork"
echo "2. Open a test PR"
echo "3. Verify automated responses"
echo "4. Check GitHub Actions logs"
```

Make executable and run:

```bash
chmod +x test-librairian.sh
./test-librairian.sh
```

## Monitoring and Observability

### Metrics to Track

1. **Response Time**: Time from PR open to first LibrAIrian comment
2. **Success Rate**: Percentage of PRs receiving expected automation
3. **Label Accuracy**: Correctness of auto-applied labels
4. **User Satisfaction**: Contributor feedback on automation

### Monitoring Commands

```bash
# View recent workflow runs
gh run list --workflow=librairian-fork-manager.yml --limit 10

# View specific run details
gh run view <run-id>

# View run logs
gh run view <run-id> --log

# List recent PRs from forks
gh pr list --label fork-contribution --limit 10

# Check label usage
gh label list
```

## Troubleshooting Test Failures

### Workflow Not Triggering

**Symptoms**: No automation on fork PRs

**Debug Steps**:
1. Check Actions are enabled: Settings → Actions
2. Verify workflow permissions
3. Check branch protection rules
4. Review workflow trigger conditions
5. Check for syntax errors in workflow files

### Labels Not Applied

**Symptoms**: PRs lack expected labels

**Debug Steps**:
1. Run label setup: `gh workflow run setup-labels.yml`
2. Check label names match config
3. Verify `issues: write` permission
4. Review changed files detection logic

### Comments Not Posted

**Symptoms**: No LibrAIrian comments

**Debug Steps**:
1. Check `pull-requests: write` permission
2. Review rate limit configuration
3. Check for API errors in logs
4. Verify fork detection logic

### Quality Checks Failing

**Symptoms**: Quality check job fails

**Debug Steps**:
1. Check tool installation (yamllint, etc.)
2. Verify file paths are correct
3. Review error messages in logs
4. Test checks locally first

## Continuous Testing

### Pre-Merge Checklist

Before merging changes to the LibrAIrian system:

- [ ] YAML validation passes
- [ ] Test PR opened and verified
- [ ] All workflows triggered successfully
- [ ] Labels applied correctly
- [ ] Comments posted appropriately
- [ ] No permission issues
- [ ] Documentation updated
- [ ] Config file validated

### Post-Deployment Verification

After deploying to production:

- [ ] Monitor first 5 fork PRs
- [ ] Check for any errors in logs
- [ ] Verify contributor feedback is positive
- [ ] Confirm no permission violations
- [ ] Review metrics for anomalies

## Test Report Template

Use this template to document test results:

```markdown
# LibrAIrian Test Report

**Date**: YYYY-MM-DD
**Tester**: Name
**Version**: X.Y.Z

## Test Summary

- Total Tests: X
- Passed: Y
- Failed: Z
- Skipped: A

## Test Results

### Fork Detection
- Status: ✅ Pass / ❌ Fail
- Notes: ...

### Welcome Message
- Status: ✅ Pass / ❌ Fail
- Notes: ...

### Auto-Labeling
- Status: ✅ Pass / ❌ Fail
- Notes: ...

[... continue for all tests ...]

## Issues Found

1. Issue description
   - Severity: High/Medium/Low
   - Steps to reproduce
   - Expected vs actual behavior

## Recommendations

- List any improvements needed
- Suggested fixes
- Future enhancements

## Sign-off

Tested by: [Name]
Approved by: [Name]
Date: YYYY-MM-DD
```

## Automated Testing (Future Enhancement)

Consider implementing automated tests using:

- **GitHub Actions Test Runner**: Run workflows against test data
- **Mock PRs**: Automated PR creation for testing
- **API Testing**: Validate GitHub API interactions
- **End-to-End Tests**: Full workflow simulation

Example test workflow:

```yaml
name: Test LibrAIrian System

on:
  push:
    paths:
      - '.github/workflows/librairian-*.yml'
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate YAML
        run: yamllint .github/workflows/*.yml
      - name: Run unit tests
        run: ./test-librairian.sh
```

---

**Remember**: Thorough testing ensures the LibrAIrian provides a smooth, helpful experience for all contributors. Test early, test often, and always verify changes before deploying to production!
