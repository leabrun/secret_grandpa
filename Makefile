run:
	uvicorn src.web.main:app --reload
lint:
	flake8 src