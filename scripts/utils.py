def matches_filter(entry, filter_cfg):
    for field, keywords in filter_cfg["keywords"].items():
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
                return True
    return False
