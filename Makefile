.PHONY: install test serve generate

install:
	pip install -e ".[dev]"

test:
	pytest

serve:
	uvicorn main:app --reload

generate:
	storycast create --topic "$(TOPIC)"
