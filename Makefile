PACKAGE_NAME=gocd-tools
PACKAGE_NAME_FORMATTED=$(subst -,_,$(PACKAGE_NAME))
OWNER=ucphhpc
IMAGE=$(PACKAGE_NAME)
TAG=edge
ARGS=

.PHONY: all init dockerbuild dockerclean dockerpush clean dist distclean maintainer-clean
.PHONY: install uninstall installtest test

all: venv install-dep init dockerbuild

init:
ifeq ($(shell test -e defaults.env && echo yes), yes)
ifneq ($(shell test -e .env && echo yes), yes)
		ln -s defaults.env .env
endif
endif

dockerbuild:
	docker build -t $(OWNER)/$(IMAGE):$(TAG) $(ARGS) .

dockerclean:
	docker rmi -f $(OWNER)/$(IMAGE):$(TAG)

dockerpush:
	docker push $(OWNER)/$(IMAGE):$(TAG)

clean:
	$(MAKE) dockerclean
	rm -fr .env
	rm -fr .pytest_cache
	rm -fr gocd_tools/__pycache__
	rm -fr tests/__pycache__

dist:
	$(VENV)/python setup.py sdist bdist_wheel

distclean:
	rm -fr dist build $(PACKAGE_NAME).egg-info $(PACKAGE_NAME_FORMATTED).egg-info

maintainer-clean:
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'
	$(MAKE) distclean
	$(MAKE) venv-clean
	$(MAKE) clean

install-dev:
	$(VENV)/pip install -r requirements-dev.txt

uninstall-dev:
	$(VENV)/pip uninstall -r requirements-dev.txt

install-dep:
	$(VENV)/pip install -r requirements.txt

uninstall-dep:
	$(VENV)/pip uninstall -y -r requirements.txt

install:
	$(MAKE) install-dep
	$(VENV)/pip install .

uninstall:
	$(MAKE) uninstall-dep
	$(MAKE) uninstall-dev
	$(VENV)/pip uninstall -y -r $(PACKAGE_NAME)

uninstalltest:
	$(VENV)/pip uninstall -y -r tests/requirements.txt

installtest:
	$(VENV)/pip install -r tests/requirements.txt

# The tests requires access to the docker socket
test:
	. $(VENV)/activate; python3 setup.py check -rms
	. $(VENV)/activate; pytest -s -v tests/

include Makefile.venv
