# defi-tracker
Django application to track DeFi investments, all you need is the public keys!

Functionalities:
  - User accounts for personalized validators/wallets tracking
  - Ethereum and Solana account value (token and USD conversion) and sum functionality for entire tracked portfolio
    - To track a wallet's value, enter the wallet public key and a personalized display name
  - Interactive performance graph for Solana validator(s) (useful for staking investment decisions)
    - To track a validator performance, enter the vote account public key and a personalized display name
    - Validator performance metric is derived from Solana economic documentation, directly related to APY %
      - A "network-average" validator with 0% commission will yield performance metric of 1.0
      - The higher the performance metric, the better yield on tokens staked to that validator!

