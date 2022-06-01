# Ripple
Ripple is a sniper that I finished developing on 2/27/2022 and will no longer be maintained as I have left the Minecraft Name Sniping Community. 

***The last update was on February 27, 2022, the Authentication Method / Endpoints may be out of date.
Feel free to make changes, but you must link to this repository for copyright reasons.***

*DM/Friend me @ 829537210390020096 via Discord for assistance*

## **Features**
- *Supports All Account Types* (Mojang, Microsoft, and Gift Card accounts.)
- *Multiple Accounts* (Allows more than one Minecraft account to be used.)
- *Auto Delay* (Gives an Estimated Delay from the Name Change Endpoint.)
- *Easy To Use* (Literally Only 2 Steps: Paste your accounts into `accs.txt`, Then enter your target username.)
- *Auto Auth* (Automatically scans and Authenticates each account.)
- *Proxie Auth* (Automatically authenticates your proxies)

## **Request Methods**
***All of these request features are optimized for speed, such as retrieving the current send time in unix and then computing the receive time for each send request once everything has been delivered.***
- *Pool + Sockets* (Uses ThreadPool and Sockets to send requests)
- *Async* (Async and Sockets to send requests) <- Fast Receives
- *Async + Proxy* (Async + Proxies to rotate requests with proxies)
- *Threading + Sockets* (Threading with sockets is highly optimized, ignoring all receives until the sending is complete, resulting in quick requests.)

## **Usage**
To change request methods, type `python3 ripp.py -METHOD` into the command line.

*Methods*
- POOL
- ASYNC
- PROXY
