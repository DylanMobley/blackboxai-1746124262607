;; ============================================
;; MEC_v13+ Symbolic Engine Startup Ruleset
;; Purpose: Load all cognitive rulepacks needed at boot
;; ============================================

(include-file "rulepacks/emotion_goals.scm")
(include-file "rulepacks/metarules.scm")
(include-file "rulepacks/custom_symbolic_flags.scm") ;; optional
(include-file "rulepacks/persona_overrides.scm") ;; optional
