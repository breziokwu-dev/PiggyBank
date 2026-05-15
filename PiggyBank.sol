// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

contract PiggyBank {

    address public owner;

    uint256 public totalDeposited;

    event Deposit(address indexed depositor, uint256 amount);
    event Withdraw(uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function deposit() external payable {
        require(msg.value > 0, "Must send ETH");
        totalDeposited += msg.value;
        emit Deposit(msg.sender, msg.value);

    }

    function withdraw(uint256 amount) external onlyOwner virtual{
        require(address(this).balance >= amount, "Insufficient balance");
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
        emit Withdraw(amount);
    }

    function getBalance() external view returns (uint) {
        return address(this).balance;
    }
}