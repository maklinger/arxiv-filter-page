from datetime import datetime, timezone, timedelta

def matches_filter(entry, filter_cfg):
    # --- 1. Keyword/author matching ---
    for field, keywords in filter_cfg.get("keywords", {}).items():
        if field == "title":
            text = entry.title
        elif field == "abstract":
            text = entry.summary
        elif field == "authors":
            text = " ".join(a.name for a in entry.authors)
        else:
            continue
        for k in keywords:
            if k.lower() in text.lower():
                break  # match found, continue to date check
        else:
            continue  # no keyword matched in this field, try next field
        break  # one field matched, proceed
    else:
        return False  # no keywords matched

    # --- 2. Date filter (last N days) ---
    days = filter_cfg.get("days", None)
    if days is not None:
        # convert arxiv published string to datetime object
        # example: "2026-01-12T09:07:00Z"
        published_dt = datetime.fromisoformat(entry.published.replace("Z", "+00:00"))
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        if published_dt < cutoff:
            return False  # too old

    return True



