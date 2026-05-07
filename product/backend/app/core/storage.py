"""Stockage SQLAlchemy pour heartbeats, événements, alertes et logs d'audit."""

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.alert import Alert
from app.models.audit import AuditLog
from app.models.event import Event
from app.models.heartbeat import Heartbeat
from app.models.user import User


def add_heartbeat(db: Session, payload: dict[str, Any]) -> Heartbeat:
    heartbeat = Heartbeat(
        endpoint_id=payload["endpoint_id"],
        timestamp=payload["timestamp"],
        status=payload["status"],
    )
    db.add(heartbeat)
    db.commit()
    db.refresh(heartbeat)
    return heartbeat


def add_event(db: Session, payload: dict[str, Any]) -> Event:
    event = Event(
        endpoint_id=payload["endpoint_id"],
        timestamp=payload["timestamp"],
        event_type=payload["event_type"],
        severity=payload["severity"],
        details=payload.get("details", {}),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_heartbeats(db: Session) -> list[Heartbeat]:
    return db.query(Heartbeat).all()


def get_events(db: Session) -> list[Event]:
    return db.query(Event).all()


def update_alert_status(db: Session, alert_id: int, new_status: str) -> Alert | None:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert is None:
        return None
    alert.status = new_status
    db.commit()
    db.refresh(alert)
    return alert


def add_alert(db: Session, alert_data: dict[str, Any]) -> Alert:
    alert = Alert(
        event_id=alert_data["event_id"],
        rule_name=alert_data["rule_name"],
        severity=alert_data["severity"],
        timestamp=alert_data["timestamp"],
        status=alert_data.get("status", "open"),
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_alerts(db: Session) -> list[Alert]:
    return db.query(Alert).all()


def add_audit_log(db: Session, action: str, user_email: str | None, details: str) -> AuditLog:
    log = AuditLog(
        timestamp=datetime.utcnow(),
        action=action,
        user_email=user_email,
        details=details,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_audit_logs(db: Session) -> list[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str, role: str = "analyst") -> User:
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def check_and_create_correlation(db: Session, event: Event) -> None:
    from datetime import timedelta
    from app.models.correlation import CorrelationGroup
    source_ip = event.details.get("source_ip") if isinstance(event.details, dict) else None
    if not source_ip:
        return
    window_minutes = 10
    cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
    recent = db.query(Event).filter(
        Event.timestamp >= cutoff,
        Event.id != event.id,
    ).all()
    same_source = [e for e in recent if isinstance(e.details, dict) and e.details.get("source_ip") == source_ip]
    same_source.append(event)
    if len(same_source) >= 3:
        existing = db.query(CorrelationGroup).filter(
            CorrelationGroup.source_ip == source_ip,
            CorrelationGroup.window_end >= cutoff,
        ).first()
        if existing:
            existing.event_count = len(same_source)
            existing.window_end = event.timestamp
        else:
            group = CorrelationGroup(
                correlation_type="ip_repetition",
                source_ip=source_ip,
                target_ip=event.details.get("target_ip"),
                event_type=event.event_type,
                window_start=min(e.timestamp for e in same_source),
                window_end=max(e.timestamp for e in same_source),
                event_count=len(same_source),
            )
            db.add(group)
        db.commit()


def seed_default_users(db: Session) -> None:
    if get_user_by_email(db, "admin@wazash.io") is None:
        create_user(db, "admin@wazash.io", "dummy123", role="admin")
    if get_user_by_email(db, "user@wazash.io") is None:
        create_user(db, "user@wazash.io", "test456", role="analyst")
