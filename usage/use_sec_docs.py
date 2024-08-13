import requests
from pprint import pprint
from edgar.client import EdgarClient

# Initialize the Edgar Client
edgar_client = EdgarClient()

# Initialize the `Filings` Services.
filings_service = edgar_client.filings()

# Grab some filings for Facebook using the advance query.
docs_10k = filings_service.query(
    cik='1326801',
    filing_type='10-k'
)

# Download the documents
for doc in docs_10k:

    response = requests.get(
        url=doc['filing_href'],
        headers={
            "User-Agent": "Sigma Coding coding.sigma@gmail.com",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.sec.gov"
        }
    )
    file_path = 'sec_docs/' + f'{doc["film_number"]}.html'

    with open(file=file_path, mode='w+', encoding='utf-8') as f:
        f.write(response.text)
