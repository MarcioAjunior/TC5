def mix_recommendations(popular, recent, limit):
    mixed = []
    for pop, rec in zip(popular, recent):
        if pop is not None:
            mixed.append(pop)
        if rec is not None:
            mixed.append(rec)
        if len(mixed) >= limit:
            break 
    
    if len(mixed) < limit:
        mixed.extend(popular[len(mixed):limit])
    if len(mixed) < limit:
        mixed.extend(recent[len(mixed):limit])

    return mixed[:limit]

