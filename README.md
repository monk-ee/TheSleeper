TheSleeper
==========

An AMI stop/start utility that parses a cron style tag for control


Tag Guide
==========
 + A tag needs to be added to each resource you wish to stop, the format is *TimeStartStop*.
 + This should (must) be managed by cloudformation or orchestration.
 + A minimum default of shutdown should be set UNLESS the resource must run all the time eg a utility server. A good default is: 0 21 * * *


NOTE WELL: all untagged resources will be shutdown at any point in time. There should never be any untagged resources ever!

Format is cron like and is in the format 'stop','start': The following example shuts down all AMI's tagged with 'Time Start/Stop' at 9pm on weekdays and starts them again at 9am.

    0 21 * * mon,fri | 0 9 * * mon,fri



If you want to just stop the instance  at 9pm weekdays and leave the start to a manual process then you would:

    0 21 * * mon,fri

If you want to ensure that the resource is not stopped add the following value:

     pass

Configuration
==========
Requires: your boto config file (~/.boto) to contain your aws credentials

    [Credentials]
    aws_access_key_id = <your access key>
    aws_secret_access_key = <your secret key>

 + You may need to change your region and timezone.
 + You shouldn't need to change threshold unless you change the cron timing -
     the threshold is the time in seconds past the action that you schedule  - it allows for clock drift etc

Proxy
==========
You may need to add proxy information to your .boto file

    [Boto]
    debug = 0
    num_retries = 10

    proxy = myproxy.com
    proxy_port = 8080


Cron Configuration
==========

    */5 * * * * /opt/TheSleeper/thesleeper.py >> /opt/TheSleeper/cron.log 2&>1

SNS Topic
==========
You can configure an AWS SNS Topic, then you can publish to email or whatever.
Add your Topic ARN to the config.yml and I am assuming you have setup the SNS Stuff.

It will aggregrate a series of stop/start actions into a single topic push. (Thanks Mark)

Author
==========
Contact me on twitter @monkee_magic

TODO
==========
@todo Rate Limit this puppy
@todo randomize start / stop inits when there are lots of servers