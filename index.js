const puppeteer = require('puppeteer');
var express     = require('express'); 
var app         = express();                
var bodyParser  = require('body-parser');
var fs = require('file-system');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 9709;        
var router = express.Router();             

router.get('/fetch-page', function(req, res) {
	(async function main(){
	    try {

			const browser = await puppeteer.launch({ headless: true, waitUntil: 'domcontentloaded', ignoreHTTPSErrors: true });
			const page = await browser.newPage();

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
		
			var json_data = data.filter(v=>v!='');

			console.log(json_data)

			res.json({ json_data });

			await browser.close();

	    } catch (e) {
			console.log('Err', e);
	    }
	})();
     
});

app.use('/api', router);
app.listen(port);
console.log('Magic happens on port ' + port);


