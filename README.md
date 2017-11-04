# uptime-script
Python script to ping the URLs of your favourite websites, you can setup

## config.json
create a `config.json` file:
````json
{
    "smtp-server": "smtp.gmail.com",
    "smtp-server": 587,
    "smtp-user": "smtp user-name",
    "smtp-password": "smtp password",

    "loop-time": {seconds},
    "sitemaps": [
        "https://google.com/sitemap.xml",
        "..."
    ],
    "urls": [
    	"https://google.com",
    	"..."
    ]
}
````

## JSON:smtp-server
url to the mail server which to send mail from

## JSON:smtp-port
The port to the smtp server

## JSON:smtp-user
user name for smtp server

## JSON:smtp-password
password for smtp server

## JSON:loop-time
number of seconds before next run

## JSON:sitemap
Needs to follow specs [<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">](http://www.sitemaps.org/schemas/sitemap/0.9)

## JSON:urls
Array of specific URLs to ping

## run script
`$ cd {path to your repository folder}
$ python uptime.py`

Script will loop as defined in config.json:loop (seconds)
