### Installation

Step 1: Bash into folder and run ``` npm install```

Step 2: Run: ```node index.js```

You can then use the Chrome browser, Python requests module, or PostMan at the api route below,
to retrieve the dynamic chart data in JSON format:

```http://localhost:9709/api/fetch-page```


Note: Between each run you must completely kill the NodeJS server process with:

```fuser -k -n tcp 9709```

---------------------------------------------------------

The only code you need to modify are the following varibles for each page, html elem, and html data attr:

```
    // url you want to target
    await page.goto(
        "https://www.eafo.eu/alternative-fuels/electricity/charging-infra-stats"
    );
    
    await new Promise(resolve =>  setTimeout(resolve, 1000));
    
    const data = await page.evaluate(() => 
    // query selector from DOM and html data attribute you want
        Array.from(document.querySelectorAll(
            '.google-chart')).map(d => JSON.parse(d.getAttribute(
                'data-tabledata'
        )))
    )
```

------------------------------------------------------

### API

1. The page you want to parse from: ```page.goto("<MY URL>")```

2. The HTML ID or Class: ```document.querySelectorAll('<ID or CLASS NAME>')```

3. The HTML data attribute: ```JSON.parse(d.getAttribute('<HTML ATTR FOR DATA>'))```