# uptime-script
Python script to ping your favourite website

## sitemaps.json
````json
{
    "sitemaps": [
        "https://google.com/sitemap.xml",
        ".."
    ],
    "urls": [
    	"https://google.com"
    ]
}
````

## JSON:sitemap
Needs to follow specs [<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">](http://www.sitemaps.org/schemas/sitemap/0.9)

## JSON:urls
Array of specific URLs to ping

## run script
`$ python uptime.py`

## setup in Automator.app (OSX)
1. Run Shell Script
2. insert shell script:
`$ cd {path to your repository folder}
$ python uptime.py
`