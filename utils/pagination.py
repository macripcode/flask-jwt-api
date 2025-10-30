def apply_ra_pagination(query, args):
    start = int(args.get("_start", 0))
    end = int(args.get("_end", 10))
    total = query.count()
    items = query.offset(start).limit(max(end - start, 0)).all()
    return items, total
