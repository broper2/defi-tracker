# solana-tracker
Django application to track Solana investments, all you need is the public key!

Functionalities:
  - User accounts for custom validators/wallets tracking
  - Validator(s) performance graph for staked tokens
    - To track a validator performance, enter the vote account public key and a personalized display name
    - Validator performance is measured in credit return rate by epoch
  - Wallet token value, with up-to-date USD conversion, and sum functionality for entire tracked portfolio
    - To track a wallet's value, enter the wallet public key and a personalized display name
