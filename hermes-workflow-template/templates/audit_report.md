# Audit Report Template

## Audit Task
[Clear statement of what was audited - should match the development task]

## Audit Scope
- **Files/Directories Audited**: [list]
- **Audit Date**: [timestamp]
- **Auditor**: Hermes Agent Autonomous Workflow
- **Tools Used**: [list of linters, static analyzers, etc.]

## Summary
- **Total Issues Found**: [number]
  - Errors: [number]
  - Warnings: [number]
  - Info: [number]
- **Files with Issues**: [number]/[total files]
- **Overall Score**: [X]/100 (based on severity weighting)

## Detailed Findings

### Errors ([count])
[Each error should include file location, description, and suggested fix]

**Example Format:**
```
FILE: src/components/Button.js:LINE 45
DESCRIPTION: Missing return statement in function handleClick
SEVERITY: Error
RULE: consistent-return (eslint)
SUGGESTED FIX: Add return statement or explicitly return undefined
```

### Warnings ([count])
[Same format as errors but for warnings]

### Info ([count])
[Same format for informational messages]

## Recommendations
### Priority Fixes (Address First)
1. [Specific actionable recommendation]
2. [Specific actionable recommendation]

### Code Quality Improvements
1. [Suggestion for improving maintainability]
2. [Suggestion for improving readability]

### Architecture Observations
[Any observations about code structure, coupling, etc. that aren't direct violations but worth noting]

## Trend Analysis (if historical data available)
[Comparison to previous audit runs if applicable]

## Conclusion
[Pass/Fail recommendation based on project quality gates]
- **Status**: [PASS/FAIL/CONDITIONAL PASS]
- **Blocking Issues**: [List of issues that must be fixed before proceeding]
- **Next Steps**: [What needs to happen to resolve remaining issues]