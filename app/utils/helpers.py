def deduplicate_papers(papers):
    seen_titles = set()
    unique_papers = []

    for p in papers:
        title = (p.get("title") or "").lower().strip()

        if title not in seen_titles:
            seen_titles.add(title)
            unique_papers.append(p)

    return unique_papers
