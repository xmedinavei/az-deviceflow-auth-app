import os
import msal
import requests

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

if "access_token" in result:
    access_token = result["access_token"]

    # ----------------------------------
    # 1. Get user profile (display name)
    # ----------------------------------
    graph_user_url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
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

    # Optional: Print the tokens (like in your .NET example)
    print("ID Token:\n", result.get("id_token"), "\n")
    print("Access Token:\n", access_token, "\n")

else:
    # If acquire_token_by_device_flow failed
    print("Failed to acquire token.")
    print(f"Error: {result.get('error')}")
    print(f"Description: {result.get('error_description')}")
