from app.config.constants import SOLANA_RPC_KEYS, ROUNDING_DECIMAL_PLACES


class SolanaValidatorWrapper(object):

    def __init__(self, data):
        self.activated_stake = data[SOLANA_RPC_KEYS['activated_stake']]
        self.commission = data[SOLANA_RPC_KEYS['commission']]
        self.epoch_credits = data[SOLANA_RPC_KEYS['epoch_credits']]
        self.epoch_vote_account = data[SOLANA_RPC_KEYS['epoch_vote_account']]
        self.node_pubkey = data[SOLANA_RPC_KEYS['node_pubkey']]
        self.root_slot = data[SOLANA_RPC_KEYS['root_slot']]
        self.vote_pubkey = data[SOLANA_RPC_KEYS['vote_pubkey']]

    def get_epoch_credit_history(self):
        # solana-py api gives below data for last 5 epochs
        #   (epoch #, end epoch credit, start epoch credit)
        history = []
        if self.epoch_credits:
            history = [round(epoch_entry[1] / epoch_entry[2], ROUNDING_DECIMAL_PLACES) for epoch_entry in
                       self.epoch_credits]
        return history

    def get_epoch_labels(self):
        # solana-py api gives below data for last 5 epochs
        #   (epoch #, end epoch credit, start epoch credit)
        labels = []
        if self.epoch_credits:
            labels = [epoch_entry[0] for epoch_entry in self.epoch_credits]
        return labels
