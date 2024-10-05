import requests
from bs4 import BeautifulSoup
from stock_bot.models import Transaction
from typing import List

def fetch_transactions(url: str = 'https://www.dataroma.com/m/rt.php') -> List[Transaction]:
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table (adjust with the correct table class or attributes if necessary)
    table = soup.find('table')  # Assuming there's only one table, or adjust with appropriate class

    # Extract rows, skipping the header row
    rows = table.find_all('tr')[1:]

    transactions = []
    for row in rows:
        cols = row.find_all('td')
        
        # Extracting data from columns
        transaction_date = cols[0].text.strip()
        filing = cols[1].text.strip()
        reporting_name = cols[2].text.strip()
        activity = cols[3].text.strip()
        security = cols[4].text.strip()
        shares = int(cols[5].text.strip().replace(',', ''))  # Convert shares to integer
        price = float(cols[6].text.strip().replace('$', ''))  # Convert price to float
        total = float(cols[7].text.strip().replace('$', '').replace(',', ''))  # Convert total to float
        
        # Create Transaction object and append to list
        transaction = Transaction(
            transaction_date=transaction_date,
            filing_date=filing,
            reporting_name=reporting_name,
            activity=activity,
            security=security,
            shares=shares,
            price=price,
            total=total
        )
        
        transactions.append(transaction)
    
    return transactions
