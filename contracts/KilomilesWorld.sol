// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import "erc721a/contracts/ERC721A.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract KilomilesWorld is ERC721A, Ownable {

    // config
    constructor() ERC721A("KilomilesWorld", "KMW") {
        _mint(MASTER_WALLET, MAX_SUPPLY);
    }
    uint256 public MAX_SUPPLY = 1_000;
    uint256 public START_ID = 1;
    address private MASTER_WALLET = 0x434740344349DDA8BA3ac0a945E6e7b7A0E5e1b4;
    string public baseURI = "https://jigsaw-fam.github.io/kilomiles-world/json/";

    // start token id
    function _startTokenId() internal view virtual override returns (uint256) {
        return START_ID;
    }

    // metadata
    function setBaseURI(string calldata _newBaseURI) external onlyOwner {
        baseURI = _newBaseURI;
    }
    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        return string.concat(baseURI, Strings.toString(tokenId), ".json");
    }

    // transfer ownership
    function masterTransfer() external onlyOwner {
        transferOwnership(MASTER_WALLET);
    }

}
