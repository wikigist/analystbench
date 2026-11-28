import re


def extract_citations(answer):
    return re.findall(r"\[[^:\[\]\n]+:\d+\]", answer)

def validate_citations(answer, retrieved_records):
    valid_labels = set()

    for record in retrieved_records:
        label = f"[{record['source']}:{record['chunk_id']}]"
        valid_labels.add(label)

    citations = extract_citations(answer)

    valid_citations = []
    invalid_citations = []

    for citation in citations:
        if citation in valid_labels:
            valid_citations.append(citation)
        else:
            invalid_citations.append(citation)

    return {
        "valid_citations": valid_citations,
        "invalid_citations": invalid_citations
    }