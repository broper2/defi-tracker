from app.adapters.validator import solana_validator


def get_validator_adapter(network_name, *args, **kwargs):
    validator_adapter_cls_map = {
        'SOLANA': solana_validator.SolanaValidatorDataAdapter
    }
    validator_cls = validator_adapter_cls_map[network_name.upper()]
    return validator_cls(*args, **kwargs)