import React, { useState, useEffect } from "react"
import { Token } from "../Main"
import { useEthers, useTokenBalance, useNotifications, useTokenAllowance } from "@usedapp/core"
import { formatUnits } from "@ethersproject/units"
import { Button, CircularProgress, Input, Snackbar, Theme } from "@material-ui/core"
import { Alert } from "@material-ui/lab"
import { useStakeTokens, useApproveTokens, useApproveAndStakeTokens } from "../../hooks/useTokenFarm"
import { constants, utils, BigNumber } from "ethers"
import { makeStyles, Grid, Typography, Slider } from '@material-ui/core';
import { SliderInput } from "./SliderInput"
import networkMapping from "../../chain-info/deployments/map.json"
import { useGetFixFormattedTokenBalance } from "./WalletBalance"


export interface StakeFormProps {
    token: Token
}

const useStyles = makeStyles((theme: Theme) => ({
    container: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: theme.spacing(2),
        width: "100%",
    },
    slider: {
        width: "100%",
        maxWidth: "400px",
    },
}))

// export const useGetTokenFarmAddress = () => {
//     //address
//     // chainId
//     const { chainId } = useEthers()
//     const tokenFarmAddress = (chainId ?
//         networkMapping[String(chainId)]["TokenFarm"][0] :
//         constants.AddressZero
//     )
//     return tokenFarmAddress
// }

export const StakeForm = ({ token }: StakeFormProps) => {
    const classes = useStyles()
    const { address: tokenAddress, name } = token
    const { account } = useEthers()

    const formattedTokenBalance: number = useGetFixFormattedTokenBalance(tokenAddress, account)
    // const formattedTokenBalance: number = (
    //     tokenBalance ?
    //         parseFloat(formatUnits(tokenBalance, 18)) :
    //         0
    // )
    const { chainId } = useEthers()
    const tokenFarmAddress = (chainId ?
        networkMapping[String(chainId)]["TokenFarm"][0] :
        constants.AddressZero
    )
    const tokenAllowance = useTokenAllowance(tokenAddress, account, tokenFarmAddress)

    const { notifications } = useNotifications()

    const [amount, setAmount] = useState<number | string | Array<number | string>>(0)

    const { approveAndStake, state: approveAndStakeErc20State } = useApproveAndStakeTokens(tokenAddress)
    const handleApproveAndStakeSubmit = () => {
        const amountAsWei = utils.parseEther(amount.toString())
        return approveAndStake(amountAsWei.toString())
    }

    const { approve, approveErc20State } = useApproveTokens(tokenAddress)
    const handleApproveSubmit = () => {
        const amountAsWei = utils.parseEther(amount.toString())
        return approve(amountAsWei.toString())
    }
    const handleApproveLimitlessSubmit = () => {
        const amountAsWei = constants.MaxUint256
        // console.log(amountAsWei.toHexString())
        return approve(amountAsWei.toString())
    }

    const { stake, stakeErc20State } = useStakeTokens(tokenAddress)
    const handleStakeSubmit = () => {
        const amountAsWei = utils.parseEther(amount.toString())
        return stake(amountAsWei.toString())
    }

    const isMining = (
        approveErc20State.status === "Mining" ||
        stakeErc20State.status === "Mining" ||
        approveAndStakeErc20State.status === "Mining"
    )

    // console.log(`Allowance: ${tokenAllowance ? BigNumber.from(tokenAllowance) : 0}`)
    // console.log(`amount   : ${amount ? utils.parseEther(amount.toString()) : 0}`)
    const isAllowance = amount ?
        (tokenAllowance ? tokenAllowance.gte(utils.parseEther(amount.toString())) : false) :
        true
    // console.log(`isAllowance: ${isAllowance}`)
    // const isAllowance = false
    const [showErc20ApprovalSuccess, setShowErc20ApprovalSuccess] = useState(false)
    const [showStakeSuccess, setShowStakeSuccess] = useState(false)
    const handleCloseSnack = () => {
        setShowErc20ApprovalSuccess(false)
        setShowStakeSuccess(false)
    }

    useEffect(() => {
        if (notifications.filter(
            (notifications) =>
                notifications.type === "transactionSucceed" &&
                notifications.transactionName === "Approve ERC20 transfer"
        ).length > 0) {
            console.log("Approved!")
            setShowErc20ApprovalSuccess(true)
            setShowStakeSuccess(false)
        }
        if (notifications.filter(
            (notifications) =>
                notifications.type === "transactionSucceed" &&
                notifications.transactionName === "Stake Tokens"
        ).length > 0) {
            console.log("Tokens Staked!")
            setShowErc20ApprovalSuccess(false)
            setShowStakeSuccess(true)
            setAmount(0)
        }
    }, [notifications, setShowErc20ApprovalSuccess, setShowStakeSuccess])

    const hasZeroBalance = formattedTokenBalance === 0
    const hasZeroAmountSelected = parseFloat(amount.toString()) === 0 || amount === ""
    return (
        <>
            <div className={classes.container}>
                <SliderInput
                    className={classes.slider}
                    lable={`Stake ${name}`}
                    maxValue={formattedTokenBalance}
                    id={`silder-input-${name}`}
                    value={amount}
                    onChange={setAmount}
                    disabled={isMining || hasZeroBalance}
                />
                {isAllowance ? (
                    <Button
                        onClick={handleStakeSubmit}
                        color="primary"
                        variant="contained"
                        size="large"
                        disabled={isMining || hasZeroAmountSelected}
                    >
                        {isMining ? <CircularProgress size={26} /> : "Stake!"}
                    </Button>
                ) : (
                    <>
                        <Button
                            onClick={handleApproveAndStakeSubmit}
                            color="primary"
                            variant="contained"
                            size="large"
                            disabled={isMining || hasZeroAmountSelected}
                        >
                            {isMining ? <CircularProgress size={26} /> : `Approve and Stake ${amount} ${name}`}
                        </Button>
                        <Button
                            onClick={handleApproveSubmit}
                            color="primary"
                            variant="contained"
                            size="large"
                            disabled={isMining || hasZeroAmountSelected}
                        >
                            {isMining ? <CircularProgress size={26} /> : `Approve ${amount} ${name}`}
                        </Button>
                        <Button
                            onClick={handleApproveLimitlessSubmit}
                            color="primary"
                            variant="contained"
                            size="large"
                            disabled={isMining || hasZeroAmountSelected}
                        >
                            {isMining ? <CircularProgress size={26} /> : "Approve Limitless!"}
                        </Button>
                    </>
                )
                }
            </div>
            <Snackbar
                open={showErc20ApprovalSuccess}
                autoHideDuration={3000}
                onClose={handleCloseSnack}
            >
                <Alert onClose={handleCloseSnack} severity="success">
                    ERC-20 token trasfer apporved! Now start stake!
                </Alert>
            </Snackbar>
            <Snackbar
                open={showStakeSuccess}
                autoHideDuration={3000}
                onClose={handleCloseSnack}
            >
                <Alert onClose={handleCloseSnack} severity="success">
                    Tokens Staked!
                </Alert>
            </Snackbar>
        </>
    )
}