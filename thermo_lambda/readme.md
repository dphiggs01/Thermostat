Steps to enable a restfull API call in AWS

1. Create a lambda method
   * Create a zip of the files for your function `zip –X –r ../index.zip *`
   * Make sure we use Python 2.7 as 3.6 on Lambda does not support the needed version of openSSL
   * Create the function see the `publish.sh` script


2. Add method to the API Gateway interface (Thermostat)
   * Create a resource from the AWS Console use the method name from the lambda function
   * Add a method post or get

3. Test from Lambda and from API Gateway test

4. Publish the API!!!!

