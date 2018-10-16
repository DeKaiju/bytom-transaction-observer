# -*- coding: utf-8 -*
import time
import requests
import argparse

host = 'https://blockmeta.com/api/v2'
transaction_count = None
unconfirmed_transactions = list()


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', required=True, help='wallet address')
    parser.add_argument('-c', required=False, default=10, help='transaction confirmation')
    parser.add_argument('-i', required=False, default=60, help='request interval')
    args = parser.parse_args()
    return args.a, int(args.c), int(args.i)


def get_transactions(_address):
    global transaction_count
    url = '{host}/address/{address}'.format(host=host, address=_address)
    result = requests.get(url).json()
    _transaction_count = result.get('transaction_count')
    _transactions = result.get('transactions')
    if transaction_count is None:
        transaction_count = _transaction_count
    else:
        difference = _transaction_count - transaction_count
        transaction_count = _transaction_count
        if difference > 0:
            handle_transactions(_transactions[0:difference])


def handle_transactions(_transactions):
    _transactions.reverse()
    for transaction in _transactions:
        transaction_id = transaction.get('id')
        unconfirmed_transactions.append(transaction_id)
        print(transaction_id, 'save')  # TODO 调用api向数据库存储数据
        # Warning
        # 这里获取到的transaction是地址下最新的交易，但是因为区块链可能分叉，这笔交易所在的区块可能成为孤块，即这笔交易失效没有上链
        # 所以需要轮询查询交易的confirmations进行确认 建议confirmations>=10认为这笔交易上链有效
        # 查询交易confirmations的api https://blockmeta.com/api/v2/transaction/{transaction_id}


def confirm_transactions(_confirmation):
    for transaction_id in unconfirmed_transactions:
        url = '{host}/transaction/{transaction_id}'.format(host=host, transaction_id=transaction_id)
        response = requests.get(url)
        status_code = response.status_code
        if status_code != 200:
            print(transaction_id, 'invalid')  # TODO 调用api将数据库交易标记为无效
            unconfirmed_transactions.remove(transaction_id)
        else:
            if response.json().get('confirmations') < _confirmation: break
            print(transaction_id, 'valid')  # TODO 调用api将数据库交易标记为有效
            unconfirmed_transactions.remove(transaction_id)


if __name__ == '__main__':
    address, confirmation, interval = get_argument()
    while True:
        get_transactions(address)
        confirm_transactions(confirmation)
        time.sleep(interval)
