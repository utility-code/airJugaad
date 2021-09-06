# AirJugaad

- I want clipboard sync + airdrop but I do not have a Mac
- (aka universal clipboard + airdrop)
- Heck. Why not integrate siri shortcuts so we can directly copy paste from the website.

## Features
- Direct copy using siri shortcuts! (This requires a lil manual effort so check the next section)
- Images, text 
- Can send files from any device with the same network
- Can access a single directory from the main system if you want to grab stuff from your main system from other devices

## Siri Shortcuts hack
- Open the shortcuts app. Its called siri shortcuts
- Add the following workflows. Send them to your home screen :)
### For text -> Actions
- Get contents of web page at ["http://<yourip:8080>/textclip.html>]
- Make rich text from [Contents of web page]
- Get text from [Rich text from HTML]
- Copy [Text] to clipboard

### For images -> Actions
- Get contents of web page at ["http://<yourip:8080>/imageclip.html>]
- Get images from [Contents of web page]
- Copy [Images] to clipboard

## How to use
- Just do python runner.py -i youripaddress
        - eg: python runner.py localhost
- It will show you a port. Default is 8080
- Open it on the browser or follow the instructions in "#Important"
- Now you can either go to the url it shows on your main system. 

## IMPORTANT
- For any other device the url will be 
youripaddress:port
        - eg: 192.168.1.114:8080

## FAQ
- Jugaad means something like a life hack in Hindi. Mostly used when you do something that would normally be expensive or time consuming, in an easy way
