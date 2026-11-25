"""Start the title and outline A2A servers, then run the routing client against them."""

import asyncio
import os
import subprocess
import sys
import time

import httpx
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ["SERVER_URL"]
SERVERS = [
    {"name": "TitleAgent", "type": "title", "port": os.environ["TITLE_AGENT_PORT"]},
    {"name": "OutlineAgent", "type": "outline", "port": os.environ["OUTLINE_AGENT_PORT"]},
]


async def wait_until_ready(server: dict, timeout: int = 60) -> bool:
    url = f"http://{HOST}:{server['port']}/health"
    start = time.time()
    async with httpx.AsyncClient() as client:
        while time.time() - start < timeout:
            try:
                if (await client.get(url, timeout=2)).status_code == 200:
                    print(f"{server['name']} is ready on port {server['port']}")
                    return True
            except Exception:
                pass
            await asyncio.sleep(1)
    print(f"Timed out waiting for {url}")
    return False


async def main() -> None:
    procs: list[subprocess.Popen] = []
    try:
        for server in SERVERS:
            print(f"Starting {server['name']}...")
            procs.append(
                subprocess.Popen(
                    [sys.executable, "a2a_server.py", "--agent-type", server["type"]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            )
            if not await wait_until_ready(server):
                print("Server failed to start. Run a2a_server.py manually to see the error.")
                return

        from routing_client import main as client_main

        await client_main()
    finally:
        print("Stopping servers...")
        for proc in procs:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    asyncio.run(main())
