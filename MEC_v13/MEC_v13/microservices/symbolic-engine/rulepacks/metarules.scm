;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; MEC_v13+ META-RULEPACK
;; Purpose: Symbolic reasoning over emotional urgency + action planning
;; Contains:
;; 1. Escalation detection via EmotionPriority
;; 2. TriggerPersona suggestions
;; 3. Recovery flag logic
;; 4. Goal inference (e.g. SeekClosure)
;; 5. Scheduled symbolic planning (e.g. ReflectionTime)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; 🔍 1. Metarule: Detect high-priority emotions
(DefineLink
  (ConceptNode "DetectUrgentEmotion")

  (LambdaLink
    (VariableList
      (VariableNode "$user")
      (VariableNode "$emotion")
      (VariableNode "$priority")
    )

    (AndLink
      (EvaluationLink
        (PredicateNode "EmotionPriority")
        (ListLink
          (VariableNode "$user")
          (VariableNode "$emotion")
          (VariableNode "$priority")
        )
      )
      (GreaterThan
        (VariableNode "$priority")
        (NumberNode "0.85")
      )
    )
  )
)

;; 🔁 2. Rule: Trigger persona if emotion is urgent (shame → reflective_mentor)
(ImplicationLink
  (ExecutionOutputLink
    (ConceptNode "DetectUrgentEmotion")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "shame")
      (NumberNode "0.88")
    )
  )
  (EvaluationLink
    (PredicateNode "TriggerPersona")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "reflective_mentor")
    )
  )
)

;; 🛟 3. Rule: Panic escalates to RecoveryTriggered flag
(ImplicationLink
  (ExecutionOutputLink
    (ConceptNode "DetectUrgentEmotion")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "panic")
      (NumberNode "0.94")
    )
  )
  (EvaluationLink
    (PredicateNode "Flag")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "RecoveryTriggered")
    )
  )
)

;; 🎯 4. Rule: Urgent shame implies goal of closure
(ImplicationLink
  (ExecutionOutputLink
    (ConceptNode "DetectUrgentEmotion")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "shame")
      (NumberNode "0.88")
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

;; 📅 5. Rule: Urgent guilt + repair function → schedule reflection
(ImplicationLink
  (AndLink
    (ExecutionOutputLink
      (ConceptNode "DetectUrgentEmotion")
      (ListLink
        (ConceptNode "User")
        (ConceptNode "guilt")
        (NumberNode "0.92")
      )
    )
    (EvaluationLink
      (PredicateNode "EmotionFunction")
      (ListLink
        (ConceptNode "User")
        (ConceptNode "guilt")
        (ConceptNode "repair")
      )
    )
  )
  (EvaluationLink
    (PredicateNode "ScheduleIntervention")
    (ListLink
      (ConceptNode "User")
      (ConceptNode "ReflectionTime")
    )
  )
)
