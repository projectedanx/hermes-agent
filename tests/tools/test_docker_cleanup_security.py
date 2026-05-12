import subprocess
from unittest.mock import MagicMock
import pytest
from tools.environments import docker as docker_env

def test_cleanup_uses_safe_subprocess_calls(monkeypatch):
    """Verify that cleanup() uses the new safe Popen calls instead of shell=True."""

    # Mock find_docker to return a "dangerous" path
    monkeypatch.setattr(docker_env, "find_docker", lambda: "/usr/bin/docker; echo injected")

    # Mock subprocess.run for _ensure_docker_available and container start
    def mock_run(cmd, **kwargs):
        if "version" in cmd:
            return subprocess.CompletedProcess(cmd, 0, stdout="Docker version", stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="container-id; injected", stderr="")

    monkeypatch.setattr(docker_env.subprocess, "run", mock_run)

    # Mock subprocess.Popen to capture calls
    popen_calls = []
    def mock_popen(cmd, **kwargs):
        popen_calls.append((cmd, kwargs))
        # Return a mock process
        mock_proc = MagicMock()
        return mock_proc

    monkeypatch.setattr(docker_env.subprocess, "Popen", mock_popen)

    # Initialize environment
    env = docker_env.DockerEnvironment(image="busybox", task_id="test-task")

    # Ensure it's not persistent so both Popen calls are made
    env._persistent = False

    # Trigger cleanup
    env.cleanup()

    # Check popen_calls
    # We expect 3 calls: 1 from init_session (via _run_bash -> _popen_bash) and 2 from cleanup
    assert len(popen_calls) == 3

    # First call is init_session, second and third are cleanup
    # First call: stop/rm
    cmd1, kwargs1 = popen_calls[1]
    assert isinstance(cmd1, list)
    assert cmd1[0] == "sh"
    assert cmd1[1] == "-c"
    assert '"$1" stop "$2" || "$1" rm -f "$2"' in cmd1[2]
    assert cmd1[4] == "/usr/bin/docker; echo injected"
    assert cmd1[5] == "container-id; injected"
    assert kwargs1.get("shell") is not True
    assert kwargs1.get("stdout") == subprocess.DEVNULL
    assert kwargs1.get("stderr") == subprocess.DEVNULL

    # Second call: delayed rm
    cmd2, kwargs2 = popen_calls[2]
    assert isinstance(cmd2, list)
    assert cmd2[0] == "sh"
    assert '"$1" rm -f "$2"' in cmd2[2]
    assert cmd2[4] == "/usr/bin/docker; echo injected"
    assert cmd2[5] == "container-id; injected"
    assert kwargs2.get("shell") is not True
    assert kwargs2.get("stdout") == subprocess.DEVNULL
    assert kwargs2.get("stderr") == subprocess.DEVNULL

def test_cleanup_exception_handling(monkeypatch, caplog):
    """Ensure exceptions in Popen don't crash cleanup."""
    monkeypatch.setattr(docker_env, "find_docker", lambda: "docker")

    def mock_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="cid", stderr="")
    monkeypatch.setattr(docker_env.subprocess, "run", mock_run)

    def mock_popen_fail(*args, **kwargs):
        raise RuntimeError("Popen failed")
    monkeypatch.setattr(docker_env.subprocess, "Popen", mock_popen_fail)

    env = docker_env.DockerEnvironment(image="busybox")

    import logging
    with caplog.at_level(logging.WARNING):
        env.cleanup()

    assert "Failed to stop container" in caplog.text
