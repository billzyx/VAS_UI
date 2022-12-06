import re
import os
import yaml
from glob import glob

config_path = 'config'
account_save_path = os.path.join(config_path, 'accounts')
session_save_path = os.path.join(config_path, 'sessions')

os.makedirs(account_save_path, exist_ok=True)
os.makedirs(session_save_path, exist_ok=True)


def account_to_profile(account):
    return re.sub(r'[^a-zA-Z0-9]', '_', account)


def get_account_path(account):
    return os.path.join(account_save_path, '{}.yaml'.format(account_to_profile(account)))


def save_account(account, password, save_dir, device):
    account_dict = {
        'account': account,
        'password': password,
        'save_dir': save_dir,
        'profile': account_to_profile(account)
    }

    if not device == 'All':
        account_dict['device'] = device
    with open(get_account_path(account), 'w') as f:
        yaml.dump(account_dict, f)


def check_account_exist(account):
    if os.path.isfile(get_account_path(account)):
        return True
    return False


def load_accounts():
    account_path_list = glob(os.path.join(account_save_path, '*.yaml'))
    account_list = []
    for account_path in account_path_list:
        with open(account_path, 'r') as f:
            account_list.append(yaml.safe_load(f))
    return account_list


if __name__ == '__main__':
    print(load_accounts())

