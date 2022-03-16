import { useConfig, useEthers } from "@usedapp/core"
import { Button, makeStyles, Snackbar, Theme } from "@material-ui/core"
import copy from "copy-to-clipboard"
import { Alert } from "@material-ui/lab"
import { useState } from "react"

const useStyles = makeStyles((theme: Theme) => ({
    container: {
        padding: theme.spacing(4),
        display: "flex",
        justifyContent: "flex-end",
        gap: theme.spacing(1)
    }
}))

export const Header = () => {
    const { account, activateBrowserWallet, deactivate, chainId } = useEthers()
    // const { networks } = useConfig()
    // const supportedChainIds = networks?.map((network) => network.chainId)
    // // console.log("supportedChainIds")
    // // console.log(supportedChainIds?.indexOf(chainId ? chainId : 88888))
    // if (chainId && supportedChainIds?.indexOf(chainId) && supportedChainIds?.indexOf(chainId) < 0) {
    //     console.log("chain error")
    //     deactivate()
    // }

    const classes = useStyles()

    const isConnected = account !== undefined

    const [showCopySuccess, setShowCopySuccess] = useState(false)
    const handleSnakeClose = (event: React.SyntheticEvent | React.MouseEvent) => {
        showCopySuccess && setShowCopySuccess(false)
    }

    const handleAccountClick = () => {
        copy(account ? account : "")
        !showCopySuccess && setShowCopySuccess(true)
    }

    return (
        <div className={classes.container}>
            {isConnected ? (
                <>
                    <Button color="primary" variant="contained" onClick={handleAccountClick}>
                        {`${account?.slice(0, 4)}...${account?.slice(-3)}`}
                    </Button>
                    <Button variant="contained" onClick={deactivate}>
                        Disconnect
                    </Button>
                    <Snackbar
                        open={showCopySuccess}
                        autoHideDuration={1000}
                        onClose={handleSnakeClose}
                        anchorOrigin={{
                            vertical: 'top',
                            horizontal: 'center'
                        }}
                    >
                        <Alert onClose={handleSnakeClose} severity="success">
                            Copied!
                        </Alert>
                    </Snackbar>
                </>
            ) : (
                <Button
                    color="primary"
                    variant="contained"
                    onClick={() => activateBrowserWallet()}
                >
                    Connect
                </Button>
            )
            }
        </div>
    )
}