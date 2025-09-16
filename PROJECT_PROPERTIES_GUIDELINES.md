# Project Properties Guidelines and Recommendations

A comprehensive guide for inputting useful and correct properties for projects in the Portfolio Management System.

## Overview

This document provides guidelines for entering project properties that ensure data quality, consistency, and analytical value across the portfolio management system. The system supports two main data models:

1. **Standard Portfolio Model** (`toy-example/toy-data/`) - Traditional project management approach
2. **Advanced Evaluation Model** (`dl-example/`) - Research-focused with qualitative evaluation translation

## Table of Contents

- [Core Project Properties](#core-project-properties)
- [Strategic Dimensions](#strategic-dimensions)
- [Advanced Properties (Research Model)](#advanced-properties-research-model)
- [Data Quality Guidelines](#data-quality-guidelines)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)
- [Validation Checklist](#validation-checklist)
- [Best Practices by Use Case](#best-practices-by-use-case)

## Core Project Properties

### Essential Identifiers

#### `project_id`
- **Format**: Use consistent naming convention (e.g., `PRJ001`, `LOGOS_CORE_001`)
- **Requirements**: 
  - Unique across entire portfolio
  - No spaces or special characters except underscore/hyphen
  - Maximum 20 characters
- **Examples**: 
  - ✅ `PRJ001`, `NIMBUS_ETH2_001`, `STATUS_APP_001`
  - ❌ `Project 1`, `PRJ-001 (New)`, `Very Long Project Name ID`

#### `name`
- **Format**: Clear, descriptive project name
- **Requirements**:
  - 5-80 characters
  - Avoid abbreviations unless widely understood
  - Use title case
- **Examples**:
  - ✅ `Customer Portal Redesign`, `Nimbus Ethereum 2.0 Client`
  - ❌ `CPR`, `proj1`, `THE REALLY LONG PROJECT NAME THAT GOES ON FOREVER`

#### `description`
- **Format**: Concise but comprehensive project summary
- **Requirements**:
  - 20-500 characters
  - Include key objectives and deliverables
  - Avoid technical jargon for stakeholder clarity
- **Template**: `[Action] [Target] to [Outcome] by [Method]`
- **Examples**:
  - ✅ `Modernize customer-facing web portal to improve user experience and reduce support tickets`
  - ❌ `Portal stuff`, `Update the thing`

### Status and Timeline Properties

#### `status`
- **Valid Values**: `Planning`, `Active`, `On Hold`, `Completed`, `Cancelled`
- **Guidelines**:
  - Update regularly (at least weekly for active projects)
  - Use `On Hold` for temporary suspensions, `Cancelled` for permanent termination
  - `Planning` for approved but not yet started projects

#### `start_date` / `end_date`
- **Format**: `YYYY-MM-DD` (ISO 8601)
- **Requirements**:
  - Start date must be <= end date
  - Use realistic estimates based on similar projects
  - Include buffer time for dependencies and risks
- **Guidelines**:
  - For planning phase: Use target dates with 20-30% buffer
  - For active projects: Update based on current progress
  - Consider dependencies when setting dates

#### `completion_percentage`
- **Range**: 0-100 (integer)
- **Guidelines**:
  - Base on deliverables completed, not time elapsed
  - Update at least bi-weekly
  - Use milestone-based calculation for accuracy
- **Calculation**: `(Completed Milestones / Total Milestones) × 100`

### Financial Properties

#### `budget_allocated` / `budget_spent`
- **Format**: Numeric values in base currency (no commas)
- **Requirements**:
  - `budget_spent` <= `budget_allocated`
  - Include all project costs (labor, materials, overhead)
  - Update `budget_spent` monthly minimum
- **Guidelines**:
  - Include 10-15% contingency in allocated budget
  - Track actual vs. planned spending trends
  - Consider currency fluctuations for multi-region projects

#### `construction_cost` (Research Model)
- **Range**: 0.1 - 10.0 (normalized scale)
- **Guidelines**:
  - Relative to portfolio average (1.0 = average cost)
  - Include total cost of ownership
  - Consider opportunity costs

### Priority and Risk Properties

#### `strategic_priority`
- **Valid Values**: `Critical`, `High`, `Medium`, `Low`
- **Guidelines**:
  - Limit `Critical` to <20% of portfolio
  - Align with organizational strategic objectives
  - Review quarterly and adjust based on business changes

#### `risk_level`
- **Valid Values**: `Low`, `Medium`, `High`, `Critical`
- **Assessment Criteria**:
  - **Low**: Well-understood technology, experienced team, clear requirements
  - **Medium**: Some unknowns, moderate complexity, standard timeline
  - **High**: New technology, tight timeline, complex dependencies
  - **Critical**: Experimental approach, multiple high-risk factors

## Strategic Dimensions

### Scoring Guidelines (1-10 Scale)

#### `innovation_score`
- **1-3**: Incremental improvements to existing processes
- **4-6**: Moderate innovation with proven technologies
- **7-8**: Significant innovation with some new approaches
- **9-10**: Breakthrough innovation, cutting-edge technology

#### `market_impact_score`
- **1-3**: Internal efficiency gains only
- **4-6**: Moderate customer/market benefits
- **7-8**: Significant competitive advantage
- **9-10**: Market-disrupting potential

#### `strategic_fit_score`
- **1-3**: Tangential to core strategy
- **4-6**: Supports strategic objectives
- **7-8**: Directly advances key strategic goals
- **9-10**: Critical to strategic success

#### `customer_value_score`
- **1-3**: Minimal customer impact
- **4-6**: Moderate customer benefits
- **7-8**: Significant customer value creation
- **9-10**: Transformational customer experience

### ROI Properties

#### `roi_projected` / `roi_actual`
- **Format**: Decimal ratio (e.g., 1.5 = 150% return)
- **Calculation**: `(Benefits - Costs) / Costs`
- **Guidelines**:
  - Include quantifiable benefits only
  - Use 3-year time horizon for calculation
  - Update `roi_actual` annually after project completion

## Advanced Properties (Research Model)

### Normalized Value Scales (0.0 - 1.0)

#### `strategic_value`
- **Range**: 0.0 - 1.0
- **Guidelines**:
  - Relative to portfolio maximum
  - Consider long-term strategic impact
  - Weight multiple strategic dimensions

#### `technical_complexity`
- **Range**: 0.0 - 1.0
- **Assessment Factors**:
  - Technology maturity
  - Integration complexity
  - Team expertise requirements
  - Architecture complexity

#### `market_impact`
- **Range**: 0.0 - 1.0
- **Considerations**:
  - Market size and growth potential
  - Competitive positioning
  - Customer adoption likelihood
  - Revenue impact potential

#### `resource_requirement`
- **Range**: 0.0 - 1.0
- **Includes**:
  - Human resources (FTE)
  - Financial investment
  - Infrastructure needs
  - Opportunity costs

### Relationship Properties

#### `cooperation_projects`
- **Format**: JSON array of project IDs
- **Guidelines**:
  - List projects that benefit from joint execution
  - Include shared resource synergies
  - Consider knowledge transfer opportunities

#### `precedence_projects`
- **Format**: JSON array of project IDs
- **Requirements**:
  - List projects that must complete before this project can start
  - Include technical dependencies
  - Consider resource availability dependencies

#### `exclusive_projects`
- **Format**: JSON array of project IDs
- **Guidelines**:
  - List projects that cannot run simultaneously
  - Include resource conflicts
  - Consider strategic conflicts

### Technology and Team Properties

#### `technology_stack`
- **Format**: JSON array of technologies
- **Guidelines**:
  - Use standard technology names
  - Include primary technologies only
  - Consider skill availability in organization

#### `team_size`
- **Format**: Integer (number of FTE)
- **Guidelines**:
  - Include all dedicated team members
  - Use average team size over project duration
  - Consider ramp-up and ramp-down periods

## Data Quality Guidelines

### Consistency Requirements

1. **Date Formats**: Always use `YYYY-MM-DD` format
2. **Currency**: Use consistent base currency across portfolio
3. **Naming**: Follow established naming conventions
4. **Updates**: Maintain regular update schedules
5. **Validation**: Implement data validation rules

### Completeness Standards

#### Required Fields (Cannot be null/empty)
- `project_id`, `name`, `description`
- `status`, `start_date`, `strategic_priority`
- `budget_allocated`, `risk_level`

#### Recommended Fields (Should be populated)
- `end_date`, `completion_percentage`
- `budget_spent`, `project_manager`
- Strategic dimension scores

#### Optional Fields (Context-dependent)
- `roi_actual` (only after project completion)
- Advanced relationship properties
- Detailed technology specifications

### Accuracy Guidelines

1. **Regular Updates**: Update dynamic fields (status, completion, budget_spent) at least bi-weekly
2. **Validation Rules**: Implement automated checks for data consistency
3. **Audit Trail**: Maintain `last_updated` timestamps
4. **Review Cycles**: Quarterly review of all strategic scores and priorities

## Common Mistakes to Avoid

### Data Entry Errors

❌ **Inconsistent Date Formats**
```
start_date: "Jan 15, 2025"  # Wrong
start_date: "15/01/2025"    # Wrong
start_date: "2025-01-15"    # Correct
```

❌ **Unrealistic Completion Percentages**
```
# Project started yesterday, 50% complete - unrealistic
# Base on actual deliverables completed
```

❌ **Vague Descriptions**
```
description: "Update system"           # Too vague
description: "Fix bugs"                # Not descriptive
description: "Modernize customer portal to improve user experience and reduce support tickets"  # Good
```

### Strategic Assessment Errors

❌ **Grade Inflation**
```
# Not every project can be "Critical" priority
# Use normal distribution across priority levels
```

❌ **Inconsistent Scoring**
```
# Ensure scoring criteria are applied consistently
# Document scoring rationale for major projects
```

❌ **Ignoring Dependencies**
```
# Always consider project interdependencies
# Update dependency lists when project scope changes
```

### Financial Tracking Issues

❌ **Incomplete Cost Tracking**
```
# Include all costs: labor, materials, overhead, opportunity costs
# Don't forget indirect costs and shared resources
```

❌ **Unrealistic Budgets**
```
# Include contingency buffers (10-15%)
# Base estimates on historical data from similar projects
```

## Validation Checklist

### Before Project Entry
- [ ] Project ID follows naming convention and is unique
- [ ] All required fields are populated
- [ ] Dates are in correct format and logical order
- [ ] Budget figures are realistic and complete
- [ ] Strategic scores are calibrated against portfolio

### During Project Execution
- [ ] Status updates are current (within 2 weeks)
- [ ] Completion percentage reflects actual progress
- [ ] Budget spent is accurate and up-to-date
- [ ] Risk level reflects current project state
- [ ] Dependencies are still valid

### Project Completion
- [ ] Final status is set to "Completed" or "Cancelled"
- [ ] Actual end date is recorded
- [ ] Final budget spent is recorded
- [ ] ROI actual is calculated and recorded
- [ ] Lessons learned are documented

## Best Practices by Use Case

### Executive Reporting
- **Focus**: High-level strategic metrics
- **Key Properties**: `strategic_priority`, `strategic_fit_score`, `roi_projected`, `completion_percentage`
- **Update Frequency**: Monthly
- **Quality Requirements**: High accuracy on financial and strategic data

### Resource Planning
- **Focus**: Resource allocation and utilization
- **Key Properties**: `team_size`, `resource_requirement`, `start_date`, `end_date`
- **Update Frequency**: Weekly
- **Quality Requirements**: Accurate timeline and resource data

### Risk Management
- **Focus**: Risk identification and mitigation
- **Key Properties**: `risk_level`, `technical_complexity`, `dependencies`
- **Update Frequency**: Bi-weekly
- **Quality Requirements**: Current risk assessments and dependency tracking

### Portfolio Optimization
- **Focus**: Mathematical optimization inputs
- **Key Properties**: All normalized scores (0.0-1.0), relationship arrays
- **Update Frequency**: Quarterly
- **Quality Requirements**: Consistent scoring methodology, complete relationship data

### Research and Development
- **Focus**: Innovation and technical advancement
- **Key Properties**: `innovation_level`, `technology_stack`, `technical_complexity`
- **Update Frequency**: Monthly
- **Quality Requirements**: Accurate technical assessments, current technology lists

## Data Validation Rules

### Automated Checks
```sql
-- Date consistency
CHECK (start_date <= end_date)
CHECK (end_date >= CURRENT_DATE OR status IN ('Completed', 'Cancelled'))

-- Budget consistency  
CHECK (budget_spent <= budget_allocated)
CHECK (budget_allocated > 0)

-- Percentage ranges
CHECK (completion_percentage >= 0 AND completion_percentage <= 100)

-- Score ranges (for strategic dimensions)
CHECK (innovation_score >= 1 AND innovation_score <= 10)
CHECK (strategic_value >= 0.0 AND strategic_value <= 1.0)
```

### Business Rules
- Maximum 20% of projects can have "Critical" priority
- Projects in "Planning" status must have completion_percentage = 0
- Projects in "Completed" status must have completion_percentage = 100
- Active projects must have recent updates (within 14 days)

## Conclusion

Following these guidelines ensures:
- **Data Quality**: Consistent, accurate, and complete project information
- **Analytical Value**: Data suitable for portfolio optimization and analysis
- **Stakeholder Confidence**: Reliable information for decision-making
- **System Efficiency**: Optimized data for visualization and reporting tools

Regular adherence to these guidelines, combined with automated validation and periodic reviews, will maintain a high-quality project portfolio dataset that supports effective strategic decision-making.

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Next Review**: March 2025
