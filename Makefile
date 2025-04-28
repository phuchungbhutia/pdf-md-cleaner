# Makefile for pdf-md-cleaner

install:
	pip install -r requirements.txt

run:
	python main.py

docker-build:
	docker build -t pdf-md-cleaner .

docker-run:
	docker run --rm -v $(PWD)/example:/app/example -v $(PWD)/output:/app/output pdf-md-cleaner

# make install — install requirements

# make run — run your cleaner

# make docker-build — build docker image

# make docker-run — run inside Docker using example/ and output/ folders mounted!