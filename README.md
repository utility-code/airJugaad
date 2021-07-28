# AirJugaad

- I want clipboard sync + airdrop
- Why not just put it in a live website with clipboard being monitored constantly?
- Heck. Why not integrate siri shortcuts so we can directly copy paste from the website.

## Features
- Direct copy using siri shortcuts! (This requires a lil manual effort so check the next section)
- Clipboard history
- Images, text 
- Stored in a text file and image folder
- Can send files from any device with the same network
- Can access a single directory from the main system if you want to grab stuff from your main system from other devices
- Should work as long as you have a browser, internet and data/wifi

## Clipboard sync
- Open the shortcuts app. Its called siri shortcuts
- Add the following workflows. Send them to your home screen :)
- ![img](./short1.jpg)  # for text
- ![img](./short2.jpg)  # for images

## How to use
- Just do python runner.py -i youripaddress
        - eg: python runner.py 192.168.1.114
- It will show you a port. Default is 8080
- Open it on the browser or follow the instructions in "#Important"
- Now you can either go to the url it shows on your main system. 

## IMPORTANT
- For any other device the url will be 
youripaddress:port
        - eg: 192.168.1.114:8080

## FAQ
- Jugaad means something like a life hack in Hindi. Mostly used when you do something that would normally be expensive or time consuming, in an easy way
