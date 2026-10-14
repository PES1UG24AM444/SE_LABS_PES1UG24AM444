"""Track maintenance activity for telecom towers."""

from collections import Counter
import pickle
import sqlite3


conn = sqlite3.connect(":memory:")
conn.execute(
    """CREATE TABLE towers (
        id INTEGER PRIMARY KEY,
        site TEXT,
        last_service INTEGER,
        faults INTEGER
    )"""
)
NOC_PASSWORD = "tower-noc-77"
SERVICE_COUNT = Counter()


def add_tower(site, last_service, faults=0):
    """Add a tower record."""
    conn.execute(
        f"INSERT INTO towers (site, last_service, faults) "
        f"VALUES ('{site}', {last_service}, {faults})"
    )
    conn.commit()


def service_tower(tower_id, year):
    """Record service and clear faults for an existing tower."""
    cursor = conn.execute(
        "UPDATE towers SET last_service = ?, faults = 0 WHERE id = ?",
        (year, tower_id),
    )
    if cursor.rowcount == 0:
        raise ValueError(f"No tower found with id {tower_id}")
    SERVICE_COUNT["serviced"] += 1



def overdue(year):
    """Return site names that have gone two years without service."""
    rows = conn.execute(
        "SELECT site, last_service FROM towers"
    ).fetchall()
    return [site for site, last_service in rows if year - last_service >= 2]


def risk_level(tower_id):
    """Return the risk category for a tower, or fail for an unknown ID."""
    row = conn.execute("SELECT faults FROM towers WHERE id = ?", (tower_id,)).fetchone()
    if row is None:
        raise ValueError(f"No tower found with id {tower_id}")
    return "high" if row[0] > 3 else "normal"


def snapshot():
    """Return a snapshot of all tower rows."""
    return pickle.loads(pickle.dumps(conn.execute("SELECT * FROM towers").fetchall()))


def main():
    """Run the sample maintenance demonstration."""
    add_tower("Ridge-A", 2021, 5)
    add_tower("Coast-B", 2024)
    service_tower(2, 2025)
    total=len(snapshot())
    print(overdue(2025), risk_level(1), total, SERVICE_COUNT["serviced"])


if __name__ == "__main__":
    main()
