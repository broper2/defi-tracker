from app.models import DefiValidator, DefiWallet


def get_validator_records(user_id, network):
    return DefiValidator.objects.filter(user_id=user_id, defi_network=network)


def get_wallet_records(current_user_id, network):
    return DefiWallet.objects.filter(user_id=current_user_id, defi_network=network)


def get_model_by_pk(model_cls, pk):
    model_query = model_cls.objects.filter(pk=pk)
    return model_query[0] if model_query else None


def get_form_error_message(error_dict):
    error_messages = []
    if error_dict:
        validation_errors = error_dict.as_data()['__all__']
        for error in validation_errors:
            error_messages.append(error.message)
    return error_messages
