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


st.markdown("## Inspect Shipment")
num_shipments=contract.functions.totalSupply().call()
print(num_shipments)
company_df=pd.read_csv(
    Path("./Company_list.csv"), index_col="company_name")
st.write(f' Total number of Shipments in transit {num_shipments}')
current_shipment_id= st.selectbox("Choose Shipment", list(range(num_shipments)))
current_shipment=contract.functions.TotalShipment(current_shipment_id).call()
st.write(current_shipment)

st.write(f'Shipment Name: {current_shipment[0]}')
st.write(f'Picked up from (origin): {current_shipment[1]}')
st.write(f'Final Destination: {current_shipment[2]}')
st.write(f'Shipment Weight: {current_shipment[3]}')
st.write(f'Number of  Packages in Shipment: {current_shipment[4]}')
st.write(f'Shipping Documents can be viewed at : {current_shipment[5]}')
st.write(f'Insurance Documents can be viewed at : {current_shipment[6]}')

shipmentOwnerWallet=contract.functions.ownerOf(current_shipment_id).call()
shipmentOwner=company_df[company_df['Wallet']==shipmentOwnerWallet].index.values
#print(df[df[‘Name’]==’Donna’].index.values)
st.write(f'This shipment is in Transit, Currently with {shipmentOwner}')

st.markdown("---")
