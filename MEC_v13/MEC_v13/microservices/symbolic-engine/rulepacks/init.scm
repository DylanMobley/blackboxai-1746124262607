;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; MEC_v13+ SYMBOLIC ENGINE BOOTSTRAP
;; File: init.scm
;; Purpose: Load all rulepacks required for emotion cognition + reasoning
;; Usage:
;;   $ guile init.scm
;;   OR load dynamically: (include-file "init.scm")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; 💡 Load Emotion Metarules (priority detection, triggers, flags)
(include-file "rulepacks/metarules.scm")

;; 🎯 Load Emotion → Goal Inference Logic
(include-file "rulepacks/emotion_goals.scm")

;; 🚧 (Optional) Load Custom Modules
;; (include-file "rulepacks/custom_flags.scm")
;; (include-file "rulepacks/emotion_needs.scm")

(display "✅ MEC_v13+ symbolic rulepacks loaded successfully.\n")
