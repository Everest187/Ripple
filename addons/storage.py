from http import client
import socket, ssl, datetime, requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import time
from colorama import Fore
# from paramiko import SSHClient, AutoAddPolicy

results = []

class SocketConn:
    def __init__(self, dataload: str, bytes_amt: int):
        self.sock = None
        self.dataload = dataload
        self.bytes_amt = bytes_amt

    def conn(self):
        socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socke.connect(('api.minecraftservices.com', 443))
        print("Delivered Connection Successfully")
        wrap = ssl.create_default_context().wrap_socket(socke, server_hostname="api.minecraftservices.com")
        self.sock = wrap

    def sock_send(self):
    	self.sock.send(bytes(f"{self.dataload}\r\n\r\n", "utf-8"))

    def sock_recv(self):
        results.append((self.sock.recv(self.bytes_amt).decode("utf-8")[9:12]))

    def sock_close(self):
    	self.sock.close()

class SuccessSnipe:
    def __init__(self, data_, reqd: list, webhook: str, target_name: str, out: list):
        self.data_ = data_
        self.reqd = reqd
        self.webhook = webhook
        self.target_name = target_name
        self.out = out

    def __len__(self) -> str:
        return f"Delivered {len(self.reqd)} Req(s) Successfully"
    
    def change_skin(self):
        skin_change = requests.post(
            "https://api.minecraftservices.com/minecraft/profile/skins",
            json={
                "variant": "slim",
                "url": "https://imgur.com/a/TNIjOT2",
            },
            headers={"Authorization": "Bearer " + token.get('bearer')},
        )
        if skin_change.status_code == 200:
            print(f"{Fore.LIGHTGREEN_EX}Successfully deliver Skin Change{Fore.RESET}")

    def check_event(self) -> bool:
        for tokens in self.data_:
            try:
                if requests.get("https://api.minecraftservices.com/minecraft/profile", headers={'Authorization': f'bearer {tokens["bearer"]}'}).json()['name'] is self.target_name:
                    print(f"Copped {self.target_name} ~~ {tokens['email']}")
                    break
                else:
                    pass
            except KeyError:
                pass

    def discweb(self):
        webhook = DiscordWebhook(url=f'{self.webhook}', rate_limit_retry=True)
        embed = DiscordEmbed(title="NameMC", url=f'https://namemc.com/search?q={self.target_name}',
                             description=f"""Ripple ~~
        > `Copped {self.target_name}`""", color=2303786)
        webhook.add_embed(embed)
        try:
            webhook.execute()
        except requests.exceptions.MissingSchema:
            print("No Webhook Url Specified")
        except requests.exceptions.ConnectionError:
            print("Failed to send webhook")

    def times(self) -> None:
        for outs in self.out:
            statusCode = outs['status'];sends = datetime.datetime.utcfromtimestamp(outs['times']).strftime('%S.%f')
            recs = datetime.datetime.utcfromtimestamp(outs['travel']).strftime('%S.%f')
            print(f"Sent @ {sends} ~~ [{statusCode}] {recs}")
            if int(statusCode) in (403, 200, 400):
                self.reqd.append(statusCode) 
            if statusCode.isnumeric() and int(statusCode) == 200:
                return True

# class VpsConn:
#     def __init__(self, hostname, port, user, passw) -> None:
#         self.hostname = hostname
#         self.port = port
#         self.user = user
#         self.passw = passw
#         self.client = SSHClient()

#     def conn(self):
#         self.client.set_missing_host_key_policy(AutoAddPolicy())
#         self.client.load_system_host_keys()
#         self.client.connect(hostname=self.hostname, port=self.port, username=self.user, password=self.passw, timeout=None)

#     def exec(self):
#         transport = client.get_transport()
#         transport.open_session()
#         client.exec_command("...")

#     def __call__(self):
#         return self.client.close()

class UpperCase:
    def __init__(self, upcase: str, obj2: str):
        self.upcase = upcase
        self. obj2 = obj2

    def __eq__(self) -> bool:
        return self.upcase == self.obj2

    def capitalize(self) -> str:
        case = "".join(map(chr, (
            ord(c) - (0x20 * (ord(c) in range(ord('a'), ord('z'))))
        for c in self.upcase)))
        self.upcase = case
        return case