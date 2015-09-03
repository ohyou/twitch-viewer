# twitch-viewer
A viewer bot for twitch.tv

## Why
This application was created in order to provide a little help to the beginner streamers. Having 0 viewers for months is very upsetting so why not give yourself several viewers?  
The application was tested and developed to be used with a small amount of viewers, for which it has a very low CPU usage. Even though it can be used to get much more viewers, it was not intended to do so by the developers.

## How
The application was developed with Python 2.7.10 using the following libraries (installed using pip):
- requests
- json
- livestreamer

In order to run it, you need two things:
- A twitch channel, which name you pass as an argument to this script. For example, if the URL to your page is `twitch.tv/myname`, you should pass just `myname`
- A text file with the name `proxylist.txt` in the script's folder. Each line of which should have the following structure: `ip:port`.

The "viewers" you get only work through proxy.  
The amount of viewers you get equals to the amount of proxies there is in the `proxylist.txt` file.

The application starts working within ~10 seconds, and you will get viewers within a couple minutes (it takes some time for twitch to process the connections).

## Errors

- `An error has occurred while trying to read arguments.` - perhaps you didn't pass your channel as an argument
- `An error has occurred while trying to read the list of proxies...` - something is wrong with your `proxylist.txt`
- `An error has occurred while trying to get the stream data.` - something is wrong with twitch
- `An error has occurred while trying to process the response.` - something is wrong with the channel you provided, maybe wrong name or it is offline?
- `An error has occurred while preparing the threads: Not enough proxy servers.` - the application requiers 1 or more proxy in order to work
- `Timeout error for IP` - your request was timed out. If it happens multiple time for the same proxy, consider replacing it
- `Connection error for IP` - this is harmless, twitch sometimes refuses connection. This may occur frequently. Nothing to worry about.
