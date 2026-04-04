.PHONY: install collections lint test converge verify destroy reset run

SCENARIO ?= docker

# Install Python dependencies via uv
install:
	uv sync

# Install Ansible collections
collections:
	uv run ansible-galaxy collection install -r requirements.yml

# Lint playbooks and roles
lint:
	uv run ansible-lint

# Full molecule test lifecycle (create -> converge -> verify -> destroy)
# Usage: make test           (uses SCENARIO=docker by default)
#        make test SCENARIO=foo
test:
	uv run molecule test -s $(SCENARIO)

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
# Usage: make run           (deploys site.yml)
#        make run PLAYBOOK=docker
run:
	uv run ansible-playbook playbooks/$(SCENARIO).yml --ask-become-pass
