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
    #st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{plist_ipfs_hash})")
st.markdown("---")

###
################################################################################
#Transfer Shipment
################################################################################
st.markdown("## Transfer Shipment")
company_df=pd.read_csv(
    Path("./Company_list.csv"), index_col="company_name")
print(company_df)
option = st.selectbox(
     'Transfer Shipment to?',
     company_df.index)
print (company_df.loc[option]['Wallet'])
contract.functions.transferFrom(address,company_df.loc[option]['Wallet'],2)

st.write('You selected:', option)
st.write('wallet:  ', company_df.loc[option]['Wallet'])

#tokens = contract.functions.totalSupply().call()
#token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
#new_appraisal_value = st.text_input("Enter the new appraisal amount")
#appraisal_report_content = st.text_area("Enter details for the Appraisal Report")
if st.button("Transfer Shipment"):

    # Use Pinata to pin an appraisal report for the report URI
    appraisal_report_ipfs_hash =  pin_appraisal_report(appraisal_report_content)
    report_uri = f"ipfs://{appraisal_report_ipfs_hash}"

    # Use the token_id and the report_uri to record the appraisal
    tx_hash = contract.functions.newAppraisal(
        token_id,
        int(new_appraisal_value),
        report_uri
    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get the appraisal report history")
art_token_id = st.number_input("Artwork ID", value=0, step=1)
if st.button("Get Appraisal Reports"):
    appraisal_filter = contract.events.Appraisal.createFilter(
        fromBlock=0, argument_filters={"tokenId": art_token_id}
    )
    reports = appraisal_filter.get_all_entries()
    if reports:
        for report in reports:
            report_dictionary = dict(report)
            st.markdown("### Appraisal Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Pinata IPFS Report URI")
            report_uri = report_dictionary["args"]["reportURI"]
            report_ipfs_hash = report_uri[7:]
            st.markdown(
                f"The report is located at the following URI: "
                f"{report_uri}"
            )
            st.write("You can also view the report URI with the following ipfs gateway link")
            st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            st.markdown("### Appraisal Event Details")
            st.write(report_dictionary["args"])
    else:
        st.write("This artwork has no new appraisals")
