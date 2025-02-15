import requests

def get_tron_transaction(tx_hash):
    url = f"https://apilist.tronscanapi.com/api/transaction-info?hash={tx_hash}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        token_transfers = data.get("tokenTransferInfo", {})
        to_address = token_transfers.get("to_address", "Не найдено")
        amount = token_transfers.get("amount_str", "Не найдено")
        return f"Адрес получателя: {to_address}, Сумма: {amount}"
    else:
        return f"Ошибка: {response.status_code}, {response.text}"

# Хеш транзакции
transaction_hash = "306fc7cad14571ef0b7d180f5a7b59af209823577c915fe40bec8068f581835b"

# Получаем данные
transaction_data = get_tron_transaction(transaction_hash)
print(transaction_data)
