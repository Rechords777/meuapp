from src.main import db
from datetime import datetime

class EventLog(db.Model):
    __tablename__ = 'event_logs'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    url_accessed = db.Column(db.Text, nullable=True) # URL where the event occurred
    referer_url = db.Column(db.Text, nullable=True) # Referer
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    isp = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    channel = db.Column(db.String(100), nullable=True) # e.g., Google Ads, Organic, Direct
    device_type = db.Column(db.String(50), nullable=True) # e.g., mobile, desktop, tablet
    is_valid_click = db.Column(db.Boolean, default=True, nullable=False)
    invalid_reason = db.Column(db.String(255), nullable=True) # Reason if click is invalid
    raw_request_data = db.Column(db.Text, nullable=True) # Store raw JSON payload for audit

    def __repr__(self):
        return f'<EventLog {self.id} - {self.ip_address} at {self.timestamp}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'timestamp': self.timestamp.isoformat() + 'Z',
            'url_accessed': self.url_accessed,
            'referer_url': self.referer_url,
            'country': self.country,
            'city': self.city,
            'region': self.region,
            'isp': self.isp,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'channel': self.channel,
            'device_type': self.device_type,
            'is_valid_click': self.is_valid_click,
            'invalid_reason': self.invalid_reason
        }

# Placeholder for other models like User, InvalidClickRule, etc.
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return f'<User {self.username}>'

# class InvalidClickRule(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     parameter = db.Column(db.String(100), nullable=False) # e.g., ip_frequency, user_agent_blacklist
#     value = db.Column(db.String(255), nullable=False) # e.g., 5 (clicks), "crawler|bot"
#     time_window_seconds = db.Column(db.Integer, nullable=True) # For frequency rules
#     is_active = db.Column(db.Boolean, default=True)

#     def __repr__(self):
#         return f'<InvalidClickRule {self.name}>'

