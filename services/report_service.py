import csv
from io import BytesIO, StringIO
from fpdf import FPDF
from sqlalchemy.orm import Session

from models.event import Event
from models.alert import Alert


def export_report_csv(db: Session) -> str:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Timestamp",
        "Source IP",
        "Destination IP",
        "Event Type",
        "Severity",
        "Risk Label",
        "Bytes In",
        "Bytes Out",
        "Anomaly",
        "Alert Title",
        "Alert Risk Score",
    ])

    rows = (
        db.query(Event, Alert)
        .outerjoin(Alert, Event.id == Alert.event_id)
        .order_by(Event.timestamp.desc())
        .all()
    )

    for event, alert in rows:
        writer.writerow([
            event.timestamp.isoformat(),
            event.source_ip,
            event.destination_ip,
            event.event_type,
            event.severity,
            event.risk_label,
            event.bytes_in,
            event.bytes_out,
            event.is_anomaly,
            alert.title if alert else "",
            alert.risk_score if alert else "",
        ])
    return output.getvalue()


def export_report_pdf(db: Session) -> bytes:
    rows = (
        db.query(Event, Alert)
        .outerjoin(Alert, Event.id == Alert.event_id)
        .order_by(Event.timestamp.desc())
        .limit(40)
        .all()
    )

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.set_fill_color(18, 10, 30)
    pdf.cell(0, 14, "AI Threat Detector Report", ln=True, align="C", fill=True)
    pdf.ln(4)
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(235, 235, 235)

    pdf.set_fill_color(32, 18, 56)
    pdf.cell(0, 8, "Generated threat and alert summary", ln=True, fill=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(50, 8, "Timestamp", border=1, fill=True)
    pdf.cell(40, 8, "Source IP", border=1, fill=True)
    pdf.cell(40, 8, "Destination IP", border=1, fill=True)
    pdf.cell(30, 8, "Type", border=1, fill=True)
    pdf.cell(18, 8, "Severity", border=1, fill=True)
    pdf.cell(30, 8, "Risk", border=1, fill=True)
    pdf.cell(50, 8, "Alert", border=1, fill=True)
    pdf.ln()
    pdf.set_font("Helvetica", size=9)

    for event, alert in rows:
        pdf.cell(50, 8, event.timestamp.strftime("%Y-%m-%d %H:%M"), border=1)
        pdf.cell(40, 8, event.source_ip, border=1)
        pdf.cell(40, 8, event.destination_ip, border=1)
        pdf.cell(30, 8, event.event_type, border=1)
        pdf.cell(18, 8, str(event.severity), border=1)
        pdf.cell(30, 8, event.risk_label, border=1)
        pdf.cell(50, 8, alert.title if alert else "None", border=1)
        pdf.ln()

    blob = BytesIO()
    blob.write(pdf.output(dest="S").encode("latin-1"))
    return blob.getvalue()
