# /home/ubuntu/traffic_tracker_backend/src/services/click_validator.py
import os
from datetime import datetime, timedelta
from src.main import db # Assuming db is initialized in main
from src.models.event_log import EventLog # To query for IP frequency

# --- Configuration for Click Validation (can be moved to .env or a config file) ---
CLICK_FREQ_LIMIT = int(os.getenv("CLICK_FREQ_LIMIT", "5"))
CLICK_FREQ_WINDOW_SECONDS = int(os.getenv("CLICK_FREQ_WINDOW_SECONDS", "10"))

# List of suspicious User Agent substrings (can be expanded and managed elsewhere)
# Sourced from common bot lists and pasted_content.txt suggestions
SUSPICIOUS_USER_AGENT_SUBSTRINGS = [
    "bot", "crawler", "spider", "headless", "phantomjs", "python-requests", 
    "curl", "wget", "libwww-perl", "go-http-client", "java/", "apache-httpclient",
    "node-fetch", "scrapy", "selenium", "puppeteer", "playwright", "dataprovider",
    "googlebot", "bingbot", "slurp", "duckduckbot", "baiduspider", "yandexbot",
    "sogou", "exabot", "facebot", "ia_archiver"
]

EMPTY_OR_GENERIC_USER_AGENTS = [
    "-", "", None, "mozilla/5.0", "generic browser"
]

class ClickValidator:
    def __init__(self, event_data, ip_address, user_agent):
        """
        Initializes the ClickValidator.
        :param event_data: Dictionary containing data from the incoming request (e.g., URL, referer).
        :param ip_address: The IP address of the request.
        :param user_agent: The User-Agent string of the request.
        """
        self.event_data = event_data
        self.ip_address = ip_address
        self.user_agent = user_agent.lower() if user_agent else ""
        self.reasons = [] # To store reasons for invalidation

    def is_suspicious_user_agent(self):
        """Checks if the User-Agent is suspicious."""
        if not self.user_agent or self.user_agent in EMPTY_OR_GENERIC_USER_AGENTS:
            self.reasons.append("Empty or Generic User Agent")
            return True
        
        for substring in SUSPICIOUS_USER_AGENT_SUBSTRINGS:
            if substring in self.user_agent:
                self.reasons.append(f"Suspicious User Agent: contains \'{substring}\'")
                return True
        return False

    def is_high_frequency_ip(self):
        """
        Checks for high-frequency clicks from the same IP address.
        This method requires database access and assumes EventLog model is available.
        """
        if not self.ip_address or self.ip_address in ["127.0.0.1", "::1"]:
            return False # Do not check local IPs for frequency

        try:
            time_window_start = datetime.utcnow() - timedelta(seconds=CLICK_FREQ_WINDOW_SECONDS)
            
            # This query will only work if the database is up and migrated.
            recent_clicks_count = EventLog.query.filter(
                EventLog.ip_address == self.ip_address,
                EventLog.timestamp >= time_window_start
            ).count()
            
            if recent_clicks_count >= CLICK_FREQ_LIMIT:
                self.reasons.append(f"High IP Frequency: {recent_clicks_count + 1} clicks in {CLICK_FREQ_WINDOW_SECONDS}s")
                return True
        except Exception as e:
            # Log this error. For now, we assume it means DB is not ready.
            print(f"DB_WARN: Could not check IP frequency for {self.ip_address} (DB might be unavailable or not migrated): {e}")
            # Optionally, add a reason indicating inability to check, or simply pass
            # self.reasons.append("IP Frequency Check Skipped: DB Unavailable")
            return False # Fail open if DB check fails, or decide on a stricter policy
        return False

    def is_inconsistent_geolocation(self, campaign_country=None):
        """
        Checks if the click's geolocation is inconsistent with campaign targeting (if provided).
        :param campaign_country: The expected country for the campaign (e.g., 'BR').
        """
        # This requires geo_data to be part of self.event_data or passed in
        click_country = self.event_data.get("country") 
        
        if campaign_country and click_country:
            if click_country.upper() != campaign_country.upper() and click_country not in ["Unknown", "Local"]:
                self.reasons.append(f"Geolocation Mismatch: Click from {click_country}, expected {campaign_country}")
                return True
        return False

    def validate(self, campaign_country=None):
        """
        Runs all validation checks.
        :param campaign_country: (Optional) Expected country for campaign targeting.
        :return: Tuple (is_valid: bool, reasons: list[str])
        """
        # Run checks
        self.is_suspicious_user_agent() # Appends to self.reasons if true
        self.is_high_frequency_ip()     # Appends to self.reasons if true
        # self.is_inconsistent_geolocation(campaign_country) # Example, needs geo_data in event_data

        if self.reasons:
            return False, self.reasons
        return True, []

# Example of how this might be integrated into the events.py route:
# from src.services.click_validator import ClickValidator
# ... inside /event route ...
# validator = ClickValidator(event_data=data, ip_address=ip_address, user_agent=user_agent)
# is_valid, reasons = validator.validate(campaign_country="BR") # Assuming campaign target is Brazil
# new_event.is_valid_click = is_valid
# new_event.invalid_reason = ", ".join(reasons) if reasons else None

