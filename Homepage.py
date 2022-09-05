import streamlit as st


st.set_page_config(
    page_title = "multipage app", 
)

st.sidebar.success("Select Options")

st.title("NIFTY Global Shipping Tracker")

st.markdown("Using an NFT token to represent a shipment and multiple wallets representing logistic / supply chain checkpoints is an innovative new way to solve shipping and supply chain logistics tracking. Instead of keeping track of shipments in a centralized database or spreadsheet, we propose using NFTs and crypto wallets on a private network as a combination shipping documentation AND representational model of the supply chain network. An NFT will be transferred between wallets representing different supply chain checkpoints that model the actual physical shipping network, along with documentation for the shipment’s contents and other metadata, for instance tamperproofing. Built on a private network rather than the public Eth network to eliminate gas fees, the NFT/Checkpoint Wallet system is an inexpensive, secure, and elegant  solution for tracking shipping logistics.")

st.image("logo.jpg")