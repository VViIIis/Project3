/ Step 1:
/ Determine 
/ wallet owners, number of wallets, funtions needed, 
/ Step 2: 
/ code 

pragma solidity ^0.5.5;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
contract ShippingToken is ERC721Full {

    address payable TokenOwner;
    mapping(uint256=>uint256) current_bid;
    string public symbol = "SHIP";
    
    constructor() public ERC721Full("Certificate", "CERT"){}
    function createToken(string memory tokenURI) public {
        uint256 tokenCount=totalSupply();
        uint256 newTokenId=tokenCount;
        _mint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
    }

/* have to have original owner, the when transfering, need to get owner (sender)
 at what point does ownership transfers */

    /*function getOwner(address TokenOwner, newTokenId) public view returns (address) {
        require (TokenOwner == msg.sender);
        /* simple transfer from 1 owner to another, confirm owner when complete
        return TokenOwner
    }*/

    function getTokenOwner(address TokenOwner, uint256 newTokenId) external view returns (address){
        return ShippingToken(TokenOwner).ownerOf(newTokenId);
    }
    
    function approve(msg.sender, uint tokens) public returns (bool success) {
        require (sender == getTokenOwner());
        


        /* is there a third party? or is it sender or receiver approving? */

    }

    /*function transferFrom(address from, address to, uint tokens) public returns (bool success);*/

    function bid(uint256 new_bid, uint256 bid_token_id) public {
        require(new_bid>current_bid[bid_token_id], "Must be higher than current bid.");
        current_bid[bid_token_id]=new_bid;
    }

    function getCurrentBid(uint256 bid_token_id) public view returns(uint256) {
        return current_bid[bid_token_id];
    
     function transfer(msg.sender, address recipient, uint amount) public payable {
        uint amount = msg.value * exchange_rate;
        balances[msg.sender] = balances[msg.sender].sub(amount);
        balances[recipient] = balances[recipient].add(amount);
        return balances, string "Congratulations, transaction complete"
    }

    /*function verify(address recipient, address sender, uint) public {
        receiver address;
        sender address;
        require (sender == getTokenOwner());
        return addresses 
        /* return baances for both parties, less gas, identifying sender (we cannot transfer ownership until sender is confirmed) */
        /* return owner addresses with getowner func, balances for sender & receiver
    }*/



 /* fallback function necessary? 
 if something happens during transaction, who receives the payment? 
 old owner or future owner or project owner
can we require (receiver == receiver)
 */



}

/* deploy on remix, check balances on ganache/*

