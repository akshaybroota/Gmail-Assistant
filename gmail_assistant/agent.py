import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from tools.gmail_search import GmailClient

gmail_agent = GmailClient()

root_agent = Agent(
    name="gmail_assistant",
    model="gemini-2.0-flash",
    description=(
        "Agent to summarize the emails from user's inbox"
    ),
    instruction=(
        """
        You should start by greeting the user with - "Hi, I am your Gmail Assistant. What can I do for you?"
        You are a helpful agent. Examples of stuff you can do:
        1. If asked, list the total number of unread emails.
        2. If asked to list the latest unread email, you need to get and summarize the latest unread email for the user.
        3. If the user asks you to search an email from the inbox, ask users to specify keywords. When the user has shared keywords, send it as a string to the function.  
        
        """
    ),
    tools=[gmail_agent.get_unread_email_count, gmail_agent.get_latest_unread_primary_email_body, gmail_agent.find_email_by_keywords],
)