# Product Management Plugin

A product management plugin primarily designed for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — though it also works in Claude Code. Covers the full PM workflow: writing feature specs, managing roadmaps, communicating with stakeholders, synthesizing user research, analyzing competitors, and tracking product metrics.

## Installation

```
claude plugin install product-management@grail-automation
```

## What It Does

This plugin gives you an AI-powered product management partner that can help with:

- **Feature Specs & PRDs** — Generate structured product requirements documents from a problem statement or feature idea. Includes user stories, requirements prioritization, success metrics, and scope management.
- **Roadmap Planning** — Create, update, and reprioritize your product roadmap. Supports Now/Next/Later, quarterly themes, and OKR-aligned formats with dependency mapping.
- **Stakeholder Updates** — Generate status updates tailored to your audience (executives, engineering, customers). Pulls context from connected tools to save you the weekly update grind.
- **User Research Synthesis** — Turn interview notes, survey data, and support tickets into structured insights. Identifies themes, builds personas, and surfaces opportunity areas with supporting evidence.
- **Competitive Analysis** — Research competitors and generate briefs with feature comparisons, positioning analysis, and strategic implications.
- **Metrics Review** — Analyze product metrics, identify trends, compare against targets, and surface actionable insights.

## Commands

| Command | What It Does |
|---|---|
| `/product-management:write-spec` | Write a feature spec or PRD from a problem statement |
| `/product-management:roadmap-update` | Update, create, or reprioritize your roadmap |
| `/product-management:stakeholder-update` | Generate a stakeholder update (weekly, monthly, launch) |
| `/product-management:synthesize-research` | Synthesize user research from interviews, surveys, and tickets |
| `/product-management:competitive-brief` | Create a competitive analysis brief |
| `/product-management:metrics-review` | Review and analyze product metrics |

## Skills

| Skill | What It Covers |
|---|---|
| `feature-spec` | PRD structure, user stories, requirements categorization, acceptance criteria |
| `roadmap-management` | Prioritization frameworks (RICE, MoSCoW), roadmap formats, dependency mapping |
| `stakeholder-comms` | Update templates by audience, risk communication, decision documentation |
| `user-research-synthesis` | Thematic analysis, affinity mapping, persona development, opportunity sizing |
| `competitive-analysis` | Feature comparison matrices, positioning analysis, win/loss analysis |
| `metrics-tracking` | Product metrics hierarchy, goal setting (OKRs), dashboard design, review cadences |

## Example Workflows

### Writing a PRD

```
You: /product-management:write-spec
Claude: What feature or problem are you speccing out?
You: We need to add SSO support for enterprise customers
Claude: [Asks about target users, constraints, success metrics]
Claude: [Generates full PRD with problem statement, user stories, requirements, success metrics, open questions]
```

### Preparing a Stakeholder Update

```
You: /product-management:stakeholder-update
Claude: What type of update? (weekly, monthly, launch, ad-hoc)
You: Weekly update for the exec team
Claude: [Pulls context from project management tool, chat, and docs]
Claude: [Generates executive summary with progress, decisions, risks, and next milestones]
```

### Synthesizing User Research

```
You: /product-management:synthesize-research
Claude: What research do you want to synthesize? You can paste interview notes, upload files, or I can pull from connected sources.
You: [Pastes 8 interview transcripts]
Claude: [Identifies themes, patterns, and insights across interviews]
Claude: [Generates synthesis with key findings, personas, opportunity areas, and evidence]
```

### Competitive Analysis

```
You: /product-management:competitive-brief
Claude: Which competitor(s) or feature area do you want to analyze?
You: Compare our onboarding flow to [competitor A] and [competitor B]
Claude: [Researches competitor onboarding approaches]
Claude: [Generates brief with feature comparison, strengths/weaknesses, and strategic implications]
```

## Data Sources

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](CONNECTORS.md).

Connect your project management and communication tools for the best experience. Without them, provide context manually.

**Default integrations:**
- Chat (Slack MCP) for team context and stakeholder threads
- Project tracker (Linear, Asana, monday.com, ClickUp, Atlassian MCP) for roadmap integration, ticket context, and status tracking
- Knowledge base (Notion MCP with `ntn` CLI pilot for pages/data sources/files) for existing specs, research, and meeting notes
- Design (Figma MCP) for design context and handoff
- Product analytics (Amplitude MCP, Pendo MCP) for usage data, metrics, and behavioral analysis
- User feedback (Intercom MCP) for support tickets, feature requests, and user conversations
- Meeting transcription (Fireflies MCP) for meeting notes and discussion context

**Additional options:**
- See [CONNECTORS.md](CONNECTORS.md) for alternative tools in each category
