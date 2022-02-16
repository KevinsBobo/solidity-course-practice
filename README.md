https://github.com/smartcontractkit/full-blockchain-solidity-course-py
https://www.youtube.com/watch?v=M576WGiDBdQ

```bash
brownie networks add Ethereum ganache-local host=http://127.0.0.1:7545 chainid=5777
brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://mainnet.infura.io/v3/$WEB3_INFURA_PROJECT_ID' accounts=10 mnemonic=brownie port=8545
# you can also get $WEB3_INFURA_PROJECT_ID form alchemyapi.io
```
