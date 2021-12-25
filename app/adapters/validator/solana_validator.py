import numpy as np

from app.adapters.validator.base_validator import ValidatorAdapterBase
from app.external.solana_network import SolanaNetworkInterface


class SolanaValidatorDataAdapter(ValidatorAdapterBase):

    def __init__(self, tracked_validators):
        self.tracked_validators = tracked_validators
        self.solana_network_interface = SolanaNetworkInterface.instance()
        self.cluster_validator_data = self._get_cluster_validator_data()
        self.total_credits_per_epoch = self._get_total_credits_per_epoch()
        self.num_validators = len(self.cluster_validator_data)

    def get_chart_data(self):
        performances = []
        for validator in self.tracked_validators:
            validator_data = self._get_validator_data(validator.key)
            performances.append(self._get_validator_performance(validator_data))
        return performances

    def get_display_names(self):
        return [data.display_name for data in self.tracked_validators]

    def get_x_axis_labels(self):
        return [self.solana_network_interface.last_epoch + i for i in
                range(1 - self.solana_network_interface.epoch_credit_count, 1)]

    def _get_cluster_validator_data(self):
        return self.solana_network_interface.get_cluster_validator_data()

    def _get_total_credits_per_epoch(self):
        # Solana RPC getVoteAccount returns epoch credit data as [(epoch #, end credit balance, start credit balance),]
        epoch_credit_data = [
            np.array(self.solana_network_interface.get_epoch_credits(data)) for data in self.cluster_validator_data
        ]
        credit_delta = np.array([epoch_entry[:,1] - epoch_entry[:,2] for epoch_entry in epoch_credit_data])
        return credit_delta.sum(axis=0)

    def _get_validator_data(self, vote_pubkey):
        for validator_data in self.cluster_validator_data:
            if self.solana_network_interface.get_vote_pubkey(validator_data) == vote_pubkey:
                return validator_data

    def _get_validator_performance(self, validator_data):
        if not validator_data:
            return [0] * self.solana_network_interface.epoch_credit_count
        commission = self._get_commission(validator_data)
        credit_history = self._get_credit_history(validator_data)
        return self._apply_performance_formula(commission, credit_history)

    def _get_commission(self, data):
        return float(self.solana_network_interface.get_commission(data) / 100)

    def _get_credit_history(self, data):
        # Solana RPC getVoteAccount returns epoch credit data as [(epoch #, end credit balance, start credit balance),]
        return np.array(
            [epoch_entry[1] - epoch_entry[2] for epoch_entry in self.solana_network_interface.get_epoch_credits(data)]
        )

    def _apply_performance_formula(self, commission, credit_history):
        credit_share_per_epoch = credit_history / self.total_credits_per_epoch
        commission_based_performance = credit_share_per_epoch * (1 - commission)
        normalized_performance = commission_based_performance * self.num_validators
        return normalized_performance
