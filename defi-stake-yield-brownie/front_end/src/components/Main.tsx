import { useEthers } from "@usedapp/core"
// import { useConfig } from "@usedapp/core"
import helperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import { constants } from "ethers"
import brownieConfig from "../brownie-config.json"
import dapp from "../dapp.png"
import { YourWallet } from "./yourWallet"
import { makeStyles, Snackbar, Theme, ThemeProvider, Typography } from "@material-ui/core"
import { useEffect, useState } from "react"
import { Alert } from "@material-ui/lab"
import { TokenFarm } from "./tokenFarm"


export type Token = {
    image: string
    address: string
    name: string
}

const useStyles = makeStyles((theme: Theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4)
    }
}))

export const Main = () => {
    // Show token values from the wallet

    // Get the address of different tokens
    // Get the balance of the users wallet

    // send the brownie-config to our 'src' folder
    // send the build folder

    // Error: TS7053: Element implicitly has an 'any' type
    // because expression of type 'ChainId' can't be used to index type
    // tsconfig.json =>
    // "compilerOptions" => "suppressImplicitAnyIndexErrors": true
    // or
    // const helperConfigObj: { [key: string]: string } = helperConfig
    const classes = useStyles()
    const { chainId, error } = useEthers()
    const networkName = chainId ? helperConfig[chainId] : "development"
    // const { networks } = useConfig()
    // console.log(networks)
    console.log(chainId)
    console.log(networkName)

    // look into tha mapping
    const dappTokenAddress = (chainId ?
        networkMapping[String(chainId)]["DappToken"][0] :
        constants.AddressZero
    )
    const wethTokenAddress = (chainId ?
        brownieConfig["networks"][networkName]["weth_token"] :
        constants.AddressZero
    )
    const fauTokenAddress = (chainId ?
        brownieConfig["networks"][networkName]["fau_token"] :
        constants.AddressZero
    )
    const daiTokenAddress = (chainId ?
        brownieConfig["networks"][networkName]["dai_token"] :
        constants.AddressZero
    )
    const linkTokenAddress = (chainId ?
        brownieConfig["networks"][networkName]["link_token"] :
        constants.AddressZero
    )

    const supportedTokens: Array<Token> = [
        {
            image: dapp,
            address: dappTokenAddress,
            name: "DAPP"
        },
        {
            image: dapp,
            address: wethTokenAddress,
            name: "WETH"
        },
        {
            image: dapp,
            address: fauTokenAddress,
            name: "FUA"
        },
        {
            image: dapp,
            address: daiTokenAddress,
            name: "DAI"
        },
        {
            image: dapp,
            address: linkTokenAddress,
            name: "LINK"
        }
    ]

    const [showNetworkError, setShowNetworkError] = useState(false)

    const handleCloseNetworkError = (
        event: React.SyntheticEvent | React.MouseEvent,
        reason?: string
    ) => {
        if (reason === "clickaway") {
            return
        }

        showNetworkError && setShowNetworkError(false)
    }

    /**
     * useEthers will return a populated 'error' field when something has gone wrong.
     * We can inspect the name of this error and conditionally show a notification
     * that the user is connected to the wrong network.
     */
    useEffect(() => {
        // console.log("effect")
        if (error && error.name == "UnsupportedChainIdError") {
            // console.log(error)
            !showNetworkError && setShowNetworkError(true)
        } else {
            showNetworkError && setShowNetworkError(false)
        }
    }, [error, showNetworkError, setShowNetworkError])

    return (
        <>
            {/* <h1 className={classes.title}>Dapp Token Farm</h1> */}
            <Typography
                variant="h2"
                component="h1"
                classes={{ root: classes.title }}
            >
                Dapp Token Farm
            </Typography>
            <YourWallet supportedTokens={supportedTokens} />
            <TokenFarm supportedTokens={supportedTokens} />
            <Snackbar
                open={showNetworkError}
                autoHideDuration={5000}
                onClose={handleCloseNetworkError}
            >
                <Alert onClose={handleCloseNetworkError} severity="warning">
                    You gotta connect to the Kovan network!
                </Alert>
            </Snackbar>
        </>
    )
}