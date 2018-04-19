'''
*** THIS MODULE IS STILL UNDER DEVELOPMENT ***
This is the test runner for executing the testcases using the ROBOT automation framework

author: rdoshi
email: rdoshi@shoretel.com
'''
import sys
import argparse
import subprocess

class RoboRunner():
    '''
    RoboRunner class
    '''
    def __init__(self):
        self.TESTRESULT = "FAIL"
        self.TEST_ENV_CONFIG = {}
        pass

    def _verify_args(self):
        parser = argparse.ArgumentParser(description="RoboRunner: Utility for executing Robot testcases")
        parser.add_argument("-l", "--logs",
                            help="location for the run logs to be saved")
        parser.add_argument("-v", "--verbosity", help="Output Verbosity",
                            choices=[0,1,2], type=int)
        args = parser.parse_args()
        return args

    def _setup_runner_env(self, runnerargs=None):
        #by default it should load the values from the config file
        #and then overwrite the user defined value from the cli
        pass

    def runtests(self):
        roborunner_args = self._verify_args()
        env_setup_sucess = self._setup_runner_env(roborunner_args)
        print roborunner_args.verbosity
        if roborunner_args.logs is not None:
            robo_args = "-l " + roborunner_args.logs
        if roborunner_args.verbosity is not None:
            print roborunner_args.verbosity
        print ("hello")
        #print(sys.argv[1])
        # help(subprocess)
        #p = subprocess.Popen(["python", "-m ", "robot", robo_args, sys.argv[1]], stdout=subprocess.PIPE)
        #print (p.communicate())


if __name__ == '__main__':
    #check the arguments

    #set the env
    roborunner = RoboRunner()
    roborunner.runtests()