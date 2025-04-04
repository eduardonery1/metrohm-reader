import os
import sys
import subprocess
import importlib.util
import logging


def launch_streamlit():
    """Find app.py and launch Streamlit."""
    if getattr(sys, 'frozen', False):  # Running as a compiled binary
        script_path = os.path.join(sys._MEIPASS, "app.py")
    else:  # Running as a script
        script_path = os.path.join(os.path.dirname(__file__), "app.py")

    print("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", script_path], check=True) 
    logging.debug(script_path)


if __name__ == "__main__":
    level = logging.DEBUG if len(sys.argv) > 1 and sys.argv[1] == "debug" else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    launch_streamlit()

