from flask import Blueprint, request, jsonify
from src.main import db, socketio # Assuming db and socketio are initialized in main
from src.models.event_log import EventLog # Import the EventLog model
from src.services.click_validator import ClickValidator # Import the ClickValidator
from datetime import datetime
import json
import os
import requests # For ipapi.co

events_bp = Blueprint("events", __name__)

# --- Helper function to get Geolocation Data ---
def get_geolocation_data(ip_address):
    if not ip_address or ip_address == "127.0.0.1" or ip_address == "::1": # Avoid local/invalid IPs
        return {
            "country": "Local",
            "city": "Local",
            "region": "Local",
            "isp": "Local Network",
            "latitude": None,
            "longitude": None
        }
    try:
        # IPAPI_CO_KEY is optional for ipapi.co, but good to have if you have a key for higher limits
        # api_key = os.getenv("IPAPI_CO_KEY") 
        # url = f"https://ipapi.co/{ip_address}/json/?key={api_key}" if api_key else f"https://ipapi.co/{ip_address}/json/"
        url = f"https://ipapi.co/{ip_address}/json/"
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        return {
            "country": data.get("country_name"),
            "city": data.get("city"),
            "region": data.get("region"),
            "isp": data.get("org"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching geolocation for {ip_address}: {e}")
        return {
            "country": "Unknown",
            "city": "Unknown",
            "region": "Unknown",
            "isp": "Unknown",
            "latitude": None,
            "longitude": None
        }

@events_bp.route("/event", methods=["POST"])
def record_event():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Extract common fields
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent")
    url_accessed = data.get("url_accessed", request.referrer) # or data.get("page_url")
    referer_url = data.get("referer_url", request.referrer)
    channel = data.get("channel")
    device_type = data.get("device_type") # Client should ideally send this
    campaign_country_target = data.get("campaign_country_target") # Optional: for geo-validation

    # Get Geolocation
    geo_data = get_geolocation_data(ip_address)

    # Prepare event data for validator and logging
    current_event_data_for_validator = {
        "url_accessed": url_accessed,
        "referer_url": referer_url,
        "channel": channel,
        "device_type": device_type,
        "country": geo_data.get("country") # Pass fetched country to validator if needed
    }

    # Validate Click using the ClickValidator service
    validator = ClickValidator(event_data=current_event_data_for_validator, ip_address=ip_address, user_agent=user_agent)
    is_valid, reasons_list = validator.validate(campaign_country=campaign_country_target)
    reason_string = ", ".join(reasons_list) if reasons_list else None

    # Create EventLog entry
    new_event = EventLog(
        ip_address=ip_address,
        user_agent=user_agent,
        timestamp=datetime.utcnow(),
        url_accessed=url_accessed,
        referer_url=referer_url,
        country=geo_data.get("country"),
        city=geo_data.get("city"),
        region=geo_data.get("region"),
        isp=geo_data.get("isp"),
        latitude=geo_data.get("latitude"),
        longitude=geo_data.get("longitude"),
        channel=channel,
        device_type=device_type,
        is_valid_click=is_valid,
        invalid_reason=reason_string,
        raw_request_data=json.dumps(data) # Store the original payload
    )

    try:
        db.session.add(new_event)
        db.session.commit()

        # Emit event via WebSocket
        event_data_for_socket = new_event.to_dict()
        socketio.emit("new_event", event_data_for_socket, namespace="/tracking")

        # TODO: If click is invalid and meets certain criteria, trigger Google Ads IP exclusion
        # if not is_valid and ip_address: # and other conditions
        #     from src.services.google_ads_manager import add_ip_to_exclusion_list
        #     campaign_id = data.get("google_campaign_id") # Assuming client sends this
        #     if campaign_id:
        #        add_ip_to_exclusion_list(ip_address, campaign_id)

        return jsonify({"message": "Event recorded successfully", "event_id": new_event.id, "is_valid": is_valid, "reason": reason_string}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error saving event: {e}") # Log this properly
        return jsonify({"error": "Failed to record event", "details": str(e)}), 500

@socketio.on("connect", namespace="/tracking")
def handle_tracking_connect():
    print("Client connected to /tracking namespace")

@socketio.on("disconnect", namespace="/tracking")
def handle_tracking_disconnect():
    print("Client disconnected from /tracking namespace")
