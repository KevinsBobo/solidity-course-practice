// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DappToken is ERC20 {
    // wei
    constructor() ERC20("DappToken", "DAPP") {
        _mint(msg.sender, 10**24);
    }
}
