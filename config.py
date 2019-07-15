import ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
header = {'User-Agent': ua}
mail_host = "smtp.163.com" #here uses 163 stmp service
mail_user = "xxxxx@163.com" 
mail_pass = "xxxxx" #your stmp password

sender = "xxxxx@163.com"
receivers = ['xxxxx@yahoo.com', 'xxxxx@gmail.com']

my_wanted_days=['2019-08-05','2019-08-06']
num_of_us = 4
prefer="BOTH" #"LUNCH", "DINER"

