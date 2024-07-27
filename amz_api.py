import requests, json, os
from dotenv import load_dotenv
import datetime

def get_access_token(client_id, client_secret, refresh_token):
    '''
    Retrieves a new access token using the provided client ID, client secret, and refresh token.

    Parameters:
    - client_id (str): The client ID associated with the application.
    - client_secret (str): The client secret associated with the application.
    - refresh_token (str): The refresh token used for obtaining a new access token.

    Returns:
    - str: The access token obtained from the token endpoint.

    Example:
    getAccessToken('your_client_id', 'your_client_secret', 'your_refresh_token')

    Note: Access token valid for 60 mins
    '''
    # OAuth2 token endpoint
    token_url = 'https://api.amazon.com/auth/o2/token'

    #data needed to get access token
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    # print("Connecting to Amazon... ")

    try: 
        # Make a POST request to retrieve the access token
        response = requests.post(token_url, data=data)
        response.raise_for_status()  # Raise an error for non-200 status codes

        # Get the access token from the response
        access_token = response.json()['access_token']
        #print("Access token:", access_token)

    except Exception as e:
        print("[X] Could not retrive AMZ access token")
        print(f"Error: {e}")
        access_token = None

    return access_token

def get_order_info(orderID, access_token):
    '''
    Retrieves information about a specific order from the Amazon Selling Partner API.

    Parameters:
    - orderID (str): The unique identifier of the order.
    - access_token (str): The access token used for authentication.

    Returns:
    - dict: A dictionary containing information about the order retrieved from the API.

    Example:
    getOrderInfo('your_order_id', 'your_access_token')
    '''

    # Parameter type error handling
    if not isinstance(orderID, str) or not isinstance(access_token, str):
        raise TypeError("OrderID and access_token must be of type str.")


    #endpoint for used for getting orders
    uri_endpoint = f'https://sellingpartnerapi-na.amazon.com/orders/v0/orders/'

    #give the unique order number in the URL query
    url = uri_endpoint + orderID
    

    headers = {
        'user-agent' : "Shipstation Automation/1.0 (Language=Python/3.11.6)",  
        'x-amz-access-token': access_token,
        'content-type': 'application/json'
    }
    try: 
        # Get order information
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an error for non-200 status codes

        response_json = response.json()

        #some debug stuff
        #pretty_json = json.dumps(response_json, indent=4)
        #print(pretty_json)

    except Exception as e:
        print("[X] Could not retrieve order info json")
        print(f"Error: {e}")
        response_json = None

    return response_json, response

def get_api_keys(store_ID):
    '''

    '''
    # Load API keys from .env file
    load_dotenv()
    try:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        refresh_token = os.getenv("REFFRESH_TOKEN")
    

    except Exception as e:
        raise Exception 
    
    return client_id, client_secret, refresh_token




if __name__ == '__main__':
    pass