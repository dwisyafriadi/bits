import requests
import time

# Define the API URLs
auth_url = "https://api-bits.apps-tonbox.me/api/v1/auth"
start_task_url = "https://api-bits.apps-tonbox.me/api/v1/socialtask/start?access_token={access_token}"
fetch_url = "https://api-bits.apps-tonbox.me/api/v1/socialtasks?access_token={access_token}"
claim_url = "https://api-bits.apps-tonbox.me/api/v1/socialtask/claim?access_token={access_token}"
daily_reward_url = "https://api-bits.apps-tonbox.me/api/v1/daily-reward?access_token={access_token}"
auto_trading_url = "https://api-bits.apps-tonbox.me/api/v1/passive?access_token={access_token}"
balance_url = "https://api-bits.apps-tonbox.me/api/v1/balance?access_token={access_token}"

# Read data from query.txt
def read_query_data():
    try:
        with open('query.txt', 'r') as file:
            data = [line.strip() for line in file.readlines()]  # Read all lines and strip whitespace
            return data
    except FileNotFoundError:
        print("Error: query.txt file not found.")
        return None

# Authenticate and obtain token
def authenticate(query_data):
    payload = {
        "data": query_data,
        "device": "Windows"
    }

    try:
        response = requests.post(auth_url, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data['token']  # Return the token
    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return None

# Timer method for cooldown
def timer(hours):
    total_seconds = hours * 3600  # Convert hours to seconds
    while total_seconds > 0:
        # Calculate hours, minutes, and seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Cooldown: {hours:02}:{minutes:02}:{seconds:02}", end='\r')  # Print countdown
        time.sleep(1)  # Wait for 1 second
        total_seconds -= 1
    print("Cooldown complete!")

# Get the access token for further API calls
query_data_list = read_query_data()
if query_data_list is None:
    raise SystemExit("Exiting due to missing query data.")

# Process each query in the list
for query_data in query_data_list:
    print(f"Processing query: {query_data}")  # Indicate the current query being processed
    access_token = authenticate(query_data)
    if access_token is None:
        raise SystemExit("Exiting due to authentication failure.")

    # Define headers with the new access token
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'app-token': 'Ct9uHfSMp8CKZpfiCt1yog',
        'connection': 'keep-alive',
        'host': 'api-bits.apps-tonbox.me',
        'origin': 'https://bits.apps-tonbox.me',
        'referer': 'https://bits.apps-tonbox.me/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sid': 'ee6eed78-b06e-40eb-bda2-d50176ab5a89',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

    # Update URLs with the access token
    fetch_url = fetch_url.format(access_token=access_token)
    claim_url = claim_url.format(access_token=access_token)
    daily_reward_url = daily_reward_url.format(access_token=access_token)
    auto_trading_url = auto_trading_url.format(access_token=access_token)
    balance_url = balance_url.format(access_token=access_token)
    start_task_url = start_task_url.format(access_token=access_token)

    def start_task(task_name):
        payload = {
            "access_token": access_token,
            "name": task_name,
            "adId": None  # Assuming adId can be None
        }
        
        try:
            response = requests.post(start_task_url, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            
            # Print the raw response content for debugging
            print(f"Response from start task API: {response.text}")

            result = response.json()
            if result is True:
                print(f"Started task: {task_name} successfully.")
                return True
            else:
                print(f"Failed to start task: {task_name}. Response: {result}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error starting task: {e}")
            return False

    def fetch_tasks():
        try:
            response = requests.get(fetch_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Return the response JSON
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tasks: {e}")
            return None

    def claim_task(task_name):
        payload = {
            "access_token": access_token,
            "name": task_name
        }
        
        try:
            response = requests.post(claim_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            
            # Check if the claim was successful
            if data and isinstance(data, list) and len(data) > 0:
                print(f"Claimed task: {task_name}, Response: {data}")
                check_balance()  # Check balance after claiming the task
            else:
                print(f"Failed to claim task: {task_name}. Response: {data}")
        except requests.exceptions.RequestException as e:
            print(f"Error claiming task: {e}")

    def check_balance():
        try:
            response = requests.get(balance_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            print(f"Balance: {data['coins']}, Total Rewards Income: {data['totalRewardsIncome']}, Total Tasks Income: {data['totalTasksIncome']}, Total Invites Income: {data['totalInvitesIncome']}")
        except requests.exceptions.RequestException as e:
            print(f"Error checking balance: {e}")

    def auto_claim_daily():
        payload = {
            "access_token": access_token
        }
        
        try:
            response = requests.post(daily_reward_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            print(f"Claimed daily reward, Response: {data}")
        except requests.exceptions.RequestException as e:
            print(f"Error claiming daily reward: {e}")

    def auto_trading():
        payload = {
            "access_token": access_token
        }
        
        try:
            response = requests.post(auto_trading_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            print(f"Auto trading status: {data}")
        except requests.exceptions.RequestException as e:
            print(f"Error in auto trading: {e}")

    # Main processing loop for the current query
    tasks = fetch_tasks()
    if tasks:
        for item in tasks:
            social_task = item['socialTask']
            if item['status'] == 'None':  # Check if the task is not claimed
                if start_task(social_task['name']):
                    claim_task(social_task['name'])

# Cooldown timer for 24 hours
print("All processes complete. Starting cooldown for 24 hours...")
timer(24)

if __name__ == "__main__":
    main()
