run:
	 uvicorn apps.views.main:app --reload

admin:
	python create_admin.py

check-email:
	python check_email.py
