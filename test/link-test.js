var assert = require("assert"),
    test = require('selenium-webdriver/testing'),
    webdriver = require('selenium-webdriver'),
    driver;

var visitedUrls = []

test.before(function() {
    driver = new webdriver.Builder().
        usingServer("http://localhost:9515/").
        withCapabilities(webdriver.Capabilities.chrome()).
        build();
    driver.manage().window().maximize();
});

test.after(function() {
    driver.quit();
});



test.describe("Checks all the links it can find on the page and verifies that they don't 404 when clicked on", function() {
    test.it('None of the pages 404d', function()
    {
        visitUrls("http://localhost:8000")
    });
});

function visitUrls(startingUrl) {

    driver.get(startingUrl);
    driver.sleep(500);
    visitedUrls.push(startingUrl);
    var current_links = [];

    driver.findElements(webdriver.By.name('404-message')).then(function(possible404)
    {
        assert.equal(possible404.length, 0);
    });

    driver.findElements(webdriver.By.tagName('a')).then(function(links)
        {
            current_links = links;
            var re = /localhost:8000/
            //console.error(current_links)

            current_links.forEach(function(link){
                link.then(function(a) {
                    a.getAttribute("href").then(function(href) {
                        if (re.test(href) && visitedUrls.indexOf(href) == -1)
                        {
                            visitUrls(href);
                        }
                    })
                })
                
            });
        });



}