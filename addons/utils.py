import time, json, requests, os, platform, threading, socks
from typing import List
from time import time, sleep
from addons.storage import *

def term_threads() -> None:
        threads = threading.active_count() - 1
        while threads:
            threads = threading.active_count() - 1
            sleep(0.5)  # Wait until threads terminate

def tcp(addr, port, user=None, pwd=None):
    s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM) # Same API as socket.socket in the standard lib
    s.set_proxy(socks.SOCKS5, addr, port, False, user, pwd) # SOCKS4 and SOCKS5 use port 1080 by default
    s.connect(("www.google.com", 80))
    s.send(b"GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n", "utf-8")
    rsp = s.recv(4096)
    if rsp.startswith("HTTP/1.1 200 OK"):
        return "TCP"
    else:
        return "N/A"
    s.close()

def ping(num_ping: int) -> float:
    """auto delay"""
    delays: List[float] = []
    test_payload = ("PUT /minecraft/profile/name/TEST HTTP/1.1\r\nHost: api.minecraftservices.com\r\nAuthorization: Bearer " + "TEST_TOKEN\r\n\r\n", "utf-8")
    socket_connection = SocketConn(test_payload, 1024)
    socket_connection.conn()
    for _ in range(num_ping):
        start = time()
        socket_connection.sock_send()
        socket_connection.sock_recv()
        end = time()
        delays.append(end - start)
    socket_connection.sock_close()
    auto_offset = int((sum(delays) / len(delays) * 4000 / 2) + 5)
    return auto_offset

def time_converter(var) -> float:
    return datetime.datetime.utcfromtimestamp(var).strftime('%S.%f')

def fetch_drop(name: str) -> float:
    """fetch unix droptime"""
    req = requests.get(f"http://api.star.shopping/droptime/{name}", headers={"User-Agent": "Sniper"})
    if req.status_code == 200:
        return req.json()["unix"]

def drop_exec(name:str, offset:float) -> float:
    """scan errors"""
    try:
        droptime: float = (fetch_drop(name) - float(offset))
    except (TypeError, json.decoder.JSONDecodeError):
        print("Failed to get droptime")
        droptime: float = int(input(f"{name} UNIX Timestamp ~~ "))

    return float(droptime)

def gc(bearer:str) -> bool:
    """Check if Giftcard acc"""
    if requests.get("https://api.minecraftservices.com/minecraft/profile/namechange",
                       headers={"Authorization": "bearer " + bearer}).status_code == 404:
        return True
    else:
        return False

def namechange(bearer: str) -> bool:
    """Check if name change is allowed"""
    return requests.get(
            "https://api.minecraftservices.com/minecraft/profile/namechange",
            headers={"Authorization": "Bearer " + bearer},
        ).json()["nameChangeAllowed"]

def sleep_for(timestamp:float) -> None:
    try:
        sleep(timestamp - time())  # sleep until target timestamp
    except Exception:
        pass

def countdown_time(count_amt: float) -> None:
    for count_amt in range(int(count_amt), 0, -1):
        mins, secs = divmod(count_amt, 99999)
        print(f"Generating Threads ~~ {secs:02d}s", end="\r")
        sleep(1)
        count_amt -= 1 

def generator(method: str=None, ep=None, json: dict=None, headers: dict=None) -> str:
    if ep[0] != "/":
        ep = f"/{ep}"
    if json is None:
        json = {}
    jsonformatted = ""
    if json != {}:
        jsonformatted = "{"
        for e in json:
            jsonformatted += f'"{e}": "{json[e]}", '
        jsonformatted = jsonformatted[:-2]
        jsonformatted += "}"
    payload = f"{method.upper()} {ep} HTTP/1.1\r\nHost: api.minecraftservices.com\r\nConnection: keep-alive\r\nReferer: https://google.com/\r\nOrigin: https://api.minecraftservices.com\r\n"
    for h in headers:
        payload += f"{h}: {headers[h]}\r\n\r\n"
    return payload

def clear() -> None:
    if platform.system() != "Windows":
        os.system("clear")
    else:
        os.system("cls")

def file_parser(*textfile: str) -> None:
    for files in textfile:
        with open(files, mode="r") as file:
            data = file.read()

        words = data.replace("\n", " ").split()

        found_words = set()  # no order.
        filtered_words = []  # keeps insertion order.
        for i in words:
            if i not in found_words:
                filtered_words.append(i)
                found_words.add(i)

        in_string = "\n".join(filtered_words)

        with open(files, mode="w") as file:
            file.write(in_string)

        try:
            with open(files, mode="r") as f:
                    # Ignore Spaces in text file
                    lines = list(filter(lambda i: i, list(map(lambda s: s.strip("\n"), f.readlines()))))
        except FileNotFoundError:
            quit(f"{files} not found")