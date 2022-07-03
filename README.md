# Have I Been Pwned Check - Python

## Description

Note: This was a python script I wrote many years for a data structures class.

`hibp.py` a script written in Python that hashes a user-provided password, reassigns the plain-text password to None, splits the password into a prefix and suffix as defined by the k-anonymity model, and runs a query against the Have I Been Pwned (HIBP) breached password database.

The HIBP database is structured so that every 5 character hexadecimal combination (00000-FFFFF) is indexed as a 'bucket' and every 35 character suffix value is stored in that bucket. At the time of writing the database was 40 gigabytes in size and stores 500 million different passwords.

On average, each API request will return 478 SHA1 suffix values. The results are stored during runtime in a hash table. A lookup is then performed to determine if the hashed password suffix is present in the API results and the number of occurrences is printed to the console.

This program successfully accomplishes all of this without your actual password ever leaving the local machine.

## Installation

- `pipenv install`

## Usage

- `pipenv shell`
- `python hibp.py`

### Example

An example checking number of occurrences for `password`

```bash
(python-hibp-check) $ python hibp.py
Enter password:
SHA1 Digest: 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
Prefix [5BAA6]
Suffix [1E4C9B93F3F0682250B6CF8331B7EE68FD8]

API returned results in 0.22 seconds
API response code: 200

Your password appears in the HIBP DB 9,545,824 times

```
