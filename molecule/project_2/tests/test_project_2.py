"""Testinfra tests for project_2 deployment."""

PROJECT_PATH = "/opt/project2"
PROJECT_NAME = "project2"


def test_project_directory_exists(host):
    d = host.file(PROJECT_PATH)
    assert d.exists
    assert d.is_directory


def test_project_directory_mode(host):
    d = host.file(PROJECT_PATH)
    assert d.mode == 0o755


def test_project_directory_owner(host):
    d = host.file(PROJECT_PATH)
    assert d.user == "root"
    assert d.group == "root"


def test_compose_file_exists(host):
    f = host.file(f"{PROJECT_PATH}/docker-compose.yml")
    assert f.exists
    assert f.is_file


def test_compose_file_mode(host):
    f = host.file(f"{PROJECT_PATH}/docker-compose.yml")
    assert f.mode == 0o644


def test_compose_file_content(host):
    f = host.file(f"{PROJECT_PATH}/docker-compose.yml")
    assert f"{PROJECT_NAME}_app" in f.content_string
    assert "nginx:alpine" in f.content_string


def test_env_file_exists(host):
    f = host.file(f"{PROJECT_PATH}/.env")
    assert f.exists
    assert f.is_file


def test_env_file_mode(host):
    f = host.file(f"{PROJECT_PATH}/.env")
    assert f.mode == 0o600


def test_env_file_content(host):
    f = host.file(f"{PROJECT_PATH}/.env")
    assert f"APP_NAME={PROJECT_NAME}" in f.content_string
    assert "APP_ENV=test" in f.content_string
