import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/shipping_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


st.title("NIFTY Global Shipping")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register New Shipment
################################################################################
st.markdown("## NIFTY Global Create Shipment")
shipment_name = st.text_input("Enter the name of the shipment")
origin_address = st.text_input("Enter the pickup location")
destination_address = st.text_input("Enter the dropoff location")
shipment_weight = st.number_input("Enter the shipment weight",value=1)
num_packages= st.number_input("Enter the number of packages in this shipment",value=1)

# initial_appraisal_value = st.text_input("Enter the initial appraisal amount")
packingList_uri = st.file_uploader("Packing List", type=["jpg", "jpeg", "png", "pdf"])
insurance_policy_uri=""

if st.button("Create Shipment"):
    plist_ipfs_hash = pin_artwork(shipment_name, packingList_uri)
    plist_uri = f"ipfs://{plist_ipfs_hash}"
    tx_hash = contract.functions.registerShipment(
        address,
        shipment_name,
        origin_address,
        destination_address,
        shipment_weight,
        num_packages,
        plist_uri,
        insurance_policy_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Shipment Created")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{plist_ipfs_hash})")
st.markdown("---")
