;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; MEC_v13+ EMOTIONAL GOAL MAP
;; Purpose: Derive symbolic goals from emotional states + ESIL function
;; Usage: 
;;  (EvaluationLink (PredicateNode "Goal") (ListLink (ConceptNode "User") (ConceptNode "SeekClosure")))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; 🧠 Shame → Goal: SeekClosure
(ImplicationLink
  (AndLink
    (EvaluationLink
      (PredicateNode "EmotionFunction")
      (ListLink
        (ConceptNode "User")
        (ConceptNode "shame")
        (ConceptNode "repair")
      )
    )
    (EvaluationLink
      (PredicateNode "EmotionPriority")
      (ListLink
        (ConceptNode "User")
        (ConceptNode "shame")
        (NumberNode "0.80")
      )
    )
  )
  (EvaluationLink
    (PredicateNode "Goal")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "SeekClosure")
    )
  )
)

;; 🧠 Guilt → Goal: RestoreTrust
(ImplicationLink
  (EvaluationLink
    (PredicateNode "EmotionFunction")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "guilt")
      (ConceptNode "repair")
    )
  )
  (EvaluationLink
    (PredicateNode "Goal")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "RestoreTrust")
    )
  )
)

;; 🧠 Panic → Goal: RegainControl
(ImplicationLink
  (EvaluationLink
    (PredicateNode "EmotionFunction")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "panic")
      (ConceptNode "protect")
    )
  )
  (EvaluationLink
    (PredicateNode "Goal")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "RegainControl")
    )
  )
)

;; 🧠 Hopelessness → Goal: ReigniteHope
(ImplicationLink
  (EvaluationLink
    (PredicateNode "EmotionFunction")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "hopelessness")
      (ConceptNode "motivate")
    )
  )
  (EvaluationLink
    (PredicateNode "Goal")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "ReigniteHope")
    )
  )
)

;; 🧠 Loneliness → Goal: Reconnect
(ImplicationLink
  (EvaluationLink
    (PredicateNode "EmotionFunction")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "loneliness")
      (ConceptNode "connect")
    )
  )
  (EvaluationLink
    (PredicateNode "Goal")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "Reconnect")
    )
  )
)

;; 🧠 Regret → Goal: ForgiveSelf
(ImplicationLink
  (EvaluationLink
    (PredicateNode "EmotionFunction")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "regret")
      (ConceptNode "repair")
    )
  )
  (EvaluationLink
    (PredicateNode "Goal")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "ForgiveSelf")
    )
  )
)
