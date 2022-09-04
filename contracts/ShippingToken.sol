/* Step 1:
/ Determine 
/ wallet owners, number of wallets, funtions needed, 
/ Step 2: code
*/  

pragma solidity ^0.5.5;
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
contract ShippingToken is ERC721Full {

   
    constructor() public ERC721Full("Certificate", "CERT"){}

    struct Shipment {
    string shipment_name;
    string origin_address;
    string destination_address;
    uint256 shipment_weight;
    uint256 num_packages;
    string plist_uri;
    string insurance_policy_uri;
    }
 //   mapping(uint256 => Shipment) public allShipments;
/*
    function createToken(string memory tokenURI) public {
        uint256 tokenCount=totalSupply();
        uint256 newTokenId=tokenCount;
        _mint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
    }
*/

/* have to have original owner, the when transfering, need to get owner (sender)
 at what point does ownership transfers */

    /*function getOwner(address TokenOwner, newTokenId) public view returns (address) {
        require (TokenOwner == msg.sender);
        /* simple transfer from 1 owner to another, confirm owner when complete
        return TokenOwner
    }*/

 /*   mapping(bytes32 => string) public requestIdToTokenURI;

    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        require (_isApprovedOrOwner(msg.sender)(), tokenId);
        _setTokenURI(tokenId, tokenURI);
        
    }

    function _setTokenURI(uint256 tokenId, string memory _tokenURI) internal virtual {
        require(_exists(tokenId), "URI set of nonexistent token");
        _tokenURIs[tokenId] = _tokenURI;
    }
*/

    mapping(uint256 => Shipment) public TotalShipment;

    function registerShipment(
        address owner,
        string memory shipment_name,
        string memory origin_address,
        string memory destination_address,
        uint256 shipment_weight,
        uint256 num_packages,
        string memory plist_uri,
        string memory insurance_policy_uri
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, plist_uri);

        TotalShipment[tokenId] = Shipment(shipment_name, origin_address, destination_address, shipment_weight, num_packages, plist_uri,insurance_policy_uri);

        return tokenId;
    }
/*
    function getTokenOwner(address TokenOwner, uint256 newTokenId) external view returns (address){
        return ShippingToken(TokenOwner).ownerOf(newTokenId);
    }
    
    function balanceOf(address owner) public returns (uint256 balance)

    function approve(uint tokens) public returns (bool success) {
        require (msg.sender == admin);
         /* makes it so only admin (3rd party) can call
        approvetransfer = true;
        require (sender == getTokenOwner());

        /* is there a third party? or is it sender or receiver approving?
    }

/* have a set address fo approver, have that address call the transfer function, only that address can call this function*/ 


    /*function transferFrom(address from, address to, uint tokens) public returns (bool success);*/

  /*  function bid(uint256 new_bid, uint256 bid_token_id) public {
        require(new_bid>current_bid[bid_token_id], "Must be higher than current bid.");
        current_bid[bid_token_id]=new_bid;
    }

    function getCurrentBid(uint256 bid_token_id) public view returns(uint256) {
        return current_bid[bid_token_id]; */
    
    /* function transfer(msg.sender, address recipient, uint amount) public payable {
        require approvetransfer = true;
        uint amount = msg.value * exchange_rate;
        balances[msg.sender] = balances[msg.sender].sub(amount);
        balances[recipient] = balances[recipient].add(amount);
        string message = "Congratulations, transaction complete";
        approvetransfer = false;
        return balances, message
    } */

    /* address seller = ownerOf(_tokenId);
        _transfer(seller, msg.sender, _tokenId);
        tokenIdToPrice[_tokenId] = 0; // not for sale anymore
        payable(seller).transfer(msg.value); // send the ETH to the seller
        emit NftBought(seller, msg.sender, msg.value);
    } /*

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