# symbolic/schema/atomspace_esil_map.py

def build_atomspace_payload(esil_state: dict) -> str:
    """
    Convert ESIL cognitive state into AtomSpace-ready Scheme payload.
    Supports dynamic, open-ended emotions.
    """
    vector = esil_state.get("vector", {})
    flags = esil_state.get("flags", [])
    meta = esil_state.get("meta", {})

    # 🔥 Start building scheme code dynamically
    scheme_parts = [
        '(EvaluationLink',
        '  (PredicateNode "CurrentEmotionState")',
        '  (ListLink'
    ]

    for emotion, score in vector.items():
        normalized_score = min(max(score, 0.0), 1.0)  # Clamp to [0,1]
        part = f'    (EvaluationLink (PredicateNode "{emotion}") (FloatNode "{normalized_score}"))'
        scheme_parts.append(part)

    scheme_parts.append('  )')
    scheme_parts.append(')')

    # 🔥 Optional: Attach flags
    if flags:
        for flag in flags:
            scheme_parts.append(f'(ConceptNode "{flag}")')

    # 🔥 Optional: Attach meta information
    for key, value in meta.items():
        scheme_parts.append(f'(CommentNode "{key}: {value}")')

    scheme_payload = "\n".join(scheme_parts)

    return scheme_payload
