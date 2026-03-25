from fastapi import HTTPException
from psycopg2 import Error

from app.db_errors import raise_db_http_error
from database.database import fetch_all, fetch_one


def create_research_evaluation(db, payload):
    paper = fetch_one(db, "SELECT id FROM research_papers WHERE id = %s", (str(payload.paper_id),))
    if not paper:
        raise HTTPException(status_code=400, detail="Paper not found")

    try:
        row = fetch_one(
            db,
            """
            INSERT INTO research_evaluations (
                paper_id, status, document_links, authorship_from_link, journal_conference_info
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, paper_id, status, document_links, authorship_from_link,
                      journal_conference_info, created_at, updated_at
            """,
            (
                str(payload.paper_id),
                payload.status,
                payload.document_links,
                payload.authorship_from_link,
                payload.journal_conference_info,
            ),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc, conflict_detail="Evaluation already exists for this paper")


def list_research_evaluations(db, paper_id: str | None, status_value: str | None, search: str | None, skip: int, limit: int):
    query = """
        SELECT id, paper_id, status, document_links, authorship_from_link,
               journal_conference_info, created_at, updated_at
        FROM research_evaluations
        WHERE (%s IS NULL OR paper_id = %s)
          AND (%s IS NULL OR status = %s)
          AND (%s IS NULL OR authorship_from_link ILIKE %s)
        ORDER BY created_at DESC
        OFFSET %s LIMIT %s
    """
    params = (
        paper_id,
        paper_id,
        status_value,
        status_value,
        search,
        f"%{search}%" if search else None,
        skip,
        limit,
    )
    return fetch_all(db, query, params)


def get_research_evaluation(db, evaluation_id: str):
    row = fetch_one(
        db,
        """
        SELECT id, paper_id, status, document_links, authorship_from_link,
               journal_conference_info, created_at, updated_at
        FROM research_evaluations
        WHERE id = %s
        """,
        (evaluation_id,),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Research evaluation not found")
    return row


def update_research_evaluation(db, evaluation_id: str, payload):
    current = get_research_evaluation(db, evaluation_id)
    update_data = payload.model_dump(exclude_unset=True)

    next_paper_id = str(update_data.get("paper_id")) if update_data.get("paper_id") else str(current["paper_id"])
    next_status = update_data.get("status", current["status"])
    next_document_links = update_data.get("document_links", current["document_links"])
    next_authorship = update_data.get("authorship_from_link", current["authorship_from_link"])
    next_journal_info = update_data.get("journal_conference_info", current["journal_conference_info"])

    try:
        row = fetch_one(
            db,
            """
            UPDATE research_evaluations
            SET paper_id = %s,
                status = %s,
                document_links = %s,
                authorship_from_link = %s,
                journal_conference_info = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, paper_id, status, document_links, authorship_from_link,
                      journal_conference_info, created_at, updated_at
            """,
            (next_paper_id, next_status, next_document_links, next_authorship, next_journal_info, evaluation_id),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc, conflict_detail="Evaluation already exists for this paper")


def delete_research_evaluation(db, evaluation_id: str):
    try:
        deleted = fetch_one(db, "DELETE FROM research_evaluations WHERE id = %s RETURNING id", (evaluation_id,))
        if not deleted:
            raise HTTPException(status_code=404, detail="Research evaluation not found")
        db.commit()
    except Error as exc:
        raise_db_http_error(db, exc)
