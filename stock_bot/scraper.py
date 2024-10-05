import requests
from bs4 import BeautifulSoup

def fetch_transactions(url: str = 'https://www.dataroma.com/m/rt.php'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table and its rows
    table = soup.find('table', {'class': 'some_class'})  # Adjust with the correct table class if needed
    rows = table.find_all('tr')[1:]  # Skip the header row

    transactions = []
    for row in rows:
        cols = row.find_all('td')
        transaction_date = cols[0].text.strip()
        filing = cols[1].text.strip()
        reporting_name = cols[2].text.strip()
        activity = cols[3].text.strip()
        security = cols[4].text.strip()
        shares = cols[5].text.strip()
        price = cols[6].text.strip()
        total = cols[7].text.strip()
        
        transactions.append({
            'transaction_date': transaction_date,
            'filing_date': filing,
            'reporting_name': reporting_name,
            'activity': activity,
            'security': security,
            'shares': shares,
            'price': price,
            'total': total
        })
    
    return transactions


