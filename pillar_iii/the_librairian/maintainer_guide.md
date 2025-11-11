---
title: Maintainer Guide
nav_order: 4
parent: The LibrAIrian Your AI Guide
grand_parent: Pillar III MLOps & DevOps
---

# LibrAIrian Fork Management - Maintainer Guide

This guide is for repository maintainers who manage the LibrAIrian fork management system. It covers configuration, monitoring, troubleshooting, and best practices.

## Table of Contents

1. [Initial Setup](#initial-setup)
2. [System Configuration](#system-configuration)
3. [Monitoring and Analytics](#monitoring-and-analytics)
4. [Customization](#customization)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

## Initial Setup

### 1. Enable GitHub Actions

Ensure GitHub Actions are enabled for the repository:

1. Go to **Settings** → **Actions** → **General**
2. Under "Actions permissions", select **Allow all actions and reusable workflows**
3. Under "Workflow permissions", ensure:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests

### 2. Create Labels

Run the label setup workflow:

```bash
# Manually trigger the workflow
gh workflow run setup-labels.yml
```

Or push changes to trigger automatically:

```bash
git add .github/librairian-config.yml
git commit -m "Update LibrAIrian configuration"
git push
```

### 3. Verify Workflows

Check that all workflows are present:

```bash
ls -la .github/workflows/
```

Expected workflows:
- `librairian-fork-manager.yml` - Main fork management workflow
- `fork-sync-helper.yml` - Fork synchronization assistance
- `librairian-pr-review.yml` - Automated PR review
- `setup-labels.yml` - Label configuration

### 4. Test the System

1. Create a test fork
2. Open a test PR from the fork
3. Verify that LibrAIrian responds with:
   - Welcome message
   - Auto-labeling
   - Quality check report

## System Configuration

### Main Configuration File

Location: `.github/librairian-config.yml`

#### Enable/Disable Features

```yaml
fork_management:
  auto_welcome: true      # Welcome new contributors
  auto_label: true        # Automatically label PRs
  auto_guidance: true     # Provide automated guidance
  
  sync_reminders:
    enabled: true         # Send sync reminders
    threshold_commits: 5  # Remind when fork is behind by N commits
    frequency_days: 7     # Check frequency
```

#### Quality Checks

```yaml
quality_checks:
  markdown_lint: true       # Validate markdown files
  yaml_lint: true          # Validate YAML files
  structure_check: true    # Check file organization
  documentation_check: true # Check for missing docs
```

#### Rate Limiting

Prevent spam by configuring limits:

```yaml
rate_limits:
  max_comments_per_pr: 5           # Max comments per PR
  max_labels_per_pr: 6             # Max labels per PR
  min_time_between_comments: 300   # Min seconds between comments
```

### Label Configuration

Define custom labels in the config file:

```yaml
labels:
  pillars:
    - name: "pillar-i-core-concepts"
      color: "0E8A16"
      description: "Related to Pillar I: Core Concepts"
  
  types:
    - name: "code-example"
      color: "BFD4F2"
      description: "Code example contribution"
```

After updating labels, run:

```bash
gh workflow run setup-labels.yml
```

### Workflow Triggers

#### Pull Request Workflow

Triggers on PR events from forks:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, edited]
    branches:
      - main
      - develop
```

#### Schedule Workflow

Runs periodically for maintenance:

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sundays at midnight
```

Adjust frequency by modifying the cron expression:
- Daily: `'0 0 * * *'`
- Twice weekly: `'0 0 * * 0,3'`
- Monthly: `'0 0 1 * *'`

## Monitoring and Analytics

### Viewing Workflow Runs

1. Go to repository **Actions** tab
2. Select a workflow from the left sidebar
3. View recent runs with status indicators

### Analyzing Workflow Logs

For detailed execution logs:

1. Click on a workflow run
2. Select a job to view logs
3. Expand steps to see detailed output

### Key Metrics to Monitor

Track these metrics for system health:

- **Response Rate**: Percentage of PRs receiving LibrAIrian welcome
- **Label Accuracy**: Correctness of auto-applied labels
- **Quality Check Pass Rate**: Percentage passing quality checks
- **Sync Reminder Effectiveness**: Forks that sync after reminder

### Creating a Monitoring Dashboard

Use GitHub API to collect metrics:

```bash
# Count fork PRs in the last 30 days
gh api repos/OWNER/REPO/pulls \
  --method GET \
  -f state=all \
  -f sort=created \
  -f direction=desc \
  | jq '[.[] | select(.head.repo.fork == true)] | length'
```

## Customization

### Customizing Welcome Messages

Edit `librairian-fork-manager.yml`:

```javascript
const welcomeMessage = `## 👋 Welcome to the Databricks Reference Library, @${author}!

// Customize your welcome message here
`;
```

### Adding New Quality Checks

Add new checks to `librairian-pr-review.yml`:

```yaml
- name: Custom Quality Check
  run: |
    # Add your custom check script here
    echo "Running custom quality check..."
```

### Creating Custom Workflows

Template for a new LibrAIrian workflow:

```yaml
name: Custom LibrAIrian Workflow

on:
  pull_request:
    types: [opened]

permissions:
  pull-requests: write

jobs:
  custom-job:
    runs-on: ubuntu-latest
    if: github.event.pull_request.head.repo.fork == true
    steps:
      - name: Custom Action
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            // Your custom logic here
```

### Modifying Auto-Label Logic

Edit the analysis logic in `librairian-fork-manager.yml`:

```javascript
// Determine affected pillars
if ('${{ steps.changed-files.outputs.pillar_i_any_changed }}' === 'true') {
  labels.push('pillar-i-core-concepts');
}

// Add custom labeling logic
if (prTitle.includes('urgent')) {
  labels.push('priority-high');
}
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: LibrAIrian Not Responding

**Symptoms**: No automated comments on fork PRs

**Diagnosis**:
```bash
# Check if workflows are enabled
gh api repos/OWNER/REPO/actions/permissions

# List recent workflow runs
gh run list --workflow=librairian-fork-manager.yml
```

**Solutions**:
1. Verify GitHub Actions are enabled
2. Check workflow permissions
3. Review recent workflow run logs
4. Ensure PR is from a fork: `head.repo.fork == true`

#### Issue: Duplicate Comments

**Symptoms**: Multiple identical comments from LibrAIrian

**Solutions**:
1. Check rate limit configuration:
   ```yaml
   rate_limits:
     max_comments_per_pr: 5
     min_time_between_comments: 300
   ```
2. Review workflow triggers to avoid redundant execution
3. Add comment deduplication logic

#### Issue: Labels Not Applied

**Symptoms**: PRs not receiving auto-labels

**Diagnosis**:
```bash
# Check label setup
gh label list

# View workflow logs
gh run view --log
```

**Solutions**:
1. Run label setup workflow: `gh workflow run setup-labels.yml`
2. Verify label names match configuration
3. Check workflow has `issues: write` permission

#### Issue: Sync Reminders Not Sent

**Symptoms**: No sync notifications despite forks being behind

**Solutions**:
1. Verify scheduled workflow is enabled
2. Check `sync_reminders.enabled: true` in config
3. Adjust `threshold_commits` if too high
4. Review cron schedule syntax

### Debugging Workflows

#### Enable Debug Logging

Set repository secrets:
- `ACTIONS_STEP_DEBUG`: `true`
- `ACTIONS_RUNNER_DEBUG`: `true`

#### View Detailed Logs

```bash
# View logs for a specific run
gh run view RUN_ID --log

# Download logs locally
gh run download RUN_ID
```

#### Test Workflows Locally

Use [act](https://github.com/nektos/act) to test workflows:

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act pull_request -W .github/workflows/librairian-fork-manager.yml
```

## Best Practices

### For System Maintenance

1. **Regular Review**: Check workflow executions weekly
2. **Monitor Feedback**: Track contributor responses to LibrAIrian
3. **Update Templates**: Refresh messages based on feedback
4. **Test Changes**: Test configuration changes in a fork first
5. **Document Customizations**: Keep this guide updated

### For Configuration Management

1. **Version Control**: Track all config changes in git
2. **Comments**: Document why settings were chosen
3. **Gradual Rollout**: Test new features with small changes
4. **Backup**: Keep backup of working configurations
5. **Review**: Regularly review and optimize settings

### For Community Management

1. **Respond Quickly**: Address LibrAIrian issues promptly
2. **Gather Feedback**: Ask contributors about their experience
3. **Iterate**: Continuously improve based on feedback
4. **Communicate**: Announce system changes to community
5. **Support**: Help contributors understand automation

### Security Best Practices

1. **Minimal Permissions**: Grant only necessary permissions
2. **Audit Regularly**: Review workflow permissions quarterly
3. **Monitor Activity**: Watch for unusual automation behavior
4. **Protect Secrets**: Never expose tokens or credentials
5. **Fork Safety**: Ensure workflows never write to forks

### Performance Optimization

1. **Caching**: Use action caching for dependencies
2. **Concurrency**: Limit concurrent workflow runs
3. **Selective Triggers**: Only trigger when necessary
4. **Efficient Checks**: Optimize quality check scripts
5. **Rate Limits**: Respect GitHub API rate limits

## Advanced Topics

### Integrating with External Services

Example: Send Slack notifications for new fork PRs

```yaml
- name: Notify on Slack
  uses: slackapi/slack-github-action@v1
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "New fork PR from ${{ github.event.pull_request.user.login }}"
      }
```

### Custom Analytics

Create a workflow to collect contribution metrics:

```yaml
name: Collect LibrAIrian Metrics

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  collect-metrics:
    runs-on: ubuntu-latest
    steps:
      - name: Gather data
        uses: actions/github-script@v7
        script: |
          // Query PRs, issues, and workflow runs
          // Store metrics in repository or external service
```

### Multi-Repository Setup

To use LibrAIrian across multiple repositories:

1. Create a reusable workflow:
   ```yaml
   # .github/workflows/librairian-reusable.yml
   on:
     workflow_call:
       inputs:
         welcome_message:
           required: true
           type: string
   ```

2. Call from other repositories:
   ```yaml
   jobs:
     call-librairian:
       uses: ginjaninja78/databricks-reference/.github/workflows/librairian-reusable.yml@main
   ```

## Getting Help

### Internal Resources

- [Fork Management Documentation](fork_management.md)
- [Contributing Guidelines](../../../CONTRIBUTING.md)
- GitHub Actions logs and insights

### External Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub Community Forum](https://github.community/)

### Support Channels

1. Open an issue with `librairian-system` label
2. Discussion in GitHub Discussions
3. Contact repository administrators

---

**Remember**: The LibrAIrian system is designed to help, not hinder. Keep it simple, responsive, and contributor-friendly. Happy maintaining! 🚀
