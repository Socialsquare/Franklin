var assert = require("assert"),
    test = require('selenium-webdriver/testing'),
    webdriver = require('selenium-webdriver'),
    driver;

var username = "admin";
var password = "123456";


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


function signIn() {
    // Go to the login page.
    driver.get("http://localhost:8000/user/login/");
    driver.sleep(500);
    driver.findElement(webdriver.By.name('login')).sendKeys(username);
    driver.findElement(webdriver.By.name('password')).sendKeys(password);
    driver.findElement(webdriver.By.css('button[type=submit]')).click();
}

test.describe('Checks that a known user can log in', function() {
    test.it('A known username/password combination allows login.', function() {
        signIn();
        driver.sleep(500);
        driver.getCurrentUrl().then(function(returned_URL)
        {
 
            if ("http://localhost:8000/welcome" != returned_URL)
            {
                console.error("Login failed with a know username/password combination.");
            }
            assert.equal("http://localhost:8000/welcome", returned_URL)

        });
    });
});