# uptime-script
Python script to ping your favourite website

## config.json
create a `config.json` file:
````json
{
	"loop-time": 86400,
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

## JSON:loop-time
number of seconds before next run

## JSON:sitemap
Needs to follow specs [<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">](http://www.sitemaps.org/schemas/sitemap/0.9)

## JSON:urls
Array of specific URLs to ping

## run script
`$ cd {path to your repository folder}
$ python uptime.py`
Script will loop per. config.json:loop
