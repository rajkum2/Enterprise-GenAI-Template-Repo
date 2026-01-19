import os


def get_env(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name, default)


def get_service_name() -> str:
    return get_env("OTEL_SERVICE_NAME", "policy-service") or "policy-service"
