#  Marcus Butler
#  pwned_passwd.py
#  Last Updated: Arpil 24, 2018

"""

  pwned_passwd.py is a script written in Python that hashes a
  user-provided password, reassigned the PT password to None,
  splits the password into a prefix and suffix as defined by the
  k-anonymity model, and runs a query against the 
  Have I Been Pwned (HIBP) breached password database. 

  The HIBP database is structured so that every 5 character hexadecimal
  combination (00000-FFFFF) is indexed as a 'bucket' and every 35 character 
  suffix value is stored in that bucket. At the time of writing the database 
  was 40 gigabytes in size and stores 500 million different passwords.
  On average, each API request will return 478 SHA1 suffix values. The results
  are stored during runtime in a hash table. A lookup is then performed to determine
  if the hashed password suffix is present in the API results and the number of occurrences
  is printed to the console.

  This program successfully accomplishes all of this without your actual password
  ever leaving the local machine.

  
"""
import hashlib
import requests
import getpass
import sys
import time

#  define the url base and headers for HIBP API access
api_url_base = "https://api.pwnedpasswords.com/range/"
headers = {"User-Agent": "Python HIBP Data Structures Project"}
results_dict = {}

#  function builds get request to pass to HIBP API
def get_info(h_prefix):
    start = time.time()
    api_url = "https://api.pwnedpasswords.com/range/{}".format(h_prefix)
    try:
        response = requests.get(api_url, headers=headers)

    except requests.exceptions.ConnectionError as e:
        print("Connection Error, Requests library returned the following error:")
        print(e, "\n")
        sys.exit(1)

    end = time.time()
    print("API returned results in {:.2f} seconds".format(end - start))
    print("API response code:", response.status_code)
    #  400 - Bad request passed to API
    if response.status_code == 400:
        print("Bad API request")
        sys.exit(1)

    #  429 - API rate limited
    if response.status_code == 429:
        print("API rate limited - Try again later")
        sys.exit(1)

    #  format the response
    response = response.content.decode("utf-8").split()
    return response


def build_dictionary(results):
    for line in results:
        line = line.split(":")
        results_dict[line[0]] = int(line[1])


passwd = getpass.getpass("Enter password:").encode("utf-8")
hash_passwd = hashlib.sha1()
hash_passwd.update(passwd)
passwd = None
digest = hash_passwd.hexdigest()
digest = digest.upper()
print("SHA1 Digest:", digest)

#  split the digest according to API docs
prefix = digest[:5]
print("Prefix [{}]".format(prefix))
suffix = digest[5:]
print("Suffix [{}]\n".format(suffix))
results = get_info(prefix)
build_dictionary(results)
print()

if suffix in results_dict:
    print(
        "Your password appears in the HIBP DB {:,} times".format(results_dict[suffix])
    )
else:
    print("Congratulations! Your password does NOT appear in the HIBP DB.")
