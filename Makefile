PACKAGE_NAME=gocd-tools
PACKAGE_NAME_FORMATTED=$(subst -,_,$(PACKAGE_NAME))
OWNER=ucphhpc
IMAGE=$(PACKAGE_NAME)
TAG=edge
ARGS=

.PHONY: all
all: venv install-dep init dockerbuild

.PHONY: init
init:
ifeq ($(shell test -e defaults.env && echo yes), yes)
ifneq ($(shell test -e .env && echo yes), yes)
		ln -s defaults.env .env
endif
endif

.PHONY: dockerbuild
dockerbuild:
	docker build -t $(OWNER)/$(IMAGE):$(TAG) $(ARGS) .

.PHONY: dockerclean
dockerclean:
	docker rmi -f $(OWNER)/$(IMAGE):$(TAG)

.PHONY: dockerpush
dockerpush:
	docker push $(OWNER)/$(IMAGE):$(TAG)

.PHONY: clean
clean: distclean dockerclean
	rm -fr .env
	rm -fr .pytest_cache
	rm -fr gocd_tools/__pycache__
	rm -fr tests/__pycache__

.PHONY: dist
dist: venv install-dist-dep
	$(VENV)/python -m build .

.PHONY: install-dist-dep
install-dist-dep: venv
	$(VENV)/pip install build

.PHONY: distclean
distclean:
	rm -fr dist build $(PACKAGE_NAME).egg-info $(PACKAGE_NAME_FORMATTED).egg-info

.PHONY: maintainer-clean
maintainer-clean:
	@echo 'This command is intended for maintainers to use; it'
	@echo 'deletes files that may need special tools to rebuild.'
	$(MAKE) distclean
	$(MAKE) venv-clean
	$(MAKE) clean

.PHONY: install-dev
install-dev: venv
	$(VENV)/pip install -r requirements-dev.txt

.PHONY: uninstall-dev
uninstall-dev: venv
	$(VENV)/pip uninstall -r requirements-dev.txt

.PHONY: install-dep
install-dep: venv
	$(VENV)/pip install -r requirements.txt

.PHONY: uninstall-dep
uninstall-dep: venv
	$(VENV)/pip uninstall -y -r requirements.txt

.PHONY: install
install: venv install-dev
	$(VENV)/pip install .

.PHONY: uninstall
uninstall: venv
	$(VENV)/pip uninstall -y -r $(PACKAGE_NAME)

.PHONY: uninstalltest
uninstalltest: venv
	$(VENV)/pip uninstall -y -r tests/requirements.txt

.PHONY: installtest
installtest: venv
	$(VENV)/pip install -r tests/requirements.txt

.PHONY: test
# The tests requires access to the docker socket
test: venv installtest
	. $(VENV)/activate; python3 setup.py check -rms
	. $(VENV)/activate; pytest -s -v tests/

include Makefile.venv
