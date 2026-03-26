## Workato CLI example use cases

The following example use cases describe how you can use the Workato Platform CLI for individual developer, team and organization, automation, and enterprise integration workflows.

## Individual developer example use cases

You can use the Platform CLI for individual developer use cases, such as local recipe development and multi-environment management.

### Local recipe development

Edit and validate integration recipes locally before deployment to avoid production issues.

#### Benefits

- Catch syntax errors early
- Version control integration recipes
- Test recipes using different profiles for development, staging, and production
- Faster development cycles

#### Commands

```bash
workato recipes validate --path ./recipes/RECIPE-NAME.json
workato push --restart-recipes
```

#### Example

```bash
% workato recipes validate --path ./customer_onboarding/google_calendar_recipe.recipe.json
✅ Recipe validation passed (0.1s)                                       
📄 File: google_calendar_recipe.recipe.json
% workato push --restart-recipes
✅ Package created: customer_onboarding.zip (0.1s)         
✅ Package uploaded successfully (0.9s)         
  📊 Import ID: 203018
  📈 Status: in_progress
🎉 Import completed successfully                   
📋 Recipe Import Results:
  ✅ 4 recipe(s): No restart needed
  ⚠️ 1 recipe(s): Updated but stopped
  📊 Summary: 4/5 recipes imported successfully
```

### Multi-environment management

Manage development, staging, and production environments with separate configurations.

#### Benefits

- Isolated testing environments
- Safer promotion workflows
- Environment-specific configurations
- Rollback capabilities

#### Workflow

```bash
# Development
workato profiles use dev
workato push

# Staging
workato profiles use staging
workato pull
workato push --restart-recipes

# Production
workato profiles use production
workato pull
```

#### Example

```bash
# Development 
% workato profiles use dev
✅ Set 'dev' as profile for current workspace
   Workspace: /Users/user-directory/workato
   Project config also updated: customer_onboarding
% workato push
✅ Package created: customer_onboarding.zip (0.1s)         
✅ Package uploaded successfully (0.9s)         
  📊 Import ID: 203022
  📈 Status: in_progress
🎉 Import completed successfully     
📋 Recipe Import Results:
  ✅ 5 recipe(s): No restart needed

# Staging
% workato profiles use staging
✅ Set 'staging' as profile for current workspace
   Workspace: /Users/user-directory/workato
   Project config also updated: customer_onboarding
% workato pull
Pulling latest changes for project: customer_onboarding
✅ Export manifest created: 39763 (0.9s)    
✅ Export package triggered: 203024 (0.5s)   
✅ Package ready for download (2.4s)                
✅ Package downloaded (0.4s)           
✅ Project assets extracted (0.1s)  
✅ Project is already up to date
% workato push --restart-recipes
✅ Package created: customer_onboarding.zip (0.1s)         
✅ Package uploaded successfully (0.8s)         
  📊 Import ID: 203025
  📈 Status: in_progress
🎉 Import completed successfully                   
📋 Recipe Import Results:
  ✅ 5 recipe(s): No restart needed

# Production 
% workato profiles use production
✅ Set 'production' as profile for current workspace
   Workspace: /Users/user-directory/workato
   Project config also updated: customer_onboarding
% workato pull
Pulling latest changes for project: customer_onboarding
✅ Export manifest created: 39765 (0.8s)    
✅ Export package triggered: 203028 (0.4s)   
✅ Package ready for download (2.5s)                
✅ Package downloaded (0.7s)           
✅ Project assets extracted (0.1s)  
✅ Project is already up to date
```

## Team and organization example use cases

You can use the Platform CLI for team and organization use cases, such as collaboration, CI/CD pipeline integration, and recipe lifecycle management.

### Team collaboration

Share recipes and connections across development teams with standardized workflows.

#### Benefits

- Consistent project structures
- Shared connection configurations
- Code review processes for integrations
- Knowledge sharing

#### Workflow

```bash
# Developer A
workato push --include-tags

# Developer B
workato pull
```

#### Example

```bash
# Developer A
% workato push --include-tags
✅ Package created: customer_onboarding.zip (0.1s)         
✅ Package uploaded successfully (0.9s)         
  📊 Import ID: 203030
  📈 Status: in_progress
🎉 Import completed successfully     
📋 Recipe Import Results:
  ✅ 5 recipe(s): No restart needed

# Developer B
% workato pull
Pulling latest changes for project: customer_onboarding
✅ Export manifest created: 39766 (0.5s)    
✅ Export package triggered: 203031 (0.6s)   
✅ Package ready for download (2.4s)                
✅ Package downloaded (0.4s)           
✅ Project assets extracted (0.1s)  
✅ Project is already up to date
```

