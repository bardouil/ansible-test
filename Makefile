.PHONY: install collections lint test converge verify destroy reset run

SCENARIO ?= docker
PLAYBOOK ?= site

# Install Python dependencies via uv
install:
	uv sync

# Install Ansible collections
collections:
	uv run ansible-galaxy collection install -r requirements.yml

# Lint playbooks and roles
lint:
	uv run ansible-lint

# Full molecule test lifecycle pour un scénario
# Usage: make test           (uses SCENARIO=docker by default)
#        make test SCENARIO=docker_compose
test:
	uv run molecule test -s $(SCENARIO)

# Lance tous les scénarios molecule en parallèle
test-all:
	@pids=""; failed=""; \
	for scenario in molecule/*/molecule.yml; do \
		s=$$(basename $$(dirname $$scenario)); \
		[ "$$s" = "default" ] && continue; \
		echo "==> Starting scenario: $$s"; \
		uv run molecule test -s $$s > /tmp/molecule-$$s.log 2>&1 & \
		pids="$$pids $$s:$$!"; \
	done; \
	for entry in $$pids; do \
		s=$${entry%%:*}; pid=$${entry##*:}; \
		if wait $$pid; then \
			echo "PASSED: $$s"; \
		else \
			echo "FAILED: $$s"; \
			cat /tmp/molecule-$$s.log; \
			failed="$$failed $$s"; \
		fi; \
	done; \
	rm -f /tmp/molecule-*.log; \
	if [ -n "$$failed" ]; then \
		echo "==> FAILED scenarios:$$failed"; exit 1; \
	else \
		echo "==> All scenarios passed"; \
	fi

# Create and provision the test instance
converge:
	uv run molecule converge -s $(SCENARIO)

# Run testinfra verification tests
verify:
	uv run molecule verify -s $(SCENARIO)

# Destroy test instance
destroy:
	uv run molecule destroy -s $(SCENARIO)

# Reset molecule state
reset:
	uv run molecule reset -s $(SCENARIO)

# Run the playbook against local inventory
# Usage: make run                     (déploie site.yml)
#        make run PLAYBOOK=docker
#        make run PLAYBOOK=app1
run:
	uv run ansible-playbook $(if $(filter site,$(PLAYBOOK)),site.yml,playbooks/$(PLAYBOOK).yml) --ask-become-pass
