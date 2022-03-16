import { Button, CircularProgress, Snackbar } from "@material-ui/core"
import { Token } from "../Main"
import { useGetStakeBalance, useUnstackTokens } from "../../hooks/useTokenFarm"
import { useEthers, useNotifications } from "@usedapp/core"
import { useEffect, useState } from "react"
import { Alert } from "@material-ui/lab"

interface UnstakeButtonProps {
    token: Token
}

export const UnstakeButton = ({ token }: UnstakeButtonProps) => {
    const { unstake, unstakeErc20State } = useUnstackTokens(token.address)
    const handleUnstakeSubmit = () => {
        return unstake()
    }

    const [showUnstakeSuccess, setShowUnstakeSuccess] = useState(false)
    const handleCloseSnack = () => {
        setShowUnstakeSuccess(false)
    }

    const { notifications } = useNotifications()
    useEffect(() => {
        if (notifications.filter(
            (notifications) =>
                notifications.type === "transactionSucceed" &&
                notifications.transactionName === "Unstake Tokens"
        ).length > 0) {
            console.log("Tokens Unstaked!")
            setShowUnstakeSuccess(true)
        }
    }, [notifications, setShowUnstakeSuccess])

    const isMining = unstakeErc20State.status === "Mining"
    const { account } = useEthers()
    const hasZeroAmountToStaked = useGetStakeBalance(token.address, account) <= 0
    return (
        <>
            <Button
                onClick={handleUnstakeSubmit}
                color="primary"
                variant="contained"
                size="large"
                disabled={isMining || hasZeroAmountToStaked}
            >
                {isMining ? <CircularProgress size={26} /> : `Unstack all ${token.name}`}
            </Button>
            <Snackbar
                open={showUnstakeSuccess}
                autoHideDuration={3000}
                onClose={handleCloseSnack}
            >
                <Alert onClose={handleCloseSnack} severity="success">
                    Tokens Unstaked!
                </Alert>
            </Snackbar>
        </>
    )
}