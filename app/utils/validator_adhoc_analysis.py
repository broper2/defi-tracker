from app.adapters.validator.solana_validator import SolanaValidatorDataAdapter
from app.basetypes import DefiValidatorData
from app.config.constants import SOLANA_VALIDATOR_HISTORY_LENGTH
from app.external.solana_network import SolanaNetworkInterface


def get_top_validators(num_validators=5, num_epochs=5):
    # Find top 'num_validators' validator nodes by performance in past 'num_epochs' epochs
    # Not used in app, but useful tool
    num_epochs = min(num_epochs, SOLANA_VALIDATOR_HISTORY_LENGTH)
    interface = SolanaNetworkInterface()
    validators = [DefiValidatorData(key, None) for key in interface.vote_account_keys]
    adapter = SolanaValidatorDataAdapter(validators)
    sum_performances = [sum(x[0-num_epochs:len(x)]) for x in adapter.get_chart_data()]
    validators_and_performances = list(zip(validators, sum_performances))
    validators_and_performances.sort(key=lambda x: x[1], reverse=True)
    return [(v.key, perf/num_epochs) for v, perf in validators_and_performances[:num_validators]]

if __name__ == '__main__':
    from pprint import pprint
    pprint(get_top_validators())