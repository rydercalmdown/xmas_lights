IMAGE_NAME=gcr.io/radical-sloth/crowdsourced-christmas-lights:0.0.1

.PHONY: build
build:
	@docker-compose build

.PHONY: run
run:
	@docker-compose up web

.PHONY: push
push:
	@docker-compose push

.PHONY: copy
copy:
	@cd firmware && rsync --exclude env -a ./ pi@10.0.0.171:/home/pi/lights


.PHONY: deploy
deploy:
	@gcloud run deploy internet-controlled-xmas-lights \
		--image $(IMAGE_NAME) \
		--region us-central1 \
		--port 8000 \
		--concurrency 80 \
		--cpu 1 \
		--max-instances 1 \
		--timeout 10 \
		--memory 128Mi \
		--platform managed \
		--allow-unauthenticated \
		--project radical-sloth
