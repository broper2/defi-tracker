from app.config.constants import SOLANA_RPC_KEYS
from app.utils.rounding import round_sol


class SolanaValidatorDataAdapter(object):

    def __init__(self, display_name, data):
        self.display_name = display_name
        self.epoch_credits = data[SOLANA_RPC_KEYS['epoch_credits']]
        self.vote_pubkey = data[SOLANA_RPC_KEYS['vote_pubkey']]

    def get_epoch_credit_history(self):
        # solana-py api gives below data for last 5 epochs
        #   (epoch #, end epoch credit, start epoch credit)
        history = []
        if self.epoch_credits:
            history = [round_sol(epoch_entry[1] / epoch_entry[2]) for epoch_entry in self.epoch_credits]
        return history

    def get_epoch_labels(self):
        # solana-py api gives below data for last 5 epochs
        #   (epoch #, end epoch credit, start epoch credit)
        labels = []
        if self.epoch_credits:
            labels = [epoch_entry[0] for epoch_entry in self.epoch_credits]
        return labels
