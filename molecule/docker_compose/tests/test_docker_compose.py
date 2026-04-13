"""Testinfra tests for the docker_compose role."""

PROJECT_PATH = "/opt/testapp"


def test_project_directory_exists(host):
    d = host.file(PROJECT_PATH)
    assert d.exists
    assert d.is_directory


def test_project_directory_mode(host):
    d = host.file(PROJECT_PATH)
    assert d.mode == 0o755


def test_compose_file_exists(host):
    f = host.file(f"{PROJECT_PATH}/docker-compose.yml")
    assert f.exists
    assert f.is_file


def test_compose_file_mode(host):
    f = host.file(f"{PROJECT_PATH}/docker-compose.yml")
    assert f.mode == 0o644


def test_compose_file_content(host):
    f = host.file(f"{PROJECT_PATH}/docker-compose.yml")
    assert "testapp_app" in f.content_string
    assert "nginx:alpine" in f.content_string


def test_env_file_exists(host):
    f = host.file(f"{PROJECT_PATH}/.env")
    assert f.exists
    assert f.is_file


def test_env_file_mode(host):
    """Le fichier .env doit être restreint (sensible)."""
    f = host.file(f"{PROJECT_PATH}/.env")
    assert f.mode == 0o600


def test_env_file_content(host):
    f = host.file(f"{PROJECT_PATH}/.env")
    assert "APP_NAME=testapp" in f.content_string
    assert "APP_ENV=test" in f.content_string


def test_config_file_exists(host):
    f = host.file(f"{PROJECT_PATH}/config.yml")
    assert f.exists
    assert f.is_file


def test_config_file_mode(host):
    f = host.file(f"{PROJECT_PATH}/config.yml")
    assert f.mode == 0o644


def test_config_file_content(host):
    f = host.file(f"{PROJECT_PATH}/config.yml")
    assert "project: testapp" in f.content_string


def test_project_directory_owner(host):
    d = host.file(PROJECT_PATH)
    assert d.user == "root"
    assert d.group == "root"
