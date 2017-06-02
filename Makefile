.PHONY: index static_assets

ifndef AWS_ACCESS_KEY_ID
$(error AWS_ACCESS_KEY_ID is not set)
endif

ifndef AWS_SECRET_ACCESS_KEY
$(error AWS_SECRET_ACCESS_KEY is not set)
endif

ifndef BUCKET_NAME
$(error BUCKET_NAME is not set)
endif

all: index static_assets

index:
	docker build -t dockerproject-uploader .
	@echo -n "Attempting to upload index.html... "
	@docker run \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		-e BUCKET_NAME \
		--rm dockerproject-uploader
	@echo "Success!"

static_assets:
	@echo -n "Attempting to upload static assets... "
	@docker run \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		-e BUCKET_NAME \
		-v $(CURDIR)/static:/static \
		--rm anigeo/awscli \
		s3 sync --acl public-read /static "s3://$$BUCKET_NAME/static/"
	@echo "Success!"
