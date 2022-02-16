// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract  SimpleStorage {
    uint256 public favoriteNumber = 5;
    bool favoriteBool = true;
    string favoriteString = "Sting";
    int256 favoriteInt = -5;
    address favoriteAddress = 0x8AcCBfeC3fA1A4b10c64730919201bD5D2D4Cc77;
    bytes32 favoriteBytes = "cat";

    // this will get initialzed to 0!
    uint256 faovriteNumberZero;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    mapping(string => uint256) public nameToFavoriteNumber;

    People public person = People({
        favoriteNumber: 2,
        name:"Bob"
    });

    People[] public people;

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }


    function retrive0() public view returns(uint256) {
        return favoriteNumber;
    }

    // view, pure
    function retrive1(uint256 _a) public pure returns(uint256) {
        return _a + _a;
    }
}