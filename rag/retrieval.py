def retrieve_by_keyword(chunks, keyword):
    matches = []

    for chunk in chunks:
        if keyword.lower() in chunk.lower():
            matches.append(chunk)

    return matches


def get_next_chunk(chunks, matching_index):
    next_index = matching_index + 1

    if next_index < len(chunks):
        return chunks[next_index]

    return None


def retrieve_records_by_keyword(records, keyword):
    matches = []

    for record in records:
        if keyword.lower() in record["text"].lower():
            matches.append(record)

    return matches