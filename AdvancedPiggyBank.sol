// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import {PiggyBank} from "./PiggyBank.sol";

import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

contract AdvancedPiggyBank is PiggyBank{

    uint256 public dailyLimit;
    uint256 public lastWithdrawDay;
    uint256 public withdrawnToday;

    AggregatorV3Interface private priceFeed;

constructor() {
    dailyLimit = 0.005 ether;
    priceFeed = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306);
}

    function withdraw(uint256 amount) external onlyOwner override {
        uint256 today = block.timestamp / 1 days;
        if (today > lastWithdrawDay) {
            lastWithdrawDay = today;       
            withdrawnToday = 0;

        }
        require(withdrawnToday + amount <= dailyLimit, "Daily limit exceeded");
        withdrawnToday += amount;
        require(address(this).balance >= amount, "Insufficient balance");
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
        emit Withdraw(amount);      
    }

    function setDailyLimit(uint256 newLimit) public onlyOwner {
         dailyLimit = newLimit;
    }

    function getWithdrawnToday() external view returns (uint256) {
        return withdrawnToday;
    }
    
    receive() external payable {
        require(msg.value > 0, "Must send ETH");
        totalDeposited += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function getLatestPrice() public view returns (uint256) {
        (, int256 price,,,) = priceFeed.latestRoundData();
        return uint256(price);
    }

    function getBalanceInUSD() public view returns (uint256) {
    uint256 ethBalance = address(this).balance;
    uint256 ethPrice = getLatestPrice();
    uint256 usdValue = (ethBalance * ethPrice) / 1e26;
    return usdValue;
    }


}