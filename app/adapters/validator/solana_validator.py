import numpy as np

from app.config.constants import SOLANA_RPC_KEYS, SOLANA_VALIDATOR_HISTORY_LENGTH
from app.external.solana_network import SolanaNetworkInterface


class SolanaValidatorDataAdapter(object):

    def __init__(self, tracked_validators):
        self.tracked_validators = tracked_validators
        self.solana_network_interface = SolanaNetworkInterface.instance()
        self.validator_network_data = self._get_validator_network_data()
        self.total_credits_per_epoch = self._get_total_credits_per_epoch()
        self.num_validators = len(self.validator_network_data)

    def get_validator_performances(self):
        performances = []
        for validator in self.tracked_validators:
            validator_data = self._get_validator_data(validator.key)
            performances.append(self._get_validator_performance(validator_data))
        return performances

    def get_display_names(self):
        return [data.display_name for data in self.tracked_validators]

    def get_epochs(self):
        return [self.solana_network_interface.last_epoch + i for i in range(1-SOLANA_VALIDATOR_HISTORY_LENGTH, 1)]

    def _get_validator_network_data(self):
        cluster_data = self.solana_network_interface.get_validator_data()
        for validator_data in cluster_data:
            validator_data[SOLANA_RPC_KEYS['epoch_credits']] = self._normalize_history_length(
                validator_data[SOLANA_RPC_KEYS['epoch_credits']]
            )
        return cluster_data

    def _get_total_credits_per_epoch(self):
        # Solana RPC getVoteAccount returns epoch credit data as [(epoch #, end credit balance, start credit balance),]
        epoch_credit_data = [np.array(data[SOLANA_RPC_KEYS['epoch_credits']]) for data in self.validator_network_data]
        credit_delta = np.array([epoch_entry[:,1] - epoch_entry[:,2] for epoch_entry in epoch_credit_data])
        return credit_delta.sum(axis=0)

    @staticmethod
    def _normalize_history_length(history):
        return [[0, 0, 0]] * (SOLANA_VALIDATOR_HISTORY_LENGTH - len(history)) + history

    def _get_validator_data(self, vote_pubkey):
        for validator_data in self.validator_network_data:
            if validator_data[SOLANA_RPC_KEYS['vote_pubkey']] == vote_pubkey:
                return validator_data

    def _get_validator_performance(self, validator_data):
        if not validator_data:
            return [0] * SOLANA_VALIDATOR_HISTORY_LENGTH
        commission = self._get_commission(validator_data)
        credit_history = self._get_credit_history(validator_data)
        return self._apply_performance_formula(commission, credit_history)

    @staticmethod
    def _get_commission(data):
        return float(data[SOLANA_RPC_KEYS['commission']] / 100)

    @staticmethod
    def _get_credit_history(data):
        # Solana RPC getVoteAccount returns epoch credit data as [(epoch #, end credit balance, start credit balance),]
        return np.array([epoch_entry[1] - epoch_entry[2] for epoch_entry in data[SOLANA_RPC_KEYS['epoch_credits']]])

    def _apply_performance_formula(self, commission, credit_history):
        credit_share_per_epoch = credit_history / self.total_credits_per_epoch
        commission_based_performance = credit_share_per_epoch * (1 - commission)
        normalized_performance = commission_based_performance * self.num_validators
        return normalized_performance
