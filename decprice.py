import requests
import time
import urllib.parse
import emoji
from binascii import hexlify
from beemgraphenebase.ecdsasig import sign_message
from datetime import datetime

usernames = ["cosmicpigee","cosmicpigee2", "cosmicpigee4", "cosmicpigee3", "namelessclone8"]
usernames2 = ["toxicdiamond", "moscowcow", "cmon777", "runner1", "runner2", "splinterlandsftw"
            ,"cosmicpigee","cosmicpigee2", "cosmicpigee4", "cosmicpigee3", "namelessclone8"]
urls = ['https://api.coingecko.com/api/v3/simple/price'
        ,'https://game-api.splinterlands.com/players/balances' 
        ,"https://api2.splinterlands.com/players/unclaimed_balances"
        ,'https://game-api.splinterlands.com/players/login'
        ,'https://api.splinterlands.com/players/balance_history'
        ,'https://api.splinterlands.com/guilds/'
        ]



querystring = {
    'ids': 'splinterlands,dark-energy-crystals',
    'vs_currencies': 'usd'
}

def sigComp(Message, PrivateKey):
        signature =sign_message(Message,PrivateKey)
        return hexlify(signature).decode('ascii')
def login(PrivateKey):
    ts = int(time.time() * 1000)
    message = "cosmicpigee" + str(ts)
    sig = sigComp(message, PrivateKey)
    urlFull=f'{urls[3]}?name=cosmicpigee&ts={ts}&sig={sig}'
    response = requests.get(urlFull)
    if response.status_code == 200:
        data = response.json()
        with open ("keys.txt","r+") as file:
            lines = file.readlines()
            for i,line in enumerate(file,start=1):
                if i == 2:
                    parts = line.split("=")   
                    expiredate = parts[1].strip() 
                    if len(expiredate) < 1:
                        JwtToken = data.get('jwt_token')
                        JwtExpire = data.get('jwt_expiration_dt')
                        lines[i] = f"{"jwttoken"}={JwtToken}\n"
                    else:
                        print(expiredate)
                        JwtToken = expiredate 
                        JwtExpire = data.get('jwt_expiration_dt')
                            
                    return JwtToken, JwtExpire ,response.json()

def getBalance (Username):
    UserParam = {"username": Username}
    responseBalance = requests.get(urls[1], params=UserParam)
    balances = responseBalance.json()
    
    decBalance = next((float(item['balance']) for item in balances if item['token'] == 'DEC'), 0.0)
    spsBalance = next((float(item['balance']) for item in balances if item['token'] == 'SPS'), 0.0)
    stakedSps = next((float(item['balance']) for item in balances if item['token'] == 'SPSP'), 0.0)
    GlintBalance = next((item['balance'] for item in balances if item['token'] == 'GLINT'),"not found")
    meritsBalance = next((item['balance'] for item in balances if item['token'] == 'MERITS'),"not found")
    VoucherBalance = next((item['balance'] for item in balances if item['token'] == 'VOUCHER'),"not found")
    return decBalance, spsBalance ,stakedSps,meritsBalance,GlintBalance,VoucherBalance
    
def getUnclaimedBalance(Username):
    
    urlFull=f'{urls[2]}?token_type=SPS&username={Username}'
    responseUnclaimed =requests.get(urlFull)
    
    Unclaimed = responseUnclaimed.json()
    
    UnclaimedKey =Unclaimed.get("unclaimed_balances", [])
    UnclaimedSps =0
    UnclaimedType = ['wild','modern','brawl']
    UnclaimedBalances=[]
    for UnclaimedType in UnclaimedType:
        for item in UnclaimedKey:
            if item.get("token") == "SPS" and item.get('type')==UnclaimedType:
                balance= float(item.get("balance",0))
                UnclaimedBalances.append({"type":UnclaimedType,"balance":balance})
                UnclaimedSps += balance
    return UnclaimedSps , UnclaimedBalances

def RentalData(Username ,JwtToken):
    urlFull = f'{urls[4]}?username={Username}&token_type=DEC&types=rental_payment&from=&last_update_date=&limit=50&token={JwtToken}'
    response = requests.get(urlFull)
    current_time = datetime.now().date()

def CurrentTime():
    print(current_time)
    return response.json()
