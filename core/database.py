
import sqlite3
from pathlib import Path
from datetime import datetime

# Store the database in the project's data folder
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "grievances.db"


def get_connection():
    """Create a connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the complaints table if it does not exist."""

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_text TEXT NOT NULL,
            detected_language TEXT NOT NULL,
            translated_complaint TEXT NOT NULL,
            department TEXT NOT NULL,
            priority_score INTEGER NOT NULL,
            priority_reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted',
            submitted_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_complaint(complaint_text, analysis):
    """Save a complaint and its AI analysis."""

    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO complaints (
            complaint_text,
            detected_language,
            translated_complaint,
            department,
            priority_score,
            priority_reason,
            submitted_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        complaint_text,
        analysis["detected_language"],
        analysis["translated_complaint"],
        analysis["department"],
        analysis["priority_score"],
        analysis["priority_reason"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    complaint_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return complaint_id


def get_all_complaints():
    """Return all complaints, newest first."""

    connection = get_connection()

    complaints = connection.execute("""
        SELECT * FROM complaints
        ORDER BY submitted_at DESC
    """).fetchall()

    connection.close()

    return [dict(row) for row in complaints]


def get_complaint_by_id(complaint_id):
    """Find a complaint using its ID."""

    connection = get_connection()

    complaint = connection.execute("""
        SELECT * FROM complaints
        WHERE id = ?
    """, (complaint_id,)).fetchone()

    connection.close()

    return dict(complaint) if complaint else None


def update_complaint_status(complaint_id, new_status):
    """Update the status of a complaint."""

    allowed_statuses = [
        "Submitted",
        "Under Review",
        "In Progress",
        "Resolved",
        "Rejected"
    ]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid complaint status.")

    connection = get_connection()

    cursor = connection.execute("""
        UPDATE complaints
        SET status = ?
        WHERE id = ?
    """, (new_status, complaint_id))

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()

    return updated
