"""Testinfra tests for the docker playbook (RHEL 9)."""


def test_docker_ce_installed(host):
    pkg = host.package("docker-ce")
    assert pkg.is_installed, "docker-ce should be installed"


def test_docker_cli_installed(host):
    pkg = host.package("docker-ce-cli")
    assert pkg.is_installed, "docker-ce-cli should be installed"


def test_containerd_installed(host):
    pkg = host.package("containerd.io")
    assert pkg.is_installed, "containerd.io should be installed"


def test_docker_binary_exists(host):
    docker_bin = host.file("/usr/bin/docker")
    assert docker_bin.exists, "/usr/bin/docker should exist"
    assert docker_bin.is_file


def test_docker_service_enabled(host):
    service = host.service("docker")
    assert service.is_enabled, "docker service should be enabled"


def test_docker_service_running(host):
    service = host.service("docker")
    assert service.is_running, "docker service should be running"


def test_podman_not_installed(host):
    pkg = host.package("podman")
    assert not pkg.is_installed, "podman should not be installed"


def test_docker_group_exists(host):
    group = host.group("docker")
    assert group.exists, "docker group should exist"


def test_docker_socket_exists(host):
    sock = host.file("/var/run/docker.sock")
    assert sock.exists, "/var/run/docker.sock should exist"


def test_docker_repo_configured(host):
    repo = host.file("/etc/yum.repos.d/docker-ce.repo")
    assert repo.exists, "Docker CE yum repo file should exist"
