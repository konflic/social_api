import docker
from config.settings import settings

client = docker.from_env()

container = client.containers.run(
    "postgres",
    detach=True,
    ports={"5432/tcp": ("127.0.0.1", 5432)},
    environment=[
        f"POSTGRES_USER={settings.DB_USER}",
        f"POSTGRES_PASSWORD={settings.DB_PASSWORD}",
        "POSTGRES_HOST_AUTH_METHOD=trust",
    ],
    name=settings.DB_NAME,
)

print(f"Docker container with postgres is up and ready: {container.id}")
print(f"Don't forget to stop it with command 'docker kill {settings.DB_NAME}'")
