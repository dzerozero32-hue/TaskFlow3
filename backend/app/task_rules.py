MAX_TITLE_LENGTH = 200

class TaskRuleError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)

def validate_title(raw):
    if not isinstance(raw, str):
        raise TaskRuleError("title_invalid")
    cleaned = raw.strip()
    if not cleaned:
        raise TaskRuleError("title_empty")
    if len(cleaned) > MAX_TITLE_LENGTH:
        raise TaskRuleError("title_too_long")
    return cleaned

def check_stored_task(id, title, completed):
    if isinstance(id, bool) or not isinstance(id, int) or id < 1:
        raise TaskRuleError("record_invalid")
    try:
        validate_title(title)
    except TaskRuleError as exc:
        raise TaskRuleError("record_invalid") from exc
    if not isinstance(completed, bool):
        raise TaskRuleError("record_invalid")
