import { ContractCall, useContractCall, useContractFunction, useEthers } from "@usedapp/core"
import TokenFarm from "../chain-info/contracts/TokenFarm.json"
import ERC20 from "../chain-info/contracts/MockWETH.json"
import { constants, utils } from "ethers"
import { Contract } from "@ethersproject/contracts"
import { useEffect, useState } from "react"
import networkMapping from "../chain-info/deployments/map.json"
import { formatUnits } from "@ethersproject/units"


function useGetTokenFarmAddress() {
    //address
    // chainId
    const { chainId } = useEthers()
    const tokenFarmAddress = (chainId ?
        networkMapping[String(chainId)]["TokenFarm"][0] :
        constants.AddressZero
    )
    return tokenFarmAddress
}

function useGetTokenFarmContract(tokenFarmAddress: string) {
    // abi
    const { abi } = TokenFarm
    // console.log(`TokenFarm address: ${tokenFarmAddress}`)
    const tokenFarmInterface = new utils.Interface(abi)
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface)
    return tokenFarmContract
}

export const useGetStakeBalance = (tokenAddress: string, account: string | null | undefined) => {
    const tokenFarmAddress = useGetTokenFarmAddress()
    // const tokenFarmContract = useGetTokenFarmContract(tokenFarmAddress)
    const { abi } = TokenFarm
    const contractCall: ContractCall = {
        abi: new utils.Interface(abi),
        address: tokenFarmAddress,
        method: "stakingBalance",
        args: [tokenAddress, account]
    }
    const [value] = useContractCall(contractCall) ?? []
    console.log(value?.toString())

    const formattedTokenBalance: number = (
        value ?
            parseFloat(formatUnits(value, 18)) :
            0
    )
    return formattedTokenBalance
}

export const useUnstackTokens = (tokenAddress: string) => {
    const tokenFarmAddress = useGetTokenFarmAddress()
    const tokenFarmContract = useGetTokenFarmContract(tokenFarmAddress)
    // stake
    const { send: unstakedSend, state: unstakeErc20State } = useContractFunction(
        tokenFarmContract,
        "unstakeTokens",
        { transactionName: "Unstake Tokens" }
    )

    const unstake = () => {
        console.log("unstake!")
        return unstakedSend(tokenAddress)
    }

    return { unstake, unstakeErc20State }

}

export const useApproveTokens = (tokenAddress: string) => {
    const tokenFarmAddress = useGetTokenFarmAddress()

    const erc20ABI = ERC20.abi
    const erc20Interface = new utils.Interface(erc20ABI)
    const erc20Contract = new Contract(tokenAddress, erc20Interface)
    // approve
    const { send: approveErc20Send, state: approveErc20State } = useContractFunction(
        erc20Contract,
        "approve",
        { transactionName: "Approve ERC20 transfer" }
    )
    const approve = (amount: string) => {
        console.log("approve!")
        return approveErc20Send(tokenFarmAddress, amount)
    }
    return { approve, approveErc20State }
}

export const useStakeTokens = (tokenAddress: string) => {
    const tokenFarmAddress = useGetTokenFarmAddress()
    const tokenFarmContract = useGetTokenFarmContract(tokenFarmAddress)
    // stake
    const { send: stakedSend, state: stakeErc20State } = useContractFunction(
        tokenFarmContract,
        "stakeTokens",
        { transactionName: "Stake Tokens" }
    )

    const stake = (amount: string) => {
        console.log("stake!")
        return stakedSend(amount, tokenAddress)
    }

    return { stake, stakeErc20State }
}

export const useApproveAndStakeTokens = (tokenAddress: string) => {
    // abi
    const tokenFarmAddress = useGetTokenFarmAddress()
    // console.log(`TokenFarm address: ${tokenFarmAddress}`)
    const tokenFarmContract = useGetTokenFarmContract(tokenFarmAddress)

    const erc20ABI = ERC20.abi
    const erc20Interface = new utils.Interface(erc20ABI)
    const erc20Contract = new Contract(tokenAddress, erc20Interface)
    // approve
    const { send: approveErc20Send, state: approveAndStakeErc20State } = useContractFunction(
        erc20Contract,
        "approve",
        { transactionName: "Approve ERC20 transfer" }
    )
    const approveAndStake = (amount: string) => {
        setAmountToStake(amount)
        console.log("approve!")
        return approveErc20Send(tokenFarmAddress, amount)
    }
    // stake
    const { send: stakedSend, state: stakeState } = useContractFunction(
        tokenFarmContract,
        "stakeTokens",
        { transactionName: "Stake Tokens" }
    )

    const [amoutnToStake, setAmountToStake] = useState("0")

    // useEffect
    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            console.log("stake!")
            console.log(amoutnToStake)
            console.log(tokenAddress)
            // stake func
            stakedSend(amoutnToStake, tokenAddress)
        }
    }, [approveAndStakeErc20State, amoutnToStake, tokenAddress])

    const [state, setState] = useState(approveAndStakeErc20State)

    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            setState(stakeState)
        } else {
            setState(approveAndStakeErc20State)
        }
    }, [approveAndStakeErc20State, stakeState])

    return { approveAndStake, state }
}