### CI/CD pipeline integration

Automate recipe deployment as part of build and release pipelines.

#### Benefits

- Consistent deployment process
- Automated validation gates
- Environment promotion workflows
- Reduced manual errors

#### Implementation

```bash
# In CI pipeline
workato recipes validate --path ./recipes/*.json
workato push --restart-recipes --include-tags
```

#### Example

```bash
% workato recipes validate --path ./customer_onboarding/google_calendar_recipe.recipe.json
✅ Recipe validation passed (2.0s)                                       
  📄 File: google_calendar_recipe.recipe.json
% workato push --restart-recipes --include-tags
✅ Package created: customer_onboarding.zip (0.1s)         
✅ Package uploaded successfully (1.0s)         
  📊 Import ID: 203034
  📈 Status: in_progress
🎉 Import completed successfully     
📋 Recipe Import Results:
  ✅ 5 recipe(s): No restart needed
```

### Recipe lifecycle management

Standardize how recipes are created, tested, deployed, and monitored across teams.

#### Operations

- Validate recipes before deployment
- Start/stop recipes for maintenance
- Monitor recipe execution
- Update connections programmatically

#### Commands

```bash
workato recipes validate --path ./recipe.json
workato recipes start --id 12345
workato recipes stop --id 67890
workato connections create-oauth --parent-id 123
```

## Automation

You can use the Platform CLI for automated connection management, and error resolution and monitoring.

### Automated connection management

You can handle OAuth flows and credential management programmatically.

#### Benefits

- Eliminate manual OAuth setup
- Bulk connection creation
- Secure credential handling
- Environment-specific configurations

#### Commands

```bash
workato connections create-oauth --parent-id 123
workato connections get-oauth-url 456
```

You can automatically diagnose and resolve common integration issues.

#### Benefits

- Proactive issue detection
- Automated troubleshooting
- Performance monitoring
- Reduced downtime

#### Monitoring

```bash
workato recipes list --running
workato recipes list --stop-cause trigger_errors_limit
```

#### Example

```bash
% workato recipes list --running
📋 Recipes (1 found) - (0.8s)                                                
  🔍 Filters: folder 75510, running recipes only

  ▶️ Google Calendar Recipe
    🆔 ID: 366663
    📊 Status: Running
    📱 Trigger App: clock
    🔧 Action Apps: google_calendar
    ⚙️  Config Apps: clock, google_calendar (Account: 71959)
    📁 Folder ID: 75510
    📊 Jobs: 24 succeeded, 0 failed
    🕐 Last Run: 2025-10-28T12:49:55.834000-07:00
    📅 Created: 2025-03-25T11:58:33.598000-07:00
    👤 Author: Amy Peak
    📝 Description: When there is a trigger on a specified schedule, do action
% workato recipes list --stop-cause trigger_errors_limit
📋 Recipes (0 found) - (0.4s)                                                                
  🔍 Filters: folder 75510, stopped due to: trigger_errors_limit
  ℹ️  No recipes found
% workato recipes list --stop-cause trigger_errors_limit
📋 Recipes (0 found) - (0.4s)                                                                
  🔍 Filters: folder 75510, stopped due to: trigger_errors_limit
  ℹ️  No recipes found
```

## Enterprise integration scenarios

You can use the Platform CLI for enterprise integration scenarios, such as API management, data operations, and project organization.

### API management

Centralize API collection management and deployment across multiple environments.

#### Benefits

- Consistent API definitions
- Version control for API specs
- Automated API deployment
- Environment-specific configurations

#### Implementation

```bash
workato api-collections create --name "Customer API" --project-id 123
```

### Data operations

Manage large-scale data synchronization and transformation workflows.

#### Benefits

- Batch processing capabilities
- Data validation and cleansing
- Error handling and retry logic
- Audit trails and monitoring

### Project organization

You can structure projects for scalability and maintainability across large teams.

#### Benefits

- Consistent folder structures
- Shared naming conventions
- Access control management
- Dependency tracking

#### Organization

- Group recipes by business function
- Use descriptive connection names
- Implement consistent tagging
- Regular cleanup and maintenance


**Last updated:** 11/3/2025, 7:56:11 PM