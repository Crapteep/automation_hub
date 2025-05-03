import argparse
import os
import sys
from uvicorn import run



def run_automation_hub(dev: bool):
    parser = argparse.ArgumentParser(description="Start the backend server.")
    parser.add_argument("--port", type=int, help="Port to listen on.", default=8000)
    parser.add_argument(
        "--origin",
        type=str,
        help="Origin for the frontend.",
        default="http://localhost:3000",
    )

    args = parser.parse_args()
    port = args.port
    origin = args.origin
    os.environ["CORS_ORIGIN"] = origin

    try:
        run(
            "src.main:create_app",
            host="0.0.0.0",
            port=port,
            reload=dev,
            factory=True,
        )
    except KeyboardInterrupt:
        print("Exiting ...")
        sys.exit(0)


def automation_hub_dev():
    run_automation_hub(dev=True)


def automation_hub():
    run_automation_hub(dev=False)


if __name__ == "__main__":
    automation_hub_dev()