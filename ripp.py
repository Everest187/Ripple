from addons.title import Logo
from addons.utils import *
from addons.storage import *
from colorama import init
from typing import Tuple, List, Dict
import msmcauth, time, socket, ssl, datetime, sys, httpx, asyncio, aiohttp, os, json, requests, itertools
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import socks #$pip install PySocks

init()
accdata = []
accdata_proxy = []
threads_proxy = []
tasks = []
tasks_prx = []
checked_proxies = []
status_codes: List[int] = []
receive: Dict[float, int] = []
output: Tuple[int, float] = []
times: List[float] = []
logo = Logo("e v e r e st")
session = requests.Session()
#request methods
def req(acc_payload):
    """Send Socket Payload"""
    times.append(time.time())
    ss.send(acc_payload)

def proxy_checker(prox, addr, port, prox_user=None, prox_pass=None):
    try:
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        session.max_redirects = 300
        session.get("http://google.com", proxies={'SOCKS5':f'SOCKS5://{prox_user}:{prox_pass}@{prox}'}, timeout=(3.05,27), allow_redirects=True)
        # is_tcp = tcp(addr, port, prox_user, prox_pass)
        print(f"{logo('proxy')}Checked ~~ {host}")
        if len(splits) == 4:
            checked_proxies.append({"type": "SOCKS5", "proxy": prox, "host": addr, "port": port, "prox_username": prox_user, "prox_password": prox_pass})
        else:
            checked_proxies.append({"proxy": prox, "host": addr, "port": port})
    except Exception as prox_execp:
        print(prox_execp)
        print(f"{logo('proxy')}Failed to auth ~~ {host}")
        return prox_execp

async def requests(data_acc):
    """Send Socket Payload"""
    times.append(time.time())
    ss.send(data_acc)

async def ripl():
    for data_acc in accdata:
        [tasks.append(asyncio.ensure_future(requests(data_acc['payload']))) for _ in range(int(totalreq / len(accdata)))]
    sleep_for(droptime)
    await asyncio.gather(*tasks)
    done(10000)

async def proxy_reqs(sessions, dataacc_prox, dataacc_jsn, proxie):
    sents = time.time()
    async with sessions.post("https://api.minecraftservices.com/minecraft/profile", proxy=proxie, headers=dataacc_prox, json=dataacc_jsn) as fire:
        rev = time.time()
        print(f"Sent @ {datetime.datetime.utcfromtimestamp(sents).strftime('%S.%f')} ~~ [{fire.status}] {datetime.datetime.utcfromtimestamp(rev).strftime('%S.%f')}")

async def rippl():
    sessions = aiohttp.ClientSession()
    for proxys, acc_prox in itertools.zip_longest(checked_proxies, accdata_proxy):
      [tasks_prx.append(asyncio.ensure_future(proxy_reqs(sessions, acc_prox['headers'], acc_prox['json'], f"http://{proxys['prox_username']}:{proxys['prox_password']}@{proxys['proxy']}"))) for _ in range(int(totalreq / len(accdata_proxy)))]
    sleep_for(droptime)
    await asyncio.gather(*tasks_prx)
    await sessions.close()

def done(byt):
    term_threads()
    for sendrg in times:
        revs = ss.recv(byt).decode('utf-8')[9:12]
        time_end = time.time()
        receive.append({"exec": time_end - sendrg, "code": revs})
    output.extend([{"status": stats['code'], "times": None, "travel": stats['exec']} for stats in receive])
    ss.close()
    [o.update({'times':tim, 'travel': tim + o['travel']}) or o for o,tim in zip(output, times)]
    success_true(accdata)

def success_true(_data) -> None:
    webhook = "YOURWEBHOOK"
    req_deli: List[int] = []
    snipe_scess = SuccessSnipe(_data, req_deli, webhook, name, output)
    """Sort Times"""
    times.sort(key=lambda sorts: sorts)
    sr_time = snipe_scess.times()
    snipe_scess.check_event()
    if sr_time:
        snipe_scess.discweb()
    print(snipe_scess.__len__()) 

print(logo("Ripple"), end="")
code = input(f"[Name] [Offset] ~~ ").split()
try:
    # declaration
    offset = float(code[1]) / 1000
except (IndexError, ValueError):
    # rough estimate of delay
    pings = ping(5)
    print(f"\n[!] Received ~~ {pings}ms")
    tune_delay = input(f"[?] Tune Delay ~~ ")
    if len(tune_delay) < 1: 
        offset = pings / 1000
    else:
        offset = float(tune_delay) / 1000

name = code[0]
try:
    while offset.isnumeric() is False:
        offset = input(f"[!] invalid offset ~~ ")
except AttributeError:
    pass
while len(code) < 1:
    code = input(f"[!] invalid format ~~ ").split()

droptime = drop_exec(name, offset)
sendingat = datetime.datetime.utcfromtimestamp(droptime).strftime('%S.%f')

#file handling
file_parser("accs.txt", "proxies.txt")
#authentication
with open("accs.txt") as file:
    for line in file.read().splitlines():
        if not line.strip():
            continue
        splitter = line.split(":")
        try:
            email, password = (splitter[0], splitter[1])
        except IndexError:
            print(f"Please Provide your password for {splitter[0]}")
            pass
        #Microsoft & Gc auth
        try:
            if (msresp := msmcauth.login(email, password).access_token) and gc(msresp):
                gc_load = generator(method="POST", ep="minecraft/profile", json={'profileName': name}, headers={'Authorization': f'bearer {msresp}'})
                print(gc_load)
                accdata.append({"type": "gc", "reqamount": 3, "bearer": msresp, "email": email,
                                        "payload": gc_load.encode()})
                accdata_proxy.append({"type": "gc", "reqamount": 3, "bearer": msresp,"email": email,
                                            "headers": {'Authorization': f'Bearer {msresp}'}, "json": {"profileName": name}})
                print(f"Authenticated {email} {logo('GC')}")
            else:
                if namechange(msresp):
                    ms = generator(method="PUT", ep=f"minecraft/profile/name/{name}", headers={'Authorization': f'bearer {msresp}'})
                    accdata.append({"type": "ms", "reqamount": 4, "bearer": msresp,"email": email,
                                            "payload": ms.encode()})
                    accdata_proxy.append({"type": "ms", "reqamount": 4, "bearer": msresp,"email": email,
                                            "headers": {'Authorization': f'Bearer {msresp}'}, "json": {}})
                    print(f"Authenticated {email} {logo('MS')}")
                else:
                    print(f"[!] {email} cannot namechange")
        except msmcauth.errors.InvalidCredentials:
            with httpx.Client() as client:
                auth = client.post("https://authserver.mojang.com/authenticate",
                                          json={"username": email, "password": password})
                try:
                    header_nc = {"Authorization": f"Bearer {auth.json()['accessToken']}"}
                except KeyError:
                    pass
                if auth.status_code == 200 and len((auth.json())) != 0:
                    accesstoken = auth.json()['accessToken']
                    if namechange(accesstoken):
                        mj = generator(method="PUT", ep=f"minecraft/profile/name/{name}", headers={'Authorization': f'bearer {auth.json()["accessToken"]}'})
                        accdata.append({"type": "mj", "reqamount": 4, "bearer": accesstoken,"email": email,
                                            "payload": mj.encode()})
                        accdata_proxy.append({"type": "mj", "reqamount": 4, "bearer": accesstoken,"email": email,
                                            "headers": {'Authorization': f'Bearer {accesstoken}'}, "json": {}})
                        print(f"Authenticated {email} {logo('MJ')}")
                    else:
                        print(f"[!] {email} Cannot NameChange")
                else:
                    print(f"[!] Failed to authenticate {email}")
        except Exception:
            print(f"[!?] {email} locked [N/A]")
            pass

if not accdata:
    quit(f"No accounts Valid...")

input("[?] initiate sniper...")
clear()
logo.show() 
totalreq = sum(i["reqamount"] for i in accdata)
print(f"""Accounts ~~ {len(accdata)}
Request Amount ~~ {totalreq}
Proxies ~~ {len(checked_proxies)}
Initiating @ {float(sendingat)}
""") 
try:  
    countdown_time((droptime - time.time()) - 5)
except ValueError:
    pass

#Gen Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(('api.minecraftservices.com', 443))
ss = ssl.create_default_context().wrap_socket(sock, server_hostname='api.minecraftservices.com')
try:
    comp_up = UpperCase(sys.argv[1], "POOL")
    comp_asy = UpperCase(sys.argv[1], "ASYNC") 
    comp_prox = UpperCase(sys.argv[1], "PROXY")
    if comp_up.capitalize() and comp_up.__eq__(): 
        #Generate Threads
        thread_pool = ThreadPoolExecutor(max_workers=sum(pooldata.get("reqamount") for pooldata in accdata))
        sleep_for(droptime)
        for accdata_pool_exec in accdata: 
            for _ in range(accdata_pool_exec["reqamount"]):
                thread_pool.submit(req, accdata_pool_exec["payload"])
        thread_pool.shutdown(wait=False)
        done(2046) 

    elif comp_asy.capitalize() and comp_asy.__eq__():
        asyncio.get_event_loop().run_until_complete(ripl())
        exit()

    elif comp_prox.capitalize() and comp_prox.__eq__():
        #Checking proxies
        with open("proxies.txt") as filer:
            for line in filer.read().splitlines():
                if not line.strip():
                    continue
                splits = line.split(":")
                try:
                    if len(splits) == 4:
                        host, port, prox_user, prox_pass = (splits[0], splits[1], splits[2], splits[3])
                        proxy_checker(":".join(line.split(":")[:2]), host, port, prox_user, prox_pass)
                    else:
                        host, port = (splits[0], splits[1])
                        proxy_checker(line, host, port)
                except IndexError:
                    print("Port was not specified ~~ {host} skipping")
        session.close()
        if not checked_proxies:
            quit("No proxies available...")
        else:
            asyncio.get_event_loop().run_until_complete(rippl())
            exit()

except IndexError:
    threads = []
    for _acc in accdata:
        threads.extend([Thread(target=req, args=(_acc['payload'],)) for _ in range(_acc["reqamount"])])
    sleep_for(droptime)
    for starter in threads:
        starter.start()
    for end in threads:
        end.join()
    done(2046)