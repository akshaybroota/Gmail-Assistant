# Gmail Assistant Agent

This project implements an intelligent agent designed to interact with your Gmail inbox, providing helpful summaries and information. Built using the `google-adk` library, this agent leverages the Gmail API through a custom `GmailClient` to perform various tasks.

## Overview

The `gmail_assistant` agent is initialized with the `gemini-2.0-flash` model and is described as an agent capable of summarizing emails from the user's inbox. Its primary goal is to assist users with common Gmail-related queries through natural language interaction.

Upon starting, the agent will greet the user with: "Hi, I am your Gmail Assistant. What can I do for you?"

## Capabilities

The agent is currently equipped with the following capabilities:

1.  **List Total Unread Emails:** When asked, the agent can retrieve and provide the total number of unread emails in your inbox.

2.  **Summarize Latest Unread Email:** If requested, the agent can fetch the latest unread email from your primary inbox, extract its content, and provide a summary to the user.

3.  **Search Emails by Keywords:** When instructed to search for an email, the agent will prompt the user to provide keywords. Once the user provides the keywords, the agent will use these keywords to search through the inbox and return information about the matching email (subject and body).

## Architecture

The core components of this project are:

* **`GmailClient` (`tools/gmail_search.py`):** This custom class handles the interaction with the Gmail API. It includes methods to:
    * Authenticate and build the Gmail service.
    * Get the total count of unread emails.
    * Retrieve the body of the latest unread email in the primary inbox.
    * Find emails based on user-provided keywords.

* **`gmail_assistant` (Main Script):** This script initializes the `GmailClient` and then creates an `Agent` using the `google-adk` library. The agent is configured with:
    * A name (`gmail_assistant`).
    * A language model (`gemini-2.0-flash`).
    * A description of its purpose.
    * Instructions on how to behave and the tasks it can perform.
    * A list of tools (methods from the `GmailClient`) that the agent can utilize to fulfill user requests.

## Setup and Usage

To run this agent, you will need to:

1.  **Obtain your Gemini API Key:**
    * Go to [Google AI Studio](https://makersuite.google.com/).
    * Create a new API key.
    * Ensure this API key is accessible in your environment or within your `google-adk` setup.

2.  **Set up Google Cloud Project and Enable Gmail API:**
    * Create a Google Cloud Project.
    * Enable the Gmail API for your project.
    * Configure the OAuth consent screen.

3.  **Create OAuth 2.0 Credentials:**
    * Within your Google Cloud Project, create OAuth 2.0 Client IDs. Choose "Desktop application" as the application type.
    * Download the generated client secrets JSON file.

4.  **Store Secrets File:**
    * Place the downloaded client secrets JSON file in a folder named `tools` within your project directory. The filename is typically `client_secret.json` or similar.

5.  **Install Required Libraries:**
    ```bash
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib google-adk
    ```

6.  **Start the Agent:**
    * After setting up the necessary credentials and installing the libraries, use the `adk web` command in your terminal within the project directory to start the agent interface. This will allow you to interact with the `gmail_assistant` agent through a web browser.

## Further Development

Future development efforts should focus on enhancing the user experience and the agent's interaction capabilities:

* **Voice Interaction:** Implement the ability for users to interact with the agent using voice commands and receive voice responses.
* **Multi-turn Conversations with In-Session Memory:** Enable the agent to maintain context across multiple turns of conversation, remembering previous interactions and user preferences within the same session.