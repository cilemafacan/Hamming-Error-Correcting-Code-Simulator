import uix
from uix.elements import *
from uix_components import *
import argparse

def hamming_code_simulator_ui():
     with row().style("padding: 20px; box-sizing: border-box;").cls("border") as page:
        with row().size().style("justify-content: start; align-items:start; gap: 5px;"):
            with col(id="left_col").style("gap: 10px; width: 35%"):
                textarea("data", "Data", "1, 0, 1, 1")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5001)
    uix.start(ui = hamming_code_simulator_ui, config = {"debug":True,  "port": parser.parse_args().port})