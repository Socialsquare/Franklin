var assert = require("assert"),
    test = require('selenium-webdriver/testing'),
    webdriver = require('selenium-webdriver'),
    driver;



var title = "CHANGE\nTHE WORLD!"


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



test.describe('Checks that a known user can log in and that the main page is displaying properly', function() {
    test.it('Opening the homepage shows the main headline properly', function()
    {
        driver.get("http://localhost:8000/");
        driver.findElement(webdriver.By.name("main-headline")).getText().then(function(returned_title_text) {
            if (returned_title_text != title)
            {
                console.error("The main headline is not equal to what the test specifies it should be. It is" + title + ", and it should be " + returned_title_text);
            }
        assert.equal(returned_title_text, title)

        }); //driver.findElement(webdriver.By.name("main-headline")).getText();

    });
});