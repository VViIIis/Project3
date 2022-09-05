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

st.markdown("## Transfer Shipment")
company_df=pd.read_csv(
    Path("./Company_list.csv"), index_col="company_name")
#print(company_df)
num_ship=contract.functions.totalSupply().call()
print(num_ship)
pick_ship=st.selectbox("Choose Shipment to Transfer", list(range(num_ship)))
st.write(f'shipment Picked: {pick_ship}')
shipOwnerWallet=contract.functions.ownerOf(pick_ship).call()
shipOwner=company_df[company_df['Wallet']==shipOwnerWallet].index.values
st.write (f'Currently Shipment is with {shipOwner}')
st.write (f'Owner Wallet : {shipOwnerWallet}')
option = st.selectbox(
     'Transfer Shipment to?',
     company_df.index)
#print (company_df.loc[option]['Wallet'])
#contract.functions.transferFrom(shipOwnerWallet,company_df.loc[option]['Wallet'],pick_ship)

st.write('You selected:', option)
st.write('wallet:  ', company_df.loc[option]['Wallet'])


if st.button("Transfer Shipment"):
    contract.functions.transferFrom(shipOwnerWallet,company_df.loc[option]['Wallet'],pick_ship).transact({'from': shipOwnerWallet, 'gas': 1000000})
   
st.markdown("---")
