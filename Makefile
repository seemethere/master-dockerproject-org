.PHONY: index

ifndef AWS_ACCESS_KEY_ID
$(error AWS_ACCESS_KEY_ID is not set)
endif

ifndef AWS_SECRET_ACCESS_KEY
$(error AWS_SECRET_ACCESS_KEY is not set)
endif

all: index

index:
	docker build -t dockerproject-uploader .
	@docker run \
		-e AWS_ACCESS_KEY_ID="$(AWS_ACCESS_KEY_ID)" \
		-e AWS_SECRET_ACCESS_KEY="$(AWS_SECRET_ACCESS_KEY)" \
		--rm dockerproject-uploader
