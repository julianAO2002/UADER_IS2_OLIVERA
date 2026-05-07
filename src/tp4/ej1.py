"""Patrón Proxy: Ping y PingProxy."""

import subprocess
import platform


class Ping:
    def _do_ping(self, ip: str) -> None:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        for i in range(1, 11):
            result = subprocess.run(
                ["ping", param, "1", ip],
                capture_output=True,
                text=True,
            )
            status = "OK" if result.returncode == 0 else "FAIL"
            print(f"Intento {i}/10 -> {ip}: {status}")

    def execute(self, ip: str) -> None:
        if not ip.startswith("192."):
            print(f"Dirección IP '{ip}' no permitida. Solo se aceptan IPs que comiencen con '192.'")
            return
        self._do_ping(ip)

    def executefree(self, ip: str) -> None:
        self._do_ping(ip)


class PingProxy:
    _REDIRECT_IP = "192.168.0.254"
    _REDIRECT_TARGET = "www.google.com"

    def __init__(self):
        self._ping = Ping()

    def execute(self, ip: str) -> None:
        if ip == self._REDIRECT_IP:
            print(f"IP especial detectada ({ip}). Redirigiendo ping a {self._REDIRECT_TARGET}...")
            self._ping.executefree(self._REDIRECT_TARGET)
        else:
            self._ping.execute(ip)


if __name__ == "__main__":
    proxy = PingProxy()

    print("=== Caso 1: IP normal permitida (192.168.1.1) ===")
    proxy.execute("192.168.1.1")

    print("\n=== Caso 2: IP especial redirigida (192.168.0.254) ===")
    proxy.execute("192.168.0.254")

    print("\n=== Caso 3: IP no permitida (10.0.0.1) ===")
    proxy.execute("10.0.0.1")
