import { Token } from "../Main"
import { useEthers, useTokenBalance } from "@usedapp/core"
import { formatUnits } from "@ethersproject/units"
import { BalanceMsg } from "../BalanceMsg"
import { BigNumber } from 'ethers'


export interface WalletBalanceProps {
    token: Token
}

export const useGetFixFormattedTokenBalance = (tokenAddress: string | false | 0 | null | undefined, account: string | false | 0 | null | undefined) => {
    const tokenBalance = useTokenBalance(tokenAddress, account)
    // const formattedTokenBalance: number = (
    //     tokenBalance ?
    //         parseFloat((parseFloat(formatUnits(tokenBalance, 18)) - 0.000000000005).toFixed(11)) :
    //         0
    // )
    const balanceLen = tokenBalance?.toString().length
    const balanceIntLen = balanceLen ? balanceLen - 18 : 0
    // console.log(balanceIntLen)
    // console.log(tokenBalance)
    // console.log(tokenBalance?.toString().slice(0, balanceIntLen + 12))
    const fixBalance = tokenBalance && !tokenBalance.isZero() ?
        BigNumber.from(tokenBalance?.toString().slice(0, balanceIntLen + 11)) :
        undefined
    // console.log(fixBalance)
    const formattedTokenBalance: number = (
        fixBalance ?
            parseFloat(formatUnits(fixBalance, 11)) :
            0
    )
    return formattedTokenBalance
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address, name } = token
    const { account } = useEthers()
    const formattedTokenBalance = useGetFixFormattedTokenBalance(address, account)
    // const tokenBalance = useTokenBalance(address, account)
    // console.log(name)
    // console.log(tokenBalance?.toString())
    // const formattedTokenBalance: number = (
    //     tokenBalance ?
    //         parseFloat((parseFloat(formatUnits(tokenBalance, 18)) - 0.000000000005).toFixed(11)) :
    //         0
    // )
    return (
        <BalanceMsg
            label={`Your un-staked ${name} balance`}
            tokenImgSrc={image}
            amount={formattedTokenBalance} />

    )
}