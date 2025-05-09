from flask import Blueprint, request, jsonify, send_file
from src.main import db
from src.models.event_log import EventLog
from sqlalchemy import and_
from datetime import datetime
import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

export_bp = Blueprint("export", __name__)

def _get_filtered_events(filters_dict):
    query = EventLog.query
    filters = []

    start_date_str = filters_dict.get("start_date")
    end_date_str = filters_dict.get("end_date")
    channel = filters_dict.get("channel")
    country = filters_dict.get("country")
    device_type = filters_dict.get("device_type")
    status = filters_dict.get("status")

    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str.replace("Z", ""))
            filters.append(EventLog.timestamp >= start_date)
        except ValueError:
            raise ValueError("Invalid start_date format. Use ISO format.")
    
    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str.replace("Z", ""))
            filters.append(EventLog.timestamp <= end_date)
        except ValueError:
            raise ValueError("Invalid end_date format. Use ISO format.")

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
            raise ValueError("Invalid status value. Use 'valid', 'invalid', or 'all'.")

    if filters:
        query = query.filter(and_(*filters))
    
    return query.order_by(EventLog.timestamp.desc()).all()

@export_bp.route("/export", methods=["GET"])
def export_data():
    export_format = request.args.get("format", "csv").lower()
    
    filter_params = {
        "start_date": request.args.get("start_date"),
        "end_date": request.args.get("end_date"),
        "channel": request.args.get("channel"),
        "country": request.args.get("country"),
        "device_type": request.args.get("device_type"),
        "status": request.args.get("status")
    }

    try:
        events = _get_filtered_events(filter_params)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error querying events for export (DB might be unavailable or not migrated): {e}")
        return jsonify({
            "warning": "Data export failed. Database may be unavailable or not yet migrated.",
            "details": str(e)
        }), 503

    if not events:
        return jsonify({"message": "No data to export for the given filters."}), 200

    if export_format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        header = [key for key in EventLog.to_dict(events[0]).keys() if key != 'id' and key != 'raw_request_data']
        writer.writerow(header)
        
        # Data rows
        for event in events:
            event_dict = event.to_dict()
            writer.writerow([event_dict.get(col) for col in header])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode("utf-8")),
            mimetype="text/csv",
            as_attachment=True,
            download_name="exported_events.csv"
        )

    elif export_format == "pdf":
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Event Log Export", styles["h1"]))
        story.append(Spacer(1, 12))

        # Define table header
        header = [key.replace("_", " ").title() for key in EventLog.to_dict(events[0]).keys() if key not in ['id', 'raw_request_data', 'latitude', 'longitude', 'isp', 'city', 'region']]
        data_keys = [key for key in EventLog.to_dict(events[0]).keys() if key not in ['id', 'raw_request_data', 'latitude', 'longitude', 'isp', 'city', 'region']]

        table_data = [header]
        for event in events:
            event_dict = event.to_dict()
            row = [str(event_dict.get(key, "")) for key in data_keys]
            table_data.append(row)
        
        if not table_data or len(table_data) <=1: # only header
             story.append(Paragraph("No data to display in PDF for the given filters.", styles["Normal"]))
        else:
            table = Table(table_data, hAlign='LEFT')
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)

        doc.build(story)
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="exported_events.pdf"
        )

    else:
        return jsonify({"error": "Invalid export format. Use 'csv' or 'pdf'."}), 400

