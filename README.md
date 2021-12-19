# solana-tracker
Django application to track Solana investments, all you need is the public keys!

Functionalities:
  - User accounts for custom validators/wallets tracking
  - Validator(s) performance interactive graph (useful for staking investment decisions)
    - To track a validator performance, enter the vote account public key and a personalized display name
    - Validator performance metric is based on Solana economics, directly related to APY %
      - A "network-average" validator with 0% commission will yield performance metric of 1.0
      - The higher the performance metric, the better yield on tokens staked to that validator!
  - Wallet token value, with up-to-date USD conversion, and sum functionality for entire tracked portfolio
    - To track a wallet's value, enter the wallet public key and a personalized display name
