import { Box, Tab, Theme } from "@material-ui/core";
import { TabContext, TabList, TabPanel } from "@material-ui/lab";
import { makeStyles } from "@material-ui/core";
import React, { useState } from "react";
import { Token } from "../Main";
import { StakeBalance } from "./StakeBalance";
import { UnstakeButton } from "./UnStakeButton";


const useStyles = makeStyles((theme: Theme) => ({
    tabContent: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: theme.spacing(4)
    },
    box: {
        backgroundColor: "white",
        borderRadius: "25px",
    },
    header: {
        color: "white"
    }
}))

interface TokenFarmProps {
    supportedTokens: Array<Token>
}

export const TokenFarm = ({ supportedTokens }: TokenFarmProps) => {
    const classes = useStyles()
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)

    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue))
    }

    return (
        <Box>
            <h1 className={classes.header}>The TokenFarm Contract</h1>
            <Box className={classes.box}>
                <TabContext value={selectedTokenIndex.toString()}>
                    <TabList onChange={handleChange} aria-label="unstake from tabs">
                        {supportedTokens.map((token, index) => {
                            return (
                                < Tab label={token.name}
                                    value={index.toString()}
                                    key={index}
                                />
                            )
                        })}
                    </TabList>
                    {supportedTokens.map((token, index) => {
                        return (
                            <TabPanel value={index.toString()}
                                key={index}>
                                <div className={classes.tabContent}>
                                    <StakeBalance token={supportedTokens[selectedTokenIndex]} />
                                    <UnstakeButton token={supportedTokens[selectedTokenIndex]} />
                                </div>
                            </TabPanel>
                        )
                    })}
                </TabContext>
            </Box>
        </Box>
    )
}