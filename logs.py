from flask import Blueprint, request, jsonify
from src.main import db
from src.models.event_log import EventLog
from sqlalchemy import and_
from datetime import datetime

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/logs", methods=["GET"])
def get_logs():
    # Pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    if per_page > 100: # Cap per_page to a reasonable limit
        per_page = 100

    # Filtering parameters (similar to metrics and export)
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    ip_address = request.args.get("ip_address")
    user_agent_contains = request.args.get("user_agent_contains")
    url_accessed_contains = request.args.get("url_accessed_contains")
    country = request.args.get("country")
    status = request.args.get("status") # 'valid', 'invalid', or 'all'
    invalid_reason_contains = request.args.get("invalid_reason_contains")

    query = EventLog.query
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

    if ip_address:
        filters.append(EventLog.ip_address == ip_address)
    if user_agent_contains:
        filters.append(EventLog.user_agent.ilike(f"%{user_agent_contains}%"))
    if url_accessed_contains:
        filters.append(EventLog.url_accessed.ilike(f"%{url_accessed_contains}%"))
    if country:
        filters.append(EventLog.country == country)
    if invalid_reason_contains:
        filters.append(EventLog.invalid_reason.ilike(f"%{invalid_reason_contains}%"))

    if status:
        if status.lower() == "valid":
            filters.append(EventLog.is_valid_click == True)
        elif status.lower() == "invalid":
            filters.append(EventLog.is_valid_click == False)
        elif status.lower() != "all":
            return jsonify({"error": "Invalid status value. Use 'valid', 'invalid', or 'all'."}), 400

    if filters:
        query = query.filter(and_(*filters))
    
    query = query.order_by(EventLog.timestamp.desc())

    try:
        paginated_logs = query.paginate(page=page, per_page=per_page, error_out=False)
        logs_data = [log.to_dict() for log in paginated_logs.items]
        
        return jsonify({
            "logs": logs_data,
            "total_logs": paginated_logs.total,
            "current_page": paginated_logs.page,
            "per_page": paginated_logs.per_page,
            "total_pages": paginated_logs.pages,
            "has_next": paginated_logs.has_next,
            "has_prev": paginated_logs.has_prev,
            "filters_applied": {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "ip_address": ip_address,
                "user_agent_contains": user_agent_contains,
                "url_accessed_contains": url_accessed_contains,
                "country": country,
                "status": status,
                "invalid_reason_contains": invalid_reason_contains
            }
        }), 200

    except Exception as e:
        print(f"Error querying logs (DB might be unavailable or not migrated): {e}")
        return jsonify({
            "warning": "Logs could not be retrieved. Database may be unavailable or not yet migrated.",
            "details": str(e),
            "logs": [],
            "total_logs": 0,
            "current_page": page,
            "per_page": per_page,
            "total_pages": 0,
             "filters_applied": {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "ip_address": ip_address,
                "user_agent_contains": user_agent_contains,
                "url_accessed_contains": url_accessed_contains,
                "country": country,
                "status": status,
                "invalid_reason_contains": invalid_reason_contains
            }
        }), 503