def Main(Username, IsSummary):
    TotalDec = 0
    TotalSps = 0
    TotalStaked = 0
    TotalUnclaimed = 0
    AllUnclaimed = 0
    AccData = ""
    for Username in Username:
        
        UnclaimedSps,UnclaimedBalances = getUnclaimedBalance(Username)
        decBalance, spsBalance ,stakedSps ,merits, GlintBalance, VoucherBalance = getBalance(Username)
        TotalUnclaimed =  (round((UnclaimedSps),2))
        TotalDec =  (round((TotalDec + decBalance),2))
        TotalSps =  (round((TotalSps + spsBalance),2))
        TotalStaked =  (round((TotalStaked +stakedSps),2))
        AllUnclaimed =  (round((AllUnclaimed+TotalUnclaimed),2))
        AccData += f"\n**Username**: {Username}\n"
        AccData += f"**DEC**: {decBalance}\n"
        AccData += f"**Liquid SPS**: {spsBalance}\n"
        AccData += f"**Staked SPS**: {stakedSps}\n"
        AccData += f"**Unclaimed SPS**: {TotalUnclaimed}\n"
        AccData += f"**Total SPS**: {spsBalance + stakedSps + TotalUnclaimed}\n"
        #UnclaimedBalaces_Pretty = ""
        #for sps in UnclaimedBalances:
        #    UnclaimedBalaces_Pretty +=(str(f"{sps['type'].capitalize()} - {sps['balance']} "))
        #AccData += f"**Unclaimed Sps **:{UnclaimedBalaces_Pretty}\n"
        
        AccData += f"**Glint**: {GlintBalance}\n"
        AccData += f"**Merits**: {merits}\n"
        AccData += f"**VOUCHER**: {VoucherBalance}\n"

    if IsSummary:
        AccSum = Summary(TotalDec, TotalSps, TotalStaked,TotalUnclaimed,AllUnclaimed )
        return AccSum
    else:
        AccSum = Summary(TotalDec, TotalSps, TotalStaked,TotalUnclaimed,AllUnclaimed )
        return AccData + AccSum

def FileOpen():
    with open ("keys.txt","r") as file:
        firstline=  file.readline().strip()
        parts = firstline.split("=")  
        privatekey = parts[1].strip()  
        print (privatekey)
        JwtToken, JwtExpire, loginResponse = login(privatekey)
        print(f"JWT Token: {JwtToken}")
        print(f"JWT Expiration: {JwtExpire}")


def Summary (TotalDec, TotalSps, TotalStaked,TotalUnclaimed,AllUnclaimed ):
    AccSum = ""
    ResponsePrice = requests.get(urls[0], params=querystring)
    PriceData = ResponsePrice.json()

    DecPrice = PriceData.get('dark-energy-crystals', {}).get('usd', 'Price not found')
    SpsPrice = PriceData.get("splinterlands", {}).get('usd', 'Price not found')
    
    ResponsePrice = requests.get(urls[1], params=querystring)
    PriceData = ResponsePrice.json()

    DecUsd = DecPrice * TotalDec
    SpsUsd = SpsPrice * TotalSps
    StakedUsd = SpsPrice * TotalStaked
    AllSPS = TotalStaked + TotalSps + TotalUnclaimed
    AllSPSUsd = SpsPrice * AllSPS
    AllUnclaimedUsd = SpsPrice * AllUnclaimed 
    EverythingUsd = DecUsd + AllSPSUsd
    
    AccSum += f"\n**Total**\n"
    AccSum += f"**DEC**: {TotalDec} (${round((DecUsd),2)})\n"
    AccSum += f"**Liquid SPS**: {TotalSps} (${round((SpsUsd),2)})\n"
    AccSum += f"**Staked SPS**: {TotalStaked} (${round((StakedUsd),2)})\n"
    AccSum += f"**Unclaimed SPS**: {AllUnclaimed } (${round((AllUnclaimedUsd),2)})\n"
    AccSum += f"**Total SPS**: {round((AllSPS),2)} (${round((AllSPSUsd),2)})\n"
    AccSum+= f"**Total Value**: (${round((EverythingUsd),2)})\n"

    
    return AccSum 

def GuildData(GuildName):
    GuildName = str(GuildName)
    FormatGuildName = GuildName.replace(" ", "%20")
    urlFull=f'{urls[5]}list?name={FormatGuildName}'
    
    ResponseGuild =requests.get(urlFull)
    Guilds = ResponseGuild.json().get("guilds", [])
    
    GuildInfo = ""
    NameData = next((guild for guild in Guilds if guild['name'] == GuildName), None)

    GuildInfo +=f"Name: {str(NameData['name'])}\n"
    GuildInfo +=f"Owner: {NameData['owner']}\n"
    GuildInfo +=f"Created Date: {NameData['created_date']}\n"
    GuildInfo +=f"Description: {NameData['description']}\n"
    GuildInfo +=f"Motto: {NameData['motto']}\n"
    GuildInfo +=f"Level: {NameData['level']}\n"
    GuildInfo +=f"Language: {NameData['language']}\n"
    GuildInfo +=f"Members: {NameData['num_members']}\n"
    GuildInfo +=f"Rank: {NameData['rank']}\n"
    GuildInfo +=f"Rating: {NameData['rating']}"
    return str(GuildInfo)
