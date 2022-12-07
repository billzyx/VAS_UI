import re
import os
import yaml
from glob import glob
from datetime import datetime

config_path = 'config'
account_save_path = os.path.join(config_path, 'accounts')
session_save_path = os.path.join(config_path, 'sessions')
download_save_path = os.path.join(config_path, 'downloads')

os.makedirs(account_save_path, exist_ok=True)
os.makedirs(session_save_path, exist_ok=True)


def account_to_profile(account):
    return re.sub(r'[^a-zA-Z0-9]', '_', account)


def get_account_path(account):
    return os.path.join(account_save_path, '{}.yaml'.format(account_to_profile(account)))


def save_account(account, password, save_dir, device, device_list):
    account_dict = {
        'account': account,
        'password': password,
        'save_dir': save_dir,
        'profile': account_to_profile(account),
        'device': None,
        'device_list': device_list,
    }

    if not device == 'All':
        account_dict['device'] = device
    with open(get_account_path(account), 'w') as f:
        yaml.dump(account_dict, f)


def check_account_exist(account):
    if os.path.isfile(get_account_path(account)):
        return True
    return False


def load_account(account):
    if not check_account_exist(account):
        return None
    with open(get_account_path(account), 'r') as f:
        return yaml.safe_load(f)


def delete_account(account):
    if os.path.exists(get_account_path(account)):
        os.remove(get_account_path(account))


def load_accounts():
    account_path_list = glob(os.path.join(account_save_path, '*.yaml'))
    account_list = []
    for account_path in account_path_list:
        with open(account_path, 'r') as f:
            account_list.append(yaml.safe_load(f))
    return account_list


def get_session_path(session_name):
    return os.path.join(session_save_path, '{}.yaml'.format(session_name))


def save_session(session_name, date_from, date_to, time_from, time_to, save_date_time, save_device_name):
    session_dict = {
        "session_name": session_name,
        "reverse": True,
        "date_from": date_from,
        "date_to": date_to,
        "time_from": time_from,
        "time_to": time_to,
        'save_date_time': save_date_time,
        'save_device_name': save_device_name,
    }
    with open(get_session_path(session_name), 'w') as f:
        yaml.dump(session_dict, f)


def check_session_exist(session):
    if os.path.isfile(get_session_path(session)):
        return True
    return False

def load_session(session):
    if not check_session_exist(session):
        return None
    with open(get_session_path(session), 'r') as f:
        return yaml.safe_load(f)


def delete_session(session):
    if os.path.exists(get_session_path(session)):
        os.remove(get_session_path(session))


def load_sessions():
    session_path_list = glob(os.path.join(session_save_path, '*.yaml'))
    session_list = []
    for session_path in session_path_list:
        with open(session_path, 'r') as f:
            session_list.append(yaml.safe_load(f))
    return session_list


def generate_download_configs(account_list, session_list):
    download_save_path_current = os.path.join(
        download_save_path, str(datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-'))
    os.makedirs(download_save_path_current)
    config_file_path_list = []
    for account in account_list:
        for session in session_list:
            session = session.copy()
            profile = account['profile']
            session_name = session['session_name']
            file_name = '{}-{}'.format(profile, session_name)
            session['session_name'] = '{}_{}'.format(profile, session_name)
            session.update(account)
            config_file = os.path.join(download_save_path_current, '{}.yaml'.format(file_name))
            config_file_path_list.append(config_file)
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(session, f)
    return config_file_path_list


def check_downloading_exist(config_file_path_list):
    for config_file_path in config_file_path_list:
        with open(config_file_path, 'r') as f:
            config = yaml.safe_load(f)
            if os.path.isdir(os.path.join(config['save_dir'], config['session_name'])):
                return False
    return True



if __name__ == '__main__':
    print(load_accounts())
    print(load_sessions())

