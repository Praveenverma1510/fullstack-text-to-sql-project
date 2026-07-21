import re
import sqlparse

BLOCKED = {
    "insert", "update", "delete", "drop", "alter",
    "truncate", "create", "grant", "revoke", "copy",
    "call", "do", "merge"
}


def validate_read_only_sql(sql: str) -> tuple[bool, str | None]:
    cleaned = sql.strip().strip(";")
    if not cleaned:
        return False, "Query is empty"
    if ";" in cleaned:
        return False, "Multiple statements are not allowed"
    parsed = sqlparse.parse(cleaned)
    if not parsed:
        return False, "Invalid SQL"
    lowered = re.sub(r"\s+", " ", cleaned.lower())
    tokens = {t.value.lower() for t in parsed[0].flatten() if not t.is_whitespace}
    for keyword in BLOCKED:
        if keyword in tokens:
            return False, f"Blocked keyword detected: {keyword.upper()}"
    if not (lowered.startswith("select") or lowered.startswith("with")):
        return False, "Only SELECT or read-only WITH queries are allowed"
    if re.search(r"\bwith\b.*\b(insert|update|delete)\b", lowered):
        return False, "Writable CTEs are not allowed"
    return True, None
