import uix
from uix.elements import *
from uix_components import *
import argparse
from hamming import *

DATA = []
HAMMING = []
PARITY_IDX = None
FETCHED = []

def hamming_code_simulator_ui():
    with page("") as main_page:
        with header(id="header", value="HAMMING ERROR CORRECTING CODE SIMULATOR").style("background: var(--ait); font-weight: bold; font-size: 20px;"):
            pass
        with main("",).style("padding: 20px; height: 50%;"):
                with row().size().style("align-items: start; gap: 20px;"):
                    with col(id="data_col").style("justify-content: start;"):
                        label("DATA").style("font-weight: bold; font-size: 16px;")
                        textarea(id="data", value="").style("width:200px;").on("change", set_data)
                    
                    with col(id="total_data_col").style("justify-content: start;"):
                        label("DATA WITH CHECK BITS").style("font-weight: bold; font-size: 16px;")
                        text(id="data_with_check", value="").style("width:100px;")

                    with col(id="num_parity_col").style("justify-content: start;"):
                        label("NUMBER OF PARITY BITS").style("font-weight: bold; font-size: 16px;")
                        text(id="num_parity", value="").style("width:100px;")
                    
                    with col(id="parity_bit_index_col").style("justify-content: start;"):
                        label("PARITY BIT INDEXES").style("font-weight: bold; font-size: 16px;")
                        text(id="idx_parity", value="").style("width:100px;")
                    
                    with col(id="parity_bits_col").style("justify-content: start;"):
                        label("PARITY BITS VALUE").style("font-weight: bold; font-size: 16px;")
                        text(id="parity", value="").style("width:100px;")
                    
                    with col(id="hamming_col").style("justify-content: start;"):
                        label("HAMMING CODE").style("font-weight: bold; font-size: 16px;")
                        text(id="hamming", value="").style("width:100px;")

                    with col(id="error_col").style("justify-content: start;"):
                        label("ERROR CODE").style("font-weight: bold; font-size: 16px;")
                        textarea(id="error_code", value="").style("width:200px;").on("change", set_fetched_data)

                    with col(id="yndrome_col").style("justify-content: start;"):
                        button(id="error_btn", value="CALCULATE ERROR").style("margin-top:20px;").size("200px").on("click", calculate_syndrome)
                    
                    with col(id="syndrome_col").style("justify-content: start;"):
                        label("ERROR SYNDROME IDX").style("font-weight: bold; font-size: 16px;")
                        text(id="error_syndrome", value="").style("width:100px;")

        
        with row(id="table").size().style("justify-contect: center; gap: 20px;"):
            create_table()


def create_table():
    global DATA, HAMMING, PARITY_IDX, FETCHED
    with table("", id="table_example").style("width: 70%;"):
        with thead("",):
            with tr("",):
                th("IDX")
                for i in range(1, len(HAMMING)+1):
                    th(f"{i}")
        with tbody("",id="table_example_body"):
                with tr("",id="table_example_header_row"):
                    th("Bit Position")
                    for i in range(len(HAMMING)-1, -1, -1):
                        th(f"{str(i)}")

                with tr("",):
                    th("Position Number")
                    for i in range(len(HAMMING)-1 , -1, -1):
                        th(f"{i:04b}")

                with tr("",):
                    th("Data Bit")
                    for i in range(len(HAMMING)):
                            if i in PARITY_IDX:
                                th("-")
                            else:
                                th(f"{HAMMING[i]}")
                with tr("",):
                    th("Check Bit")
                    for i in range(len(HAMMING)):
                        if i in PARITY_IDX:
                            th(f"{HAMMING[i]}")
                        else:
                            th("-")
                with tr("",):
                    th("Word Stored")
                    for i in range(len(HAMMING)):
                        th(f"{HAMMING[i]}") 
                
                with tr("",):
                    th("Word Fetches")
                    for i in range(len(FETCHED)):
                        th(f"{FETCHED[i]}", id=f"fc_{i}")
                        

def set_fetched_data(ctx, id, value):
    global FETCHED
    
    value = value.split(",")
    fetched = [int(i) for i in value]
    FETCHED = fetched.copy()

    ctx.elements["error_code"].value = fetched
    ctx.elements["table"].update(create_table)
    if FETCHED != HAMMING:
        diff = [i for i in range(len(HAMMING)) if HAMMING[i] != FETCHED[i]]
        for i in diff:
            ctx.elements[f"fc_{i}"].set_style("background",  "red")
    

def set_data(ctx, id, value):
    global DATA, HAMMING, PARITY_IDX, FETCHED
    data = [int(i) for i in value]
    DATA = data.copy()
    ctx.elements["data"].value = data

    number_of_parity = calculate_number_of_parity(len(data))
    ctx.elements["num_parity"].value = number_of_parity

    idx_parity = calculate_parity_bit_indexes(number_of_parity)
    ctx.elements["idx_parity"].value = idx_parity
    PARITY_IDX = idx_parity.copy()

    parity_bits = calculate_hamming_code(data, idx_parity)
    ctx.elements["hamming"].value = parity_bits
    ctx.elements["error_code"].value = parity_bits
    HAMMING = parity_bits.copy()

    FETCHED = [int(i) for i in parity_bits]
    parity_value = [parity_bits[i] for i in range(len(parity_bits)) if i in idx_parity]
    ctx.elements["parity"].value = parity_value

    data_with_check = []
    for i in range(len(data) + number_of_parity):
        if i in idx_parity:
            data_with_check.append("-")
        else:
            data_with_check.append(str(data.pop(0)))
    ctx.elements["data_with_check"].value = data_with_check
    ctx.elements["table"].update(create_table)

def calculate_syndrome(ctx, id, value):
    global DATA, HAMMING, PARITY_IDX, FETCHED
    error_syndrome = calculate_error_syndrome(FETCHED, PARITY_IDX)
    ctx.elements["error_syndrome"].value = error_syndrome

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5008)
    uix.start(ui = hamming_code_simulator_ui, config = {"debug":True,  "port": parser.parse_args().port})