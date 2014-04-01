#!/usr/bin/python

__author__ = 'monkee'
import boto.ec2
from datetime import date
import yaml, sys,logging,time,os
from croniter import croniter



class thesleeper:
    conn = ""
    config = ""
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
    time = ""

    def __init__(self):
        os.environ["TZ"]="Australia/Brisbane"
        time.tzset()
        self.time = time.time()
        try:
            configStr = open('config.yml', 'r')
            self.config = yaml.load(configStr)
        except Exception as error:
            #we are done
            print ("Unexpected error:" + str(error))
            exit("Failed Configuration")
        logging.basicConfig(filename=self.config['general']['logfile'],level=logging.DEBUG)
        try:
            self.conn = boto.ec2.connect_to_region(self.config['general']['region'],aws_access_key_id=self.config['credentials']['aws_access_key'], aws_secret_access_key=self.config['credentials']['aws_secret_key'])
        except:
            #done again
            exit("Failed to connect to EC2")

    def stop_instance(self,instance):
        if instance.state == "running":
            instance.stop()

    def start_instance(self,instance):
        if instance.state != "running":
            instance.start()

    def search_for_tagged(self):
        try:
            reservations = self.conn.get_all_instances(filters={'tag-key' : self.config['general']['filter']})
            for reserve in reservations:
                self.parse_sleeper_tags(reserve.instances[0])

        except (BaseException) as emsg:
             logging.warning(self.timestamp + ': Cannot send message: ' + str(emsg))
             sys.exit(2)

    def search_for_untagged_to_stop(self):
        try:
            reservations = self.conn.get_all_instances()
            for reserve in reservations:
                if self.config['general']['filter'] not in reserve.instances[0].__dict__['tags']:
                    self.stop_instance(reserve.instances[0])
        except (BaseException) as emsg:
             logging.warning(self.timestamp + ': Base Exception ' + str(emsg))
             sys.exit(2)

    def parse_sleeper_tags(self,instance):
        value = instance.__dict__['tags'][self.config['general']['filter']]
        if value == "":
            #we always trash instances that are not tagged correctly
            self.stop_instance(instance)
            return
        elif value == 'pass':
            #we take no specific action with this - by design
            return
        try:
            crons = value.split('|')
            for i,v in enumerate(crons):
                if i == 0:
                    self.cron_stop(instance,v)
                elif i == 1:
                    self.cron_start(instance,v)
        except (BaseException) as emsg:
             logging.warning(self.timestamp + ': Base Exception ' + str(emsg))
             sys.exit(2)

    def cron_stop(self,instance,value):
        try:
            iter = croniter(value,self.time)
            point = iter.get_next(float)
            newpoint = iter.get_prev(float)
            misspast = newpoint - self.time
            if (misspast < 0) and (misspast > -300):
                self.stop_instance(instance)
        except (BaseException) as emsg:
             logging.warning(self.timestamp + ': Base Exception ' + str(emsg))
             sys.exit(2)

    def cron_start(self,instance,value):
        return
        print("start " + str(self.timestamp) + " " + str(self.time))
        try:
            iter = croniter(value,self.time)
            point = iter.get_next(float)
            newpoint = iter.get_prev(float)
            misspast = newpoint - self.time
            if (misspast < 0) and (misspast > -300):
                self.start_instance(instance)
        except (BaseException) as emsg:
             logging.warning(self.timestamp + ': Base Exception ' + str(emsg))
             sys.exit(2)


if __name__ == "__main__":
    thesleeper = thesleeper()
    thesleeper.search_for_untagged_to_stop()
    thesleeper.search_for_tagged()

