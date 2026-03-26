## Workato Platform CLI quick start

This guide walks you through the essential steps to get started with the Workato Platform CLI. You'll learn how to set up your environment, work with recipes and connections, and establish an efficient development workflow.

## Key development workflow

1

Initialize: Configure API credentials with `workato init`.

2

Manage Projects: Use `workato projects list` and `workato projects use name`.

3

Edit Recipes: Develop JSON recipe files locally.

4

Validate: Run `workato recipes validate` to check syntax.

5

Setup Connections: Create OAuth connections with `workato connections create`.

6

Deploy: Push changes with `workato push`.

7

Monitor: Show recipe executions with `workato recipes list --running`.

## Initial commands

Start using the Platform CLI with the following commands.

List available commands:

```bash
workato --help
```

List your recipes:

```bash
workato recipes list
```

List your connections:

```bash
workato connections list
```

List current project details:

```bash
workato workspace
```

## Example recipe workflow

Validate a recipe file.

```bash
workato recipes validate --path ./my-recipe.json
```

Push local files to your current Workato project.

```bash
workato push
```

Pull local files from your current Workato project.

```bash
workato pull
```

This section provides suggested initial actions for different roles.

### Individual developers

Complete the following steps for local-first development with validation and testing:

1

Configure your environment with `workato init`.

2

Use `workato recipes validate` for local development.

3

Set up profiles for your environments with `workato profiles use NAME`.

### Development teams

Development teams can use the Platform CLI for the following collaborative workflows with version control integration tasks:

- Establish shared project structures.
- Implement code review processes for recipes.
- Use CI/CD pipelines for deployments.

### Enterprise organizations

Enterprise organizations can use the Platform CLI for the following scalable automation with governance and monitoring tasks:

- Create standardized development workflows.
- Implement proper access controls and environments.
- Use monitoring and alerting for production systems.

  
**Last updated:** 11/3/2025, 7:56:11 PM