# Mermaid Diagrams for Multi-Agent System

This directory contains Mermaid diagrams that visualize the architecture of the Wendy's AI Agents Hackathon multi-agent system.

## Diagrams

1. **01_overall_system.mmd** - High-level overview of the entire multi-agent system showing how all components work together
2. **02_market_trends_analyst.mmd** - Market Trends Analyst agent and its sub-agents (Data Collection, Research Synthesis)
3. **03_customer_insights.mmd** - Customer Insights agent and its parallel sub-agents (Behavioral Analysis, Profile Synthesizer, Sentiment Analysis)
4. **04_competitor_intelligence.mmd** - Competitor Intelligence agent and its sequential sub-agents (Target Identification, Research Orchestrator, Competitor Analysis, Whitespace Synthesizer)
5. **05_offer_design.mmd** - Offer Design agent showing both the full 4-step pipeline and the simplified single-agent version used in the hackathon
6. **06_marketing_orchestrator.mmd** - Marketing Orchestrator showing how it coordinates all sub-agents in sequence

## Converting to Images

### Option 1: Using Mermaid CLI (Recommended)

1. Install Mermaid CLI:
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

2. Convert a diagram to PNG:
   ```bash
   mmdc -i 01_overall_system.mmd -o 01_overall_system.png
   ```

3. Convert all diagrams:
   ```bash
   # Windows PowerShell
   Get-ChildItem *.mmd | ForEach-Object { mmdc -i $_.Name -o "$($_.BaseName).png" }
   
   # Mac/Linux
   for file in *.mmd; do mmdc -i "$file" -o "${file%.mmd}.png"; done
   ```

### Option 2: Using Online Mermaid Editor

1. Go to https://mermaid.live/
2. Copy the contents of a `.mmd` file
3. Paste into the editor
4. Click "Download PNG" or "Download SVG"

### Option 3: Using VS Code Extension

1. Install the "Markdown Preview Mermaid Support" extension in VS Code
2. Open a `.mmd` file
3. Use the preview feature to view the diagram
4. Export as image using the extension's export feature

### Option 4: Using GitHub/GitLab

1. Create a markdown file with the diagram:
   ````markdown
   ```mermaid
   [paste diagram content here]
   ```
   ````
2. View the rendered diagram on GitHub/GitLab
3. Use browser tools to save as image

## Diagram Color Scheme

- **Blue** (#e1f5ff): Marketing Orchestrator (root agent)
- **Orange** (#fff3e0): Market Trends Analyst
- **Purple** (#f3e5f5): Customer Insights
- **Green** (#e8f5e9): Competitor Intelligence
- **Pink** (#fce4ec): Offer Design
- **Light Green** (#c8e6c9): Final outputs
- **Yellow** (#fff9c4): Data sources (BigQuery)
- **Dashed lines**: Optional components or data flow

## Diagram Types

- **SequentialAgent**: Agents that run in sequence (→)
- **ParallelAgent**: Agents that run simultaneously (parallel branches)
- **LlmAgent**: Single agent using Large Language Model
- **Tools**: External tools/functions available to agents
- **Data Sources**: BigQuery databases, web sources, etc.

## Notes

- The Competitor Intelligence agent is shown as optional (dashed lines) as it's commented out in the hackathon version
- The Offer Design diagram shows both the full 4-step pipeline and the simplified single-agent version
- All diagrams use consistent color coding for easy identification of agent types

