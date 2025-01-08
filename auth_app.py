import os
import msal
import requests
from datetime import datetime, timedelta
import pytz
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GraphConfig:
    client_id: str
    tenant_id: str
    scopes: List[str]
    
    @classmethod
    def from_env(cls) -> 'GraphConfig':
        client_id = os.environ.get("CLIENT_ID")
        tenant_id = os.environ.get("TENANT_ID")
        
        if not client_id or not tenant_id:
            raise ValueError("CLIENT_ID and TENANT_ID environment variables must be set.")
            
        return cls(
            client_id=client_id,
            tenant_id=tenant_id,
            scopes=["User.Read", "Calendars.ReadWrite"]
        )

class GraphClient:
    """A client for interacting with Microsoft Graph API.
    This class provides functionality to authenticate users and interact with Microsoft Graph API
    to access user profiles and manage calendar events.
    Attributes:
        config (GraphConfig): Configuration object containing client_id, tenant_id and scopes.
        app (msal.PublicClientApplication): MSAL application instance for authentication.
        access_token (Optional[str]): The OAuth access token for API requests.
    Example:
        ```
        config = GraphConfig(client_id="xxx", tenant_id="xxx", scopes=["User.Read"])
        client = GraphClient(config)
        if client.authenticate():
            profile = client.get_user_profile()
        ```
    """
    def __init__(self, config: GraphConfig):
        self.config = config
        self.app = msal.PublicClientApplication(
            client_id=config.client_id,
            authority=f"https://login.microsoftonline.com/{config.tenant_id}"
        )
        self.access_token: Optional[str] = None
        
    def authenticate(self) -> bool:
        try:
            flow = self.app.initiate_device_flow(scopes=self.config.scopes)
            
            if "user_code" not in flow:
                raise ValueError(f"Failed to create device flow. Error: {flow}")
                
            print(flow["message"])
            result = self.app.acquire_token_by_device_flow(flow)
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                return True
            else:
                logger.error(f"Authentication failed: {result.get('error')} - {result.get('error_description')}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
            
    def get_user_profile(self) -> Optional[Dict]:
        if not self.access_token:
            return None
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error fetching user profile: {response.text}")
            return None
            
    def get_calendar_events(self, limit: int = 5) -> List[Dict]:
        if not self.access_token:
            return []
            
        headers = {"Authorization": f"Bearer {self.access_token}"}
        events_url = (
            "https://graph.microsoft.com/v1.0/me/events"
            f"?$select=subject,organizer,start,end"
            f"&$top={limit}"
            "&$orderby=start/dateTime ASC"
        )
        
        response = requests.get(events_url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get("value", [])
        else:
            logger.error(f"Error fetching events: {response.text}")
            return []
            
    def create_calendar_event(self, subject: str, duration_minutes: int = 30) -> Optional[Dict]:
        if not self.access_token:
            return None
            
        try:
            # Use UTC for consistency
            start_time = datetime.now(pytz.UTC) + timedelta(minutes=5)
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            event = {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": "I've heard there's a good book from Packt for that."
                },
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "UTC"
                },
                "location": {
                    "displayName": "Wherever you are"
                }
            }
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(
                "https://graph.microsoft.com/v1.0/me/events",
                headers=headers,
                json=event
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                logger.error(f"Error creating event: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating calendar event: {str(e)}")
            return None

def main():
    try:
        config = GraphConfig.from_env()
        client = GraphClient(config)
        
        if not client.authenticate():
            return
            
        # Get user profile
        if profile := client.get_user_profile():
            print(f"\nWelcome, {profile.get('displayName', 'Unknown')}!\n")
            
        # Get calendar events
        if events := client.get_calendar_events():
            print("Your upcoming calendar events:")
            for idx, event in enumerate(events, start=1):
                # Skip duplicate line printing by combining into a single formatted string
                subject = event.get('subject', 'No subject')
                organizer = event['organizer']['emailAddress'].get('name', 'Unknown')
                start_time = event['start'].get('dateTime', '').split('.')[0]  # Remove milliseconds
                end_time = event['end'].get('dateTime', '').split('.')[0]      # Remove milliseconds
                
                # Format the event details
                event_details = (
                    f"{idx}. Subject: {subject}\n"
                    f"   Organizer: {organizer}\n"
                    f"   Start: {start_time}\n"
                    f"   End:   {end_time}\n"
                )
                print(event_details)
        else:
            print("No upcoming events found.")
            
        # Create new event
        if created_event := client.create_calendar_event("Study for the AZ-204 exam"):
            # Format the created event details in a single block
            created_event_details = (
                "Your meeting was created with the following details:\n"
                f"Subject: {created_event['subject']}\n"
                f"Location: {created_event['location']['displayName']}\n"
                f"Start: {created_event['start']['dateTime'].split('.')[0]}\n"
                f"End: {created_event['end']['dateTime'].split('.')[0]}\n"
            )
            print(created_event_details)
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()
