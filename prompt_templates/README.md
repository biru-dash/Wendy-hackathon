# Prompt Templates

This folder contains example instruction templates for agents. Use these as references when modifying agent instructions during the hackathon.

## Structure

Each agent has two template versions:
- **`[agent]_basic.txt`**: Extremely simple, minimal instructions (baseline)
- **`[agent]_advanced.txt`**: Detailed, goal-specific instructions (enhanced)

## Available Templates

### Market Trends Analyst
- `data_collection_basic.txt` - Basic data collection instructions
- `data_collection_advanced.txt` - Advanced data collection with goal-specific guidance
- `research_synthesis_basic.txt` - Basic research synthesis instructions
- `research_synthesis_advanced.txt` - Advanced research synthesis with structured output

### Customer Insights
- `behavioral_analysis_basic.txt` - Basic behavioral analysis instructions
- `behavioral_analysis_advanced.txt` - Advanced behavioral analysis with Gen Z breakfast focus
- `sentiment_analysis_basic.txt` - Basic sentiment analysis instructions
- `sentiment_analysis_advanced.txt` - Advanced sentiment analysis with messaging cues

### Offer Design
- `offer_design_basic.txt` - Basic offer design instructions
- `offer_design_advanced.txt` - Advanced offer design with comprehensive output format

## How to Use

1. **Start with Basic**: The actual instruction files in `src/` start with basic versions
2. **Compare**: Look at the advanced versions to see what improvements can be made
3. **Modify**: Copy relevant sections from advanced templates to improve the basic instructions
4. **Test**: Run the agent and observe how the changes affect output quality

## Key Differences

### Basic Instructions
- Minimal guidance
- Generic tasks
- No goal-specific focus
- Simple output format
- Limited constraints

### Advanced Instructions
- Detailed role descriptions
- Goal-specific guidance (Gen Z breakfast in Q1)
- Structured output formats
- Clear constraints and guidelines
- Evidence citation requirements
- Business context and rationale

## Example: Improving Instructions

**Basic**: "Analyze customer data and return insights."

**Advanced**: 
- "Focus analysis on Gen Z customer segments (ages 18-27)"
- "Analyze breakfast-specific behavioral patterns (6am-11am visits)"
- "Always include percentage comparisons when analyzing segments"
- "Compare metrics across at least 3 different Gen Z segments"

The advanced version provides specific, actionable guidance that leads to better, more focused outputs.

