run:
	uvicorn src.app.main:app --reload
lint:
	flake8 src