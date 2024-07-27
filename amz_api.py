import requests, os
from dotenv import load_dotenv


def get_api_keys(store_ID):
    """
    Retrieve API keys from a .env file.

    This function loads the environment variables from a .env file and retrieves the CLIENT_ID, CLIENT_SECRET, 
    and REFFRESH_TOKEN required for API access. If there is an issue loading the environment variables, 
    an exception is raised.

    Parameters:
    store_ID (str): The identifier for the store. (Currently not used in the function, but can be 
                    utilized in future versions if needed.)

    Returns:
    tuple: A tuple containing three elements:
        - client_id (str): The client ID for the API.
        - client_secret (str): The client secret for the API.
        - refresh_token (str): The refresh token for the API.

    Raises:
    Exception: If there is an error loading the environment variables.
    """
    load_dotenv()
    try:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        refresh_token = os.getenv("REFFRESH_TOKEN")
    

    except Exception as e:
        raise Exception 
    
    return client_id, client_secret, refresh_token


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

def get_order_info( access_token):
    '''

    '''

    #endpoint for used for getting orders
    uri_endpoint = f''
    
    url = ""

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
        print("[X] Could not retrieve data from Amazon")
        print(f"Error: {e}")
        response_json = None

    return response_json, response


def fetch_amazon_data():
    client_id, client_secret, refresh_token = get_api_keys()

    access_token = get_access_token(client_id, client_secret, refresh_token)

    


if __name__ == '__main__':
    pass