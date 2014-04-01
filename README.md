TheSleeper
==========

A AMI stop/start utility that parses a cron style tag for control

Intro
==========
A python utility server runs "TheSleeper" a scheduler that parses cron like commands to shutdown and start instances.

Step-by-step guide
==========
 + A tag needs to be added to each resource you wish to stop, the format is 'Time Start/Stop'. This should be managed by cloudformation or orchestration.
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
Add your secret API details to the config.yml.sample and rename config.yml


Author
==========
Contact me on twitter @monkee_magic