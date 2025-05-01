def build_priority_links(emotion: str, needs: list, urgency: float) -> list:
    """
    Builds Atomese blocks to represent urgency/priority of emotion and needs.
    """
    atomese = []

    # Emotion priority
    atomese.append(f"""
    (EvaluationLink
        (PredicateNode "EmotionPriority")
        (ListLink
            (ConceptNode "User")
            (ConceptNode "{emotion}")
            (NumberNode "{urgency:.2f}")
        )
    )
    """)

    # Need priorities (distributed)
    if needs:
        weight = urgency / len(needs)
        for need in needs:
            atomese.append(f"""
            (EvaluationLink
                (PredicateNode "NeedPriority")
                (ListLink
                    (ConceptNode "User")
                    (ConceptNode "{need}")
                    (NumberNode "{weight:.2f}")
                )
            )
            """)

    return atomese
