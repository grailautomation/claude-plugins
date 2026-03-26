## Workato Platform CLI

The Workato Platform CLI is a modern, type-safe command-line interface for the Workato API, designed to help developers build, validate, and manage Workato recipes, connections, and projects.

Refer to the Workato [Developer API](https://docs.workato.com/en/workato-api.html) and [Embedded API](https://docs.workato.com/en/oem/oem-api.html) for more information about the APIs you can use with the Platform CLI.

## Features

The Workato Platform CLI provides the following features:

- **Project management**: Create, push, pull, and manage Workato projects
- **Recipe operations**: Validate, start, stop, and manage recipes
- **Connection management**: Create and manage OAuth connections
- **API integration**: Manage API clients, collections, and endpoints

Refer to [Use cases examples](https://docs.workato.com/platform-cli/use-cases.html) for more information about these features.

## Prerequisites

The Workato Platform CLI requires the following:

- Python 3.11 or later
- Valid Workato account and API token
- Network access to Workato API endpoints

Workato recommends using the CLI with a version control system, such as Git.

## Authentication

To use the Platform CLI, you must create an API client with a client role that authorizes access to the required API endpoints. Creating the API client generates the API token you'll need to configure the CLI.

### Create a client role

The Platform CLI needs access to specific API endpoints to manage projects, recipes, connections, and API collections.

Complete the following steps to create a client role that defines this API access:

1

Go to **Workspace admin > API clients > Client roles**.

2

Click **Add client role**.

3

Enter a **Name** that describes your client role.

4

Select the following in the **Projects** tab:

- **Projects & folders**: Select all.
- **Connections**: Select all.
- **Recipes**: Select all.
- **Recipe Versions**: Select all.
- **Recipe lifecycle management**: Select all.
- **Export manifests**: Select all.

5

Select the following in the **Tools** tab:

- **Collections & endpoints**
	- List collections
		- Create collection
		- List endpoints in a collection
		- Enable endpoint
		- Disable endpoint

6

Select the following in the **Admin** tab:

- **Workspace details**: Select all.

7

Click **Save changes**.

Refer to [configuring API clients and roles](https://docs.workato.com/workato-api/api-clients.html) for detailed instructions.

### Create an API client

Complete the following steps to create an API client and associate it with the [client role you created](https://docs.workato.com/en/platform-cli.html#client-role):

1

Go to **Workspace admin > API clients** in Workato.

2

Click **Create API client**.

3

Enter a **Name** for your API client.

4

Select the client role that you [created above](https://docs.workato.com/en/platform-cli.html#client-role). This authorizes your API client to access the endpoints defined in the client role.

5

Use the **Environment access** drop-down menu to specify the environment that your API client can access in your workspace. To allow access to another environment, you must create a separate API client.

6

Use the **Project access** drop-down menu to specify whether the API client can access all projects or only specific projects in your workspace.

7

Enter any **Allowed IPs**.

8

Click **Create client**.

9

Copy and save your API token. You'll need this token when you [configure the Platform CLI](https://docs.workato.com/en/platform-cli.html#configure-the-platform-cli).

## Install the Platform CLI

Complete the following steps to install the Platform CLI:

1

Run `pip install workato-platform-cli` to install the CLI.

2

Run `workato --version` to verify your installation was successful.

## Configure the Platform CLI

1

Run `workato init` to initialize the CLI configuration. The CLI returns a welcome message, including your workspace root.

Configure your profile. Enter a profile name to use a new profile, or press enter to use the default profile.

For example:

```bash
📋 Step 1: Configure profile
Enter profile name [default]:
```

Select your Workato region from the following options:

```bash
[?] Select your Workato region:
   US Data Center (https://www.workato.com)
   EU Data Center (https://app.eu.workato.com)
   JP Data Center (https://app.jp.workato.com)
   SG Data Center (https://app.sg.workato.com)
   AU Data Center (https://app.au.workato.com)
   IL Data Center (https://app.il.workato.com)
   Developer Sandbox (https://app.trial.workato.com)
 > Custom URL
```

Enter your API token. Your API token starts with `wrk` and has an ending that matches the type of environment. For example, `wrkprod-` for production environments.

For example:

```bash
🔐 Enter your API token
Enter your Workato API token: wrkprod-**************
✅ Authenticated as: User Name
✅ Profile: default
```

STORE PROJECTS IN A DIRECTORY

Workato recommends creating a directory to store your projects in to maintain organization.

Select the project you plan to use with the Platform CLI. Use the project that contains the recipes or connections you plan to interact with.

For example:

```bash
📁 Step 2: Setup project
[?] Select a project:
   Create new project
   Home (ID: 75422)
   Development projects (ID: 61943)
   Sales automation project (ID: 61940)
 > Customer Onboarding (ID: 60715)
```

Enter `y` to proceed with initializing even though the project folder isn't empty. This adds configuration files or other setup files to your existing project. Enter `N` to stop initializing and prevent changes to your project folder.

```bash
⚠️  Directory '/Users/workato/Customer Onboarding' is not empty.
Proceed with initialization? This may overwrite or delete files. [y/N]: y
```

You see a message indicating if the initialization was successful, for example:

```bash
✅ Successfully pulled project changes (+324 -0)
🎉 Project setup complete!
```

7

Run `workato workspace` to verify your workspace is configured successfully.

  
**Last updated:** 1/5/2026, 9:44:20 PM