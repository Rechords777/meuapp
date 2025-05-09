from flask import Blueprint, request, jsonify
from src.main import db # Assuming db is initialized in main
from src.models.event_log import EventLog
from sqlalchemy import func, and_
from datetime import datetime, timedelta

metrics_bp = Blueprint("metrics", __name__)

@metrics_bp.route("/metrics", methods=["GET"])
def get_metrics():
    # Query parameters for filtering
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    channel = request.args.get("channel")
    country = request.args.get("country")
    device_type = request.args.get("device_type")
    status = request.args.get("status") # 'valid', 'invalid', or 'all'

    query = db.session.query(
        func.count(EventLog.id).label("total_events"),
        func.sum(db.case((EventLog.is_valid_click == True, 1), else_=0)).label("valid_clicks"),
        func.sum(db.case((EventLog.is_valid_click == False, 1), else_=0)).label("invalid_clicks"),
        func.count(func.distinct(EventLog.ip_address)).label("unique_ips")
    )

    filters = []
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str.replace("Z", ""))
            filters.append(EventLog.timestamp >= start_date)
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use ISO format."}), 400
    
    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str.replace("Z", ""))
            filters.append(EventLog.timestamp <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use ISO format."}), 400

    if channel:
        filters.append(EventLog.channel == channel)
    if country:
        filters.append(EventLog.country == country)
    if device_type:
        filters.append(EventLog.device_type == device_type)
    
    if status:
        if status.lower() == "valid":
            filters.append(EventLog.is_valid_click == True)
        elif status.lower() == "invalid":
            filters.append(EventLog.is_valid_click == False)
        elif status.lower() != "all":
            return jsonify({"error": "Invalid status value. Use 'valid', 'invalid', or 'all'."}), 400

    if filters:
        query = query.filter(and_(*filters))

    # Execute the query
    # Note: This will fail if the database is not set up and migrations are not run.
    # For now, we'll proceed with the logic, assuming the DB will be available later.
    try:
        result = query.one()
        metrics_data = {
            "total_events": result.total_events or 0,
            "valid_clicks": result.valid_clicks or 0,
            "invalid_clicks": result.invalid_clicks or 0,
            "unique_ips": result.unique_ips or 0,
            "filters_applied": {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "channel": channel,
                "country": country,
                "device_type": device_type,
                "status": status
            }
        }
        return jsonify(metrics_data), 200
    except Exception as e:
        # This will catch errors if the DB is not available or table doesn't exist
        print(f"Error querying metrics (DB might be unavailable or not migrated): {e}")
        return jsonify({
            "warning": "Metrics could not be retrieved. Database may be unavailable or not yet migrated.",
            "details": str(e),
            "total_events": 0, # Return dummy data or an explicit error
            "valid_clicks": 0,
            "invalid_clicks": 0,
            "unique_ips": 0,
             "filters_applied": {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "channel": channel,
                "country": country,
                "device_type": device_type,
                "status": status
            }
        }), 503 # Service Unavailable or appropriate error

# Placeholder for more detailed metrics, e.g., time series data
# @metrics_bp.route("/metrics/timeseries", methods=["GET"])
# def get_metrics_timeseries():
#     # ... logic to return data puntos for charts ...
#     return jsonify({"message": "Timeseries metrics endpoint placeholder"}), 200

