import requests

headers = {
    'authority': 'www.codechef.com',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'sec-fetch-user': '?1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'referer': 'https://www.codechef.com/COOK114B',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-IN,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'cookie': '__auc=cfe49115165bc8f981c046451c7; notification=0; _ga=GA1.2.408395970.1536466852; _fbp=fb.1.1549118717620.1730458805; _hjid=741b61c3-a53d-4362-984c-2782a4be33b8; _gcl_au=1.1.714354353.1572513312; SESS93b6022d778ee317bf48f7dbffe03173=kh4234o9asfhskm7cabu18qnf0; __utmz=100380940.1579333730.352.107.utmcsr=discuss.codechef.com^|utmccn=(referral)^|utmcmd=referral^|utmcct=/; __utma=100380940.408395970.1536466852.1579338887.1579458666.355; __utmc=100380940; _gid=GA1.2.560363926.1579458666; __asc=d0067f1f16fbf53e0fe3bf23066; __utmt=1; _gat_UA-83576305-2=1; _gat_UA-141612136-1=1; poll_time=1579464583489; __utmb=100380940.29.10.1579458666; AWSALB=j02FqHRS2gc42q6fwugF3iSuOyD7+PuMvicc22H6tkJk+3aUbw3my0SW2Ey4veM+QFJYcrTCCZvX7YTWMZ7uTVGC7dWA6WhIZPCR2j2cyQH74zjJ3PLloE5G6zZS',
    'if-modified-since': 'Sun, 19 Jan 2020 20:09:42 +0000',
}

response = requests.get('https://www.codechef.com/users/noob77777', headers=headers)


