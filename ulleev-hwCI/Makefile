RUN := poetry run

TEST_DIR := tests

# Allow arguments to be passed in make
PARAMS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
# Turn them into do-nothing targets
$(eval $(PARAMS):;@:)

test:
	@echo "[ \033[00;33mRunning tests\033[0m ]" && \
 		$(RUN) pytest $(PARAMS) $(TEST_DIR)


build:
	@echo "[ \033[00;33mRunning tests\033[0m ]" && \
		poetry build
