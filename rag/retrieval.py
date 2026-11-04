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