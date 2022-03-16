import { useEthers } from "@usedapp/core"
import { BalanceMsg } from "../BalanceMsg"
import { Token } from "../Main"
import { useGetStakeBalance } from "../../hooks/useTokenFarm"

interface StakeBalanceProps {
    token: Token
}

export const StakeBalance = ({ token }: StakeBalanceProps) => {
    const { image, address, name } = token
    const { account } = useEthers()
    const formattedStakeBalance = useGetStakeBalance(address, account)

    return (
        <BalanceMsg
            label={`You staked ${name} balance`}
            tokenImgSrc={image}
            amount={formattedStakeBalance} />
    )
}