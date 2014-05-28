#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Requires: your boto config file (~/.boto) to contain your aws credentials
#
# [Credentials]
# aws_access_key_id = <your access key>
# aws_secret_access_key = <your secret key>

__author__ = 'monkee'
__project__ = 'TheSleeper'

import boto.ec2, boto.sns
import yaml, sys,logging,time,os
from croniter import croniter


class thesleeper:
    conn = ""
    config = ""
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
    sns_stop = list()
    sns_start = list()
    profile_name = None
    profile_list = []

    def __init__(self):
        self.load_credentials()
        self.load_defaults()
        self.set_timezone()
        self.sns_connect()
        #begin multiple connection loop
        for profile in self.profile_list:
            self.profile_name = profile
            self.ec2_connect()
            if self.config['general']['shutdown_untagged'] is True:
                self.search_for_untagged_to_stop()
            self.search_for_tagged()
            self.sns_message()
            #end multiple connection loop

    def load_credentials(self):
        for section,details in boto.config._sections.iteritems():
            if section == "Credentials":
                self.profile_list.append('None')
                continue
            if 'profile ' in section:
                self.profile_list.append(section[8:])
                continue

    def load_defaults(self):
        try:
            config_str = open(os.path.dirname(__file__) + '/config.yml', 'r')
            self.config = yaml.load(config_str)
            logfile = os.path.dirname(__file__) + "/" + self.config['general']['logfile']
            logging.basicConfig(filename=logfile, level=logging.INFO)
        except IOError as error:
            exit("Could not load config.yml: " + str(error))
        except:
            raise
            exit("Unexpected error:" + str(sys.exc_info()[0]))

    def set_timezone(self):
        try:
            os.environ["TZ"]=self.config['general']['time_zone']
            time.tzset()
            self.time = time.time()
        except Exception as error:
            exit("Could not set time related stuff- very bad")

    def ec2_connect(self):
        try:
            self.conn = boto.ec2.connect_to_region(self.config['general']['region'],profile_name=self.profile_name)
        except:
            #done again
            exit("Failed to connect to EC2")

    def sns_connect(self):
        try:
            self.snsconn = boto.sns.connect_to_region(self.config['general']['region'],profile_name=self.profile_name)
        except (BaseException) as emsg:
            #done again
            logging.warning(self.timestamp + ': No SNS configured correctly - carry on - ' + str(emsg))
            #no sns configured or some issue
            pass

    def search_for_tagged(self):
        try:
            reservations = self.conn.get_all_instances(filters={'tag-key' : self.config['general']['filter']})
            for reserve in reservations:
                self.search_sleeper_tags(reserve.instances[0])
        except (BaseException) as emsg:
             logging.warning(self.timestamp + ': Cannot search for instances ' + str(emsg))
             sys.exit("Cannot search for instances/reservations")

    def search_for_untagged_to_stop(self):
        try:
            reservations = self.conn.get_all_instances()
            for reserve in reservations:
                if self.config['general']['filter'] not in reserve.instances[0].__dict__['tags']:
                    self.stop_instance(reserve.instances[0])
        except (BaseException) as emsg:
             logging.warning(self.timestamp + ': Untagged stop exception - not critical' + str(emsg))
             pass

    def search_sleeper_tags(self,instance):
        value = instance.__dict__['tags'][self.config['general']['filter']]
        if value == "":
            #we always trash instances that are not tagged correctly
            self.stop_instance(instance)
            return
        elif value == 'pass':
            #we take no specific action with this - by design
            return
        self.parse_cron(instance,value)

    def parse_cron(self,instance,value):
        try:
            crons = value.split('|')
            for i,v in enumerate(crons):
                if i == 0:
                    self.cron_stop(instance,v)
                elif i == 1:
                    self.cron_start(instance,v)
        except (BaseException) as emsg:
             logging.warning(self.timestamp + ': Could not parse tags - carry on ' + str(emsg))
             pass

    def cron_stop(self,instance,value):
        try:
            misspast = self.return_misspast(value)
            if misspast is False:
                return
            if (misspast < 0) and (misspast > -self.config['general']['threshold']):
                self.stop_instance(instance)
        except (BaseException) as emsg:
            logging.warning(self.timestamp + ': Cron Stop Failed on a value ' + str(emsg))
            pass

    def cron_start(self,instance,value):
        try:
            misspast = self.return_misspast(value)
            if misspast is False:
                return
            if (misspast < 0) and (misspast > -self.config['general']['threshold']):
                self.start_instance(instance)
        except (BaseException) as emsg:
            logging.warning(self.timestamp + ': Cron start failed on a value ' + str(emsg))
            pass

    def return_misspast(self,value):
        try:
            iter = croniter(value,self.time)
            point = iter.get_next(float)
            newpoint = iter.get_prev(float)
            misspast = newpoint - self.time
            return misspast
        except:
            return False

    def stop_instance(self, instance):
        if instance.state == "running":
            self.sns_stop.append(instance.id)
            instance.stop()

    def start_instance(self, instance):
        if instance.state == "stopped":
            self.sns_start.append(instance.id)
            instance.start()

    def sns_message(self):
        message = ""

        for item in self.sns_start:
            message += "Started Instance:" + item + "\n"
        for item in self.sns_stop:
            message += "Stopped Instance:" + item + "\n"

        if message != "":
            try:
                self.snsconn.publish(self.config['general']['sns_topic'], message, "TheSleeper was invoked")
            except:
                pass


if __name__ == "__main__":
    ts = thesleeper()


