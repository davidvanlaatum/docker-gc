CGO_ENABLED=0
GOOS=linux
GOARCH=amd64
COMMIT=`git rev-parse --short HEAD`
APP=docker-gc
REPO?=ndeloof/$(APP)
TAG?=latest
VERSION=1.0.0

all: image

deps:
	@go get -d -v

build: build-docker

build-app: docker-gc

docker-gc: deps
	@go build -v -a -tags netgo -ldflags '-w'

build-docker:
	@docker run --rm -v $(PWD):/usr/src/$(APP) -w /usr/src/$(APP) golang bash -c "make build-app"

build-image:
	@docker build -t $(REPO):$(TAG) .
	@echo "Image created: $(REPO):$(TAG)"

image: build build-image

clean:
	@rm docker-gc

.PHONY: deps build build-docker build-app build-image image clean

tar:
	mkdir -p docker-gc-$(VERSION)
	cp gc.go docker-gc-$(VERSION)/
	cp docker-gc-rh7.service docker-gc-$(VERSION)/docker-gc.service
	tar -zcf docker-gc-$(VERSION).tar.gz docker-gc-$(VERSION)
	rm -rf docker-gc-$(VERSION)

rpm: tar
	cp docker-gc-$(VERSION).tar.gz ~/rpmbuild/SOURCES/
	rpmbuild -ba docker-gc.spec
