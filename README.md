TheSleeper
==========

An AMI stop/start utility that parses a cron style tag for control

![ScreenShot](https://raw.github.com/monk-ee/TheSleeper/master/images/sleeper.png)

Tag Guide
==========
 + A tag needs to be added to each resource you wish to stop, the format is *TimeStartStop*.
 + This should (must) be managed by cloudformation or orchestration.
 + A minimum default of shutdown should be set UNLESS the resource must run all the time eg a utility server. A good default is: 0 21 * * *


NOTE WELL: all untagged resources will be shutdown at any point in time. There should never be any untagged resources ever!

Format is cron like and is in the format 'stop','start': The following example shuts down all AMI's tagged with 'Time Start/Stop' at 9pm on weekdays and starts them again at 9am.

    0 21 * * mon-fri | 0 9 * * mon-fri



If you want to just stop the instance  at 9pm weekdays and leave the start to a manual process then you would:

    0 21 * * mon-fri

If you want to ensure that the resource is not stopped add the following value:

     pass


TheSleeper shuts down to a schedule, and starts to a schedule.

Anything in between is considered to be manual shenanigans and sleeper don't care.

The only exception to this is untagged instances which are terminated with extreme prejudice at any time of day.

Configuration
==========
Requires: your boto config file (~/.boto) to contain your aws credentials

    [Credentials]
    aws_access_key_id = <your access key>
    aws_secret_access_key = <your secret key>

 + You may need to change your region and timezone.
 + You shouldn't need to change threshold unless you change the cron timing -
     the threshold is the time in seconds past the action that you schedule  - it allows for clock drift etc

Multiple Account Configuration
==========
Requires: your boto config file (~/.boto) add each additional account as a profile

    [profile SecondAccount]
    aws_access_key_id = <your access key>
    aws_secret_access_key = <your secret key>

You will need to have at least one base set of credentials setup. I made the decision to only use one sns topic to avoid complexity;
So the base credential should have the sns topic setup.

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


Dependencies
==========
 + PyYAML==3.10
 + boto==2.27.0
 + croniter==0.3.4


Author
==========
Contact me on twitter @monkee_magic

TODO
==========
 + @todo Rate Limit this puppy
 + @todo randomize start / stop inits when there are lots of servers
 + @todo setup the sns topic and subscription with boto