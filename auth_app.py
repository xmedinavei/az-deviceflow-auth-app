import os
import msal
import requests
from datetime import datetime, timedelta
import pytz

# Retrieve CLIENT_ID and TENANT_ID from environment variables
client_id = os.environ.get("CLIENT_ID")
tenant_id = os.environ.get("TENANT_ID")

if not client_id or not tenant_id:
    raise ValueError("CLIENT_ID and TENANT_ID environment variables must be set.")

# Build the authority URL
authority = f"https://login.microsoftonline.com/{tenant_id}"

# Scopes we want to request
scopes = ["User.Read", "Calendars.Read"]

# Initialize the PublicClientApplication
app = msal.PublicClientApplication(
    client_id=client_id,
    authority=authority
)

# Initiate the device flow (headless auth)
flow = app.initiate_device_flow(scopes=scopes)

# Check if we actually got a device code; if not, something failed
if "user_code" not in flow:
    raise ValueError(
        "Failed to create device flow. Error: %s" % str(flow)
    )

print(flow["message"])  # Instructions for the user to go to https://microsoft.com/devicelogin

# Acquire the token by completing the device code flow
result = app.acquire_token_by_device_flow(flow)

def create_calendar_event():
    # Get local timezone
    local_tz = datetime.now().astimezone().tzinfo
    start_time = datetime.now() + timedelta(minutes=5)
    end_time = start_time + timedelta(minutes=30)

    event = {
        "subject": "Study for the AZ-204 exam",
        "body": {
            "contentType": "HTML",
            "content": "I've heard there's a good book from Packt for that."
        },
        "start": {
            "dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": str(local_tz)
        },
        "end": {
            "dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": str(local_tz)
        },
        "location": {
            "displayName": "Wherever you are"
        }
    }
    return event

if "access_token" in result:
    access_token = result["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # ----------------------------------
    # 1. Get user profile (display name)
    # ----------------------------------
    graph_user_url = "https://graph.microsoft.com/v1.0/me"
    user_resp = requests.get(graph_user_url, headers=headers)

    if user_resp.status_code == 200:
        user_data = user_resp.json()
        display_name = user_data.get("displayName", "Unknown")
        print(f"\nWelcome, {display_name}!\n")
    else:
        print("Error fetching user profile:", user_resp.text)

    # ---------------------------
    # 2. Get upcoming calendar events
    # ---------------------------
    # Retrieve up to 5 upcoming events
    events_url = (
        "https://graph.microsoft.com/v1.0/me/events"
        "?$select=subject,organizer,start,end"
        "&$top=5"
        "&$orderby=start/dateTime ASC"
    )
    events_resp = requests.get(events_url, headers=headers)

    if events_resp.status_code == 200:
        events_data = events_resp.json()
        events = events_data.get("value", [])

        if events:
            print("Your upcoming calendar events:")
            for idx, event in enumerate(events, start=1):
                subject = event.get("subject", "No subject")
                organizer_name = event["organizer"]["emailAddress"].get("name", "Unknown")
                start_time = event["start"].get("dateTime")
                end_time = event["end"].get("dateTime")

                print(f"{idx}. Subject: {subject}")
                print(f"   Organizer: {organizer_name}")
                print(f"   Start: {start_time}")
                print(f"   End:   {end_time}\n")
        else:
            print("No upcoming events found.")
    else:
        print("Error fetching events:", events_resp.text)

    # Create calendar event
    try:
        event_data = create_calendar_event()
        events_url = "https://graph.microsoft.com/v1.0/me/events"
        event_resp = requests.post(events_url, headers=headers, json=event_data)

        if event_resp.status_code == 201:
            created_event = event_resp.json()
            print("Your meeting was created with the following details:")
            print(f"Subject: {created_event['subject']}")
            print(f"Location: {created_event['location']['displayName']}")
            print(f"Start: {created_event['start']['dateTime']}")
            print(f"End: {created_event['end']['dateTime']}\n")
        else:
            print("Error creating event:", event_resp.text)

    except Exception as ex:
        print(f"Error creating calendar event: {str(ex)}")

    # Optional: Print the tokens (like in your .NET example)
    print("ID Token:\n", result.get("id_token"), "\n")
    print("Access Token:\n", access_token, "\n")

else:
    # If acquire_token_by_device_flow failed
    print("Failed to acquire token.")
    print(f"Error: {result.get('error')}")
    print(f"Description: {result.get('error_description')}")
