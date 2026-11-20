"""Validation of one registration line. Uses string methods only (no regular expressions)."""

class InvalidRegistration(Exception):
    """A line cannot be used. Raised by parse_registration(); handled in processor.process_file()."""

def is_valid_email(email):
    if not email or " " in email or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain or ".." in email:
        return False
    if domain.startswith(".") or domain.endswith(".") or "." not in domain:
        return False
    return len(domain.rsplit(".", 1)[1]) >= 2           # top-level part such as 'com' or 'in'

def parse_registration(line):
    """'192311001,Arun Kumar,CSE,arun@mail.com,Dance;Quiz' -> (reg, name, dept, email, [events])"""
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        raise InvalidRegistration(f"expected 5 fields, found {len(parts)}")
    reg, name, dept, email, events_text = parts
    if not (reg.isdigit() and len(reg) == 9):
        raise InvalidRegistration(f"register number {reg!r} is not 9 digits")
    if not name:
        raise InvalidRegistration("empty name")
    if not dept:
        raise InvalidRegistration("empty department")
    if not is_valid_email(email):
        raise InvalidRegistration(f"invalid e-mail {email!r}")
    events = []
    for e in events_text.split(";"):
        e = e.strip().title()
        if e and e not in events:
            events.append(e)
    if not events:
        raise InvalidRegistration("no event chosen")
    return reg, name, dept.upper(), email.lower(), events
