from fastapi import FastAPI
from app.models import Client, Transaction
from app.database import add_client as add_client_to_db
from app.database import get_client_balance as get_client_balance_from_db
from app.database import update_client_balance as update_client_balance_in_db
from app.database import add_to_balance as add_to_balance_db
from typing import Union
import os
from pathlib import Path
from .logging_tools.logger import Logger

# Initialize API app object
app = FastAPI()

# Initialize Logger for the app
current_directory = Path(__file__).parent.absolute()
log_file_path = os.path.join(current_directory, 'logging_tools/log_files/logs.log')
logger = Logger(module_name='app_logger', log_file_path=log_file_path)


@app.get("/")
def check_app():  # checks that API works

    return {"message": "It works fine :)"}


@app.post('/add_client/')
def add_client(client: Client):
    """
    Add new Client to the DB
    """

    # Get all client's details
    client_name = client.name
    client_balance = client.balance

    # Log current action
    logger.log(f'Trying to add client with name = {client_name} and balance = {client_balance}', level='info')

    # Try to add client to the db
    result = add_client_to_db(client_name, client_balance)

    output = {
        'status': 200,
        'message': ''
    }

    # Change output to success status
    success_message = f'Client was created successfully, id of the client={result}'
    if result is not None:
        output['message'] = success_message

    # Log successful status
    logger.log(success_message, level='info')

    return output


@app.get('/get_client_balance/')
def get_client_balance(client_id: int):
    """
    Gets balance of the client be client's Id
    :param client_id: Id of the client
    """

    # Structure of JSON output
    output = {
        'status': 200,
        'message': '',
        'client_id': client_id,
        'balance': None
    }

    # Try to get client's balance
    balance = None
    try:
        balance = get_client_balance_from_db(client_id)

    # Handle Error of multiple clients rows
    except ValueError:
        output['message'] = 'Request to clients table returned more than 1 row'
        return output

    # If client with such client's id was not found
    if balance is None:
        output['message'] = f'No client with client_id={client_id} in clients table'
    else:
        output['message'] = f'Client with client_id={client_id} was found in clients table'
        output['balance'] = balance

    return output


@app.post('/update_client_balance/')
def update_client_balance(client_id: int, new_balance: float):
    """
    Updates client's balance
    :param client_id:
    :param new_balance:
    :return:
    """

    # Structure of JSON output
    output = {
        'status': 200,
        'message': '',
    }

    # Log current operation
    logger.log(f'Trying to update client balance, client_id={client_id}, new_balance={new_balance}', level='info')

    # Changes client's balance in the Db Table
    result = update_client_balance_in_db(client_id, new_balance)

    # Fill JSON output message
    if result is None:
        output['message'] = f'There is no client with client_id={client_id}'
        logger.log(f'There is no client with client_id={client_id}', level='error')
    else:
        output['message'] = "Client's balance was successfully changed"
        logger.log(f"Client's balance with client_id={client_id} was successfully changed", level='info')

    return output


@app.post('/perform_transaction/')
def perform_transaction(transaction: Transaction):
    # Get parameters of Transaction
    first_client_id = transaction.first_client_id
    second_client_id = transaction.second_client_id
    amount = transaction.amount
    first_client_balance, second_client_balance = None, None

    output = {
        'status': 200,
        'message': ''
    }

    # Get first client balance
    try:
        first_client_balance = get_client_balance_from_db(first_client_id)
    except ValueError:
        output['message'] = f'No client with client_id={first_client_id}'
        logger.log(f'There is no client with client_id={first_client_id}', level='error')
        return output

    if first_client_balance is None:
        output['message'] = f'No client with client_id={first_client_id}'
        logger.log(f'There is no client with client_id={first_client_id}', level='error')
        return output

    # Get second client balance
    try:
        second_client_balance = get_client_balance_from_db(second_client_id)
    except ValueError:
        output['message'] = f'No client with client_id={second_client_id}'
        logger.log(f'There is no client with client_id={second_client_id}', level='error')
        return output

    if second_client_balance is None:
        output['message'] = f'No client with client_id={second_client_id}'
        logger.log(f'There is no client with client_id={second_client_id}', level='error')
        return output

    # Check if transaction could be performed
    if first_client_balance - amount < 0:
        output['status'] = 400
        output['message'] = f'Negative balance for client with client_id={first_client_id}'
        logger.log(f'Negative balance for client with client_id={first_client_id}', level='error')
    else:
        # Take amount from the first client's balance
        add_to_balance_db(first_client_id, amount, negative=True)

        # Add sum to the second client's balance
        add_to_balance_db(second_client_id, amount)

        # Change output massage and log the result
        output['message'] = f'Transaction with client_id={first_client_id} and client_id={second_client_id} ' \
                            f'was performed successfully'
        logger.log(f'Transaction with client_id={first_client_id} and client_id={second_client_id} was performed successfully', level='info')

    return output
