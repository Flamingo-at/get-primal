<h1 align="center">Primal</h1>

<p align="center">Registration of referrals for the <a href="https://www.getprimal.com/">Primal</a> application</p>
<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
</p>

## ⚡ Installation
+ Install [python](https://www.google.com/search?client=opera&q=how+install+python)
+ [Download](https://sites.northwestern.edu/researchcomputing/resources/downloading-from-github) and unzip repository
+ Install requirements:
```python
pip install -r requirements.txt
```

## 💻 Preparing
**Bot only supports rambler email with activated IMAP**
+ Create ```emails.txt``` in the project folder
+ Insert emails each on a new line
  + Example: ```email@rambler.ru:password```
+ Register and replenish the balance <a href="https://rehalka.online/user">rehalka.online</a>
  + <i>You may need a VPN to access the site, in which case the bot will also need a VPN</i>
+ Run the bot:
```python
python get_primal.py
```

## ✔️ Usage
+ ```Captcha key``` - your key from rehalka.online
+ ```Referral code``` - your referral code from the application
+ ```Delay(sec)``` - delay between referral registrations in seconds
+ ```Threads``` - number of simultaneous registrations

**Successfully registered referrals are saved in** ```registered.txt``` **in the format** ```{email}:{password}:{address}:{private_key}```

## 📧 Contacts
+ Telegram - [@flamingoat](https://t.me/flamingoat)
