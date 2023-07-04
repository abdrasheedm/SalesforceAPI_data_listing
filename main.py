import requests


''' Salesforce Domain '''

DOMAIN = 'https://aidetic2-dev-ed.develop.my.salesforce.com'


''' Function for getting Access Token from saved file '''

def get_access_token():
    try:
        with open('access_token.txt', 'r') as file:
            access_token = file.read()
        return access_token

    except FileNotFoundError:
        raise Exception('There is no \'access_token.txt\' file in your directory')
    except IOError:
        raise Exception("File can't be accessed")
    


''' Function for generating new Access Token using refresh token '''

def get_refreshed_access_token():
    try:
        with open('refresh_token.txt', 'r') as file:
            refresh_token = file.read()
    except:
        raise Exception("There is no \'refresh_token.txt\' in your directory")
    
    try:
        with open('consumer_key.txt', 'r') as file:
            consumer_key = file.read()
    except:
        raise Exception("There is no \'consumer_key.txt\' file in your directory")
    
    try:
        with open('consumer_secret.txt', 'r') as file:
            consumer_secret = file.read()
    except:
        raise Exception("There is no \'consumer_secret.txt\' file in your directory")
    

    if refresh_token and consumer_key and consumer_secret:
        host = 'https://login.salesforce.com'
        api_endpoint = '/services/oauth2/token'
        params = {
            'grant_type' : 'refresh_token',
            'client_id' : consumer_key,
            'client_secret' : consumer_secret,
            'refresh_token' : refresh_token

        }

        url = f"{host}{api_endpoint}"

        response = requests.post(url=url, params=params)
        if response.status_code == 200:
            new_access_token = response.json()['access_token']

            # Storing access token to file
            text_file = open("access_token.txt", "w")  
            text_file.write(new_access_token)
            text_file.close()



            return f'Your new access token is {new_access_token}'
        else:
            return response.json()
    
    return 'Please provide all mandatory params'

    

''' Function to generate header '''

def get_headers(access_token):
    headers = {
        "Authorization" : f"Bearer {access_token}"
    }
    return headers


''' Function to list all Accounts data with filter option '''

def get_accounts(token, id = None, AccountNumber = None, Name = None, created_on = None, created_before = None, created_after = None):
    api_endpoint = f'/services/data/v58.0/query'
    headers = get_headers(token)
    query_fields = "Id, Name, BillingAddress, ShippingAddress, Phone, AccountNumber, CreatedDate"

    where_conditions = []
    if Name:
        where_conditions.append(f"Name = \'{Name}\'")
    if id:
        where_conditions.append(f"Id = \'{id}\'")
    if AccountNumber:
        where_conditions.append(f"AccountNumber = \'{AccountNumber}\'")
    if created_on:
        where_conditions.append(f"CreatedDate = {created_on}")
    else:
        if created_before:
            where_conditions.append(f"CreatedDate < {created_before}")
        if created_after:
            where_conditions.append(f"CreatedDate > {created_after}")

    # Joining all where conditions with AND
    where_clause = " AND ".join(where_conditions) if where_conditions else ""
    query = f"SELECT {query_fields} FROM Account"
    if where_clause:
        query += f" WHERE {where_clause}"
    
    # Limiting size of queries
    query_limit = " LIMIT 5"
    params = {'q' : query+query_limit}

    url = f"{DOMAIN}{api_endpoint}"
    response = requests.get(url=url, headers=headers, params=params)
    data = response.json()
    return data


''' Function to list all Contacts data with filter option '''

def get_contacts(token, id = None, Name = None, email = None, birth_date_on = None, birth_date_before = None, birth_date_after = None):

    api_endpoint = f'/services/data/v58.0/query'
    headers = get_headers(token)
    query_fields = "Id, AccountId, Name, MailingAddress, Phone, Email, Department, BirthDate, OwnerId, CreatedDate"
    
    where_conditions = []
    if Name:
        where_conditions.append(f"Name = \'{Name}\'")
    if id:
        where_conditions.append(f"Id = \'{id}\'")
    if email:
        where_conditions.append(f"Email = \'{email}\'")
    if birth_date_on:
        where_conditions.append(f"BirthDate = {birth_date_on}")
    else:
        if birth_date_before:
            where_conditions.append(f"BirthDate < {birth_date_before}")
        if birth_date_after:
            where_conditions.append(f"BirthDate > {birth_date_after}")

    # Joining all where conditions with AND
    where_clause = " AND ".join(where_conditions) if where_conditions else ""
    query = f"SELECT {query_fields} FROM Contact"
    if where_clause:
        query += f" WHERE {where_clause}"

    # Limiting size of queries
    query_limit = " LIMIT 5"
    params = {'q' : query+query_limit}

    url = f"{DOMAIN}{api_endpoint}"
    response = requests.get(url=url, headers=headers, params=params)
    data = response.json()
    return data


''' Function to list all Oppurtunities data with filter option '''

def get_opportunities(token, id = None, Name = None, Amount = None, Amount_gt = None, Amount_lt = None, ExpectedRevenue = None, ExpectedRevenue_gt = None, ExpectedRevenue_lt = None):
    api_endpoint = f'/services/data/v58.0/query'
    headers = get_headers(token)
    query_fields = "Id, AccountId, Name, Amount, Probability, ExpectedRevenue, CloseDate, OwnerId, CreatedDate"
    
    where_conditions = []
    if Name:
        where_conditions.append(f"Name = \'{Name}\'")
    if id:
        where_conditions.append(f"Id = \'{id}\'")

    if Amount:
        where_conditions.append(f"Amount = {Amount}")
    else:
        if Amount_gt:
            where_conditions.append(f"Amount > {Amount_gt}")
        if Amount_lt:
            where_conditions.append(f"Amount < {Amount_lt}")

    if ExpectedRevenue:
        where_conditions.append(f"ExpectedRevenue > {ExpectedRevenue}")
    else:
        if ExpectedRevenue_gt:
            where_conditions.append(f"ExpectedRevenue > {ExpectedRevenue_gt}")
        if ExpectedRevenue_lt:
            where_conditions.append(f"ExpectedRevenue < {ExpectedRevenue_lt}")

    # Joining all where conditions with AND
    where_clause = " AND ".join(where_conditions) if where_conditions else ""
    query = f"SELECT {query_fields} FROM Opportunity"
    if where_clause:
        query += f" WHERE {where_clause}"

    # Limiting size of queries
    query_limit = " LIMIT 5"
    params = {'q' : query+query_limit}
    url = f"{DOMAIN}{api_endpoint}"
    response = requests.get(url=url, headers=headers, params=params)
    data = response.json()
    return data



if __name__ == '__main__':

    try:
        token = get_access_token()
        data = get_accounts(token, Name='GenePoint')
        # data = get_contacts(token, email='jrogers@burlington.com')
        # data = get_opportunities(token, Amount_gt = 75000)
        print(get_refreshed_access_token())

        print(data)

    except TypeError:
        print("Please provide all mandatory parameters")

    except Exception as e:
        print(f"An error occured : {e}")