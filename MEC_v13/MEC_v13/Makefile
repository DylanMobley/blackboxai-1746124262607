# Root Makefile Wrapper

.DEFAULT_GOAL := help

.PHONY: help dev prod env-check ensure-env

help:
	@echo "\033[1;32mAvailable targets:\033[0m"
	@echo "  dev         - Run development commands (Makefile.dev)"
	@echo "  prod        - Run production commands (Makefile.prod)"
	@echo "  env-check   - Ensure .env is available (generate from template if missing)"
	@echo "  help        - Show this help message"

# Automatically copy .env from template if it doesn't exist
env-check: ensure-env
	@echo "\033[1;32m[OK] .env is ready.\033[0m"

ensure-env:
	@if [ ! -f .env ]; then \
		if [ -f .env.template ]; then \
			echo "\033[1;33m[INFO] .env not found. Creating from template...\033[0m"; \
			cp .env.template .env; \
		else \
			echo "\033[1;31m[ERROR] .env.template not found. Cannot create .env.\033[0m"; \
			exit 1; \
		fi \
	fi

# Delegate to Makefile.dev
dev: env-check
	$(MAKE) -f Makefile.dev $(MAKECMDGOALS)

# Delegate to Makefile.prod
prod: env-check
	$(MAKE) -f Makefile.prod $(MAKECMDGOALS)
