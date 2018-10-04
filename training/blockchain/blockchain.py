blockchain = []

def get_user_input():
    return float(input('Your transaction amount plz: '))

def add_value(transcation_amount, last_transcation=[1]):
    blockchain.append([last_transcation, transcation_amount])


def get_last_blockchain_value():
    return blockchain[-1]

tx_amount = get_user_input()
add_value(tx_amount)

tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

print(blockchain)
