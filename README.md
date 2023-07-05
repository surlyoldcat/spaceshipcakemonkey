# spaceshipcakemonkey
## Setup
### S3 Data Source
1. Create or choose a bucket and prefix in S3
2. Upload the data file `db.json` to the desired S3 location
3. Pat yourself on the back

### IAM
There are 2 roles needed, although they can be rolled into 1 if you so desire. The first is the Lambda execution role, with permissions to read the data file from S3. The second is for AppSync to invoke the Resolver lambdas.

I recommend prefixing the roles with something like 'mg_' so it's easier to select them from the dropdown lists in the console.
#### Lambda Execution
Trust relationship:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
Policies:
- AWSLambdaBasicExecutionRole
- an S3 policy something like this. You can make it specific to the S3 bucket and file if you like.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::*"
        }
    ]
}
```
#### AppSync Resolver
_Note: It's easiest just to choose 'create new role' when you set up the Lambda Data Source in the AppSync console. It will create these roles for you._

Trust relationship:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "appsync.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
Policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:invokeFunction"
            ],
            "Resource": [
                "arn:aws:lambda:us-east-1:YOURACCOUNTID:function:mg_spaceship_resolver",
                "arn:aws:lambda:us-east-1:YOURACCOUNTID:function:mg_spaceship_resolver:*"
            ]
        }
    ]
}

```
### Resolver Lambdas
Each subdirectory under `lambdas` is a lambda function. For each one,
1. Create a new Lambda function
2. Runtime = Python 3.8
3. Execution role = the role you created above
4. Copy/paste the code into the console code editor

### AppSync
1. Create a new AppSync API with the 'build from scratch' settings and API Key security.
2. Copy the schema from `schema.graphql`
3. Create a new AppSync Data Source for each lambda
   - Either use the AppSync role above, or select 'New Role' to let AWS magically create it for you.
4. From the Schema view in the console, map fields to resolvers:
    - Query.allMonkeys --> mg_monkey_resolver
    - Query.getMonkey --> mg_monkey_resolver
    - Query.allSpaceships --> mg_spaceship_resolver
    - Monkey.spaceships --> mg_spaceship_resolver
    - Spaceship.crew --> mg_spaceship_crew_resolver
      - THIS IS A BATCH RESOLVER. So in the console, flip the Enable Batching toggle and set the Max Batch Size to something like 10
5. If you like, you can also set up the Cake resolver for Monkey.cakes, but I didn't include that in the demo doc. It's a regular resolver like Monkey.spaceships.

_Note: The Enable Batching toggle doesn't always stick. I don't know why. But after you set things up, go back to Spaceship.crew resolver setup to make sure batching is on._

## Try It Out
Just use the Queries tab in the AppSync console to run some queries. The events and such can be found in the Lambda Cloudwatch logs.
