from nutils import system
from os import environ, listdir,getenv
from os.path import join,basename,isdir,expanduser
from sys import argv
from platform import platform,node
from socket import getfqdn
import getpass

####VARIABLES
global COMMANDS
COMMANDS = []
DEFAULT_COMMANDS    = ["CLEANUP_WWW_AREA","UNINSTALL","ENVIRONMENT","DEPENDENCIES",
                       "CHECKOUT","BUILD","RELEASE","INSTALL","TEST_DUMMY_SUBSYSTEM",
                       "TEST_L1CE","TEST_CENTRAL_CELL","TEST_RETRI_CELL","TEST_TTC",
                       "TEST_GT","TEST_GMT","TEST_L1PAGE"]
TO_EMAIL            = ""
CHECKOUT_NAME       = ""
BUILD_HOME          = ""
USER_NAME           = getpass.getuser()
USER_HOME           = join(expanduser("~"))
PLATFORM            = platform()
HOSTNAME            = node()
RELATIVE_BASE       = join("nightly",basename(__name__+".py"),PLATFORM)
NIGHTLY_BASE        = join(USER_HOME,"www",RELATIVE_BASE)
NIGHTLY_RPM_DIR     = join(NIGHTLY_BASE,"RPMS")
NIGHTLY_LOG_DIR     = join(NIGHTLY_BASE,"logs")
#The log file name and path should be the same than in the one in the acrontab
CACTUS_PREFIX       = "/opt/cactus"
XDAQ_ROOT           = "/opt/xdaq"
L1PAGE_ROOT         = "/opt/l1page/tomcat/webapps/ROOT"

#PSEUDO PLATFORM
pseudo_platform = "unknown"
if PLATFORM.find("i686-with-redhat-5") != -1:
    pseudo_platform="slc5_i686"
elif PLATFORM.find("x86_64-with-redhat-5") != -1:
    pseudo_platform="slc5_x86_64"
elif PLATFORM.find("x86_64-with-redhat-6") != -1:
    pseudo_platform="slc6_x86_64"

####VARIABLES: analysis of logs
TITLE             = "TS Nightlies : %s @%s " % (pseudo_platform,HOSTNAME)
FROM_EMAIL        = "cactus.service@cern.ch"
WEB_URL           = join("http://cern.ch/"+USER_NAME,RELATIVE_BASE)
NIGHTLY_LOG_FILE    = join(NIGHTLY_LOG_DIR,"nightly.log")
ERROR_LIST        = ['error: ',
                     'RPM build errors',
                     'collect2: ld returned',
                     ' ERROR ',
                     ' Error ',
                     'TEST FAILED',
                     'L1Page ERROR']

IGNORE_ERROR_LIST = ["sudo pkill",
                     "sudo rpm -ev"]

TEST_PASSED_LIST  = ["TEST OK",
                     "L1Page OK"]


#xdaq.repo file name as a function of the platform, and alias dirs for the nightlies results
XDAQ_REPO_FILE_NAME = "xdaq.%s.repo" % pseudo_platform

####ENVIRONMENT
environ["XDAQ_ROOT"]       = XDAQ_ROOT
environ["LD_LIBRARY_PATH"] = ":".join([join(CACTUS_PREFIX,"lib"),
                                       join(XDAQ_ROOT,"lib"),
                                       "/lib",
                                       environ.get("LD_LIBARY_PATH","")])

def importCommands() :
  global COMMANDS
  COMMANDS += [["TESTECHO", 
                ["echo This is a test",
                "echo TO_EMAIL = %s" % TO_EMAIL,
                "echo CHECKOUT_NAME = %s" % CHECKOUT_NAME,
                "echo BUILD_HOME = %s" % BUILD_HOME,
                "echo PLATFORM = %s" % PLATFORM,
                "echo HOSTNAME = %s" % HOSTNAME,
                "echo RELATIVE_BASE = %s" % RELATIVE_BASE,
                "echo NIGHTLY_BASE = %s" % NIGHTLY_BASE]]]

  COMMANDS += [["CLEANUP_WWW_AREA", [""]]] # Dummy placeholder -- this corresponds to the call to cleanupLogs()

  COMMANDS += [["UNINSTALL",
                ["sudo /sbin/service xdaqd stop &> /dev/null ",
                "rpm -qa | grep daq-xaas-l1test | xargs sudo rpm -ev --nodeps",
                "rpm -qa | grep daq-xaas-gtgmttest | xargs sudo rpm -ev --nodeps",
                "sudo yum -y groupremove triggersupervisor gtgmt",
                "sudo yum -y groupremove uhal",
                "sudo yum -y groupremove extern_coretools coretools extern_powerpack powerpack database_worksuite general_worksuite hardware_worksuite ",
                "rpm -qa | grep l1page | xargs sudo rpm -ev &> /dev/null ",
                "sudo pkill -f \"xdaq.exe\" ",
                "rpm -qa| grep cactuscore- | xargs sudo rpm -ev &> /dev/null ",
                "rpm -qa| grep cactusprojects- | xargs sudo rpm -ev &> /dev/null ",
                "sudo pkill -f \"jsvc\" &> /dev/null ",
                "sudo pkill -f \"DummyHardwareTcp.exe\" &> /dev/null ",
                "sudo pkill -f \"DummyHardwareUdp.exe\" &> /dev/null ",
                "sudo pkill -f \"cactus.*erlang\" &> /dev/null ",
                "sudo pkill -f \"cactus.*controlhub\" &> /dev/null ",
                "sudo rm -rf %s" % BUILD_HOME]]]

  COMMANDS += [["ENVIRONMENT",
              ["env"]]]

  COMMANDS += [["DEPENDENCIES",
                ["sudo yum -y install arc-server createrepo bzip2-devel zlib-devel ncurses-devel python-devel curl curl-devel graphviz graphviz-devel boost boost-devel wxPython e2fsprogs-devel libuuid-devel qt qt-devel PyQt PyQt-devel qt-designer libusb libusb-devel",
                "sudo cp %s %s" % (XDAQ_REPO_FILE_NAME,"/etc/yum.repos.d/xdaq.repo"),
                "sudo yum clean all && sudo yum clean metadata && sudo yum clean dbcache && sudo yum makecache",
                "sudo yum -y groupinstall extern_coretools coretools extern_powerpack powerpack database_worksuite general_worksuite hardware_worksuite",
                "sed \"s/<platform>/%s/\" cactus.stable.repo  | sudo tee /etc/yum.repos.d/cactus.repo > /dev/null" % pseudo_platform,
                "sudo yum clean all && sudo yum clean metadata && sudo yum clean dbcache && sudo yum makecache",
                "sudo yum -y groupinstall uhal"
                ]]]

  CHECKOUT_CMDS = ["sudo mkdir -p %s" % BUILD_HOME,
                  "sudo chmod -R 777 %s" % BUILD_HOME,
                  "cd %s" % BUILD_HOME,
                  "svn -q co svn+ssh://%s@svn.cern.ch/reps/cactus/trunk" % CHECKOUT_NAME,
  #                 "svn -q co svn+ssh://svn.cern.ch/reps/cactus/tags/ts_1_12_6 ./trunk",
                  "svn -q co svn+ssh://%s@svn.cern.ch/reps/cmsos/branches/l1_xaas l1test/daq/xaas" % CHECKOUT_NAME,
                  "svn -q co svn+ssh://%s@svn.cern.ch/reps/cmsos/branches/gtgmt_xaas gtgmttest/daq/xaas" % CHECKOUT_NAME]

  COMMANDS += [["CHECKOUT",
                [";".join(CHECKOUT_CMDS)]]]

  COMMANDS += [["BUILD",
                ["cd %s;make -sk Set=ts" % join(BUILD_HOME,"trunk"),
                "cd %s;make -sk Set=ts rpm" % join(BUILD_HOME,"trunk")]]]

  COMMANDS += [["RELEASE",
                ["rm -rf %s" % NIGHTLY_RPM_DIR,
                "mkdir -p %s" % NIGHTLY_RPM_DIR,
                "mkdir -p %s" % NIGHTLY_LOG_DIR,
                "cp %s %s" % ("yumgroups.xml",NIGHTLY_RPM_DIR),
                "find %s -name '*.rpm' -exec cp {} %s \;" % (BUILD_HOME,NIGHTLY_RPM_DIR),
                "cd %s;createrepo -vg yumgroups.xml ." % NIGHTLY_RPM_DIR]]]

  COMMANDS += [["INSTALL",
                ["sed \"s/<platform>/%s/\" ts.nightly.repo  | sudo tee /etc/yum.repos.d/ts.repo > /dev/null" % pseudo_platform,
                "sudo yum clean all && sudo yum clean metadata && sudo yum clean dbcache && sudo yum makecache",
                "sudo yum -y groupinstall triggersupervisor",
                "sudo yum -y groupinstall gtgmt"]]]

  COMMANDS += [["TEST_DUMMY_SUBSYSTEM",
                ["sudo cp %s /etc/tnsnames.ora" % join(BUILD_HOME,"l1test/daq/xaas/slim/l1test/settings/etc/tnsnames.cern.ora"),
                "cp -r %s %s" % (USER_HOME+"/secure",BUILD_HOME),
                "sed -i 's|\(PWD_PATH=\).*$|\\1%s|' %s" % (join(BUILD_HOME,"secure"),
                                                            join(BUILD_HOME,"l1test/daq/xaas/slim/l1test/service/mf.service.settings")),
                "cd %s;make;make rpm;make install" % join(BUILD_HOME,"l1test/daq/xaas/slim/l1test"),
		"sudo rm -f /etc/cron.d/l1test.jobcontrol.cron",
                "sudo cp %s /etc/slp.conf" % join(BUILD_HOME,"l1test/daq/xaas/slim/l1test/settings/etc/slp.localhost.conf"),
                "sudo /sbin/service slp restart",
                "/bin/slptool findsrvs service:directory-agent",
                "sudo /sbin/service xdaqd start l1test",
                "sleep 240",
                "cd %s;python multicell.py" % join(BUILD_HOME,"trunk/cactusprojects/subsystem/tests"),
                "cd %s;python multicell_fault.py;" % join(BUILD_HOME,"trunk/cactusprojects/subsystem/tests"),
                "cd %s;python multicell_stress.py" % join(BUILD_HOME,"trunk/cactusprojects/subsystem/tests"),
                "sudo /sbin/service xdaqd stop l1test"]]]

  COMMANDS += [["TEST_L1CE",
                ["sudo /sbin/service xdaqd start l1test",
                "sleep 30",
                "cd %s;python l1ce.py" % join(BUILD_HOME,"trunk/cactuscore/ts/l1ce/tests"),
                "sudo /sbin/service xdaqd stop l1test"]]]

  COMMANDS += [["TEST_CENTRAL_CELL",
                ["sudo /sbin/service xdaqd start l1test",
                "sleep 30",
                "cd %s;python central.py" % join(BUILD_HOME,"trunk/cactusprojects/central/tests"),
                "sudo /sbin/service xdaqd stop"]]]

  COMMANDS += [["TEST_RETRI_CELL",
                ["sudo /sbin/service xdaqd start l1test",
                "sleep 30",
                "cd %s;python retri.py" % join(BUILD_HOME,"trunk/cactusprojects/retri/tests"),
                "sudo /sbin/service xdaqd stop l1test"]]]

  COMMANDS += [["TEST_TTC",
                ["sudo /sbin/service xdaqd start l1test",
                "sleep 30",
                "cd %s;python ttc.py" % join(BUILD_HOME,"trunk/cactusprojects/ttc/tests"),
                "sudo /sbin/service xdaqd stop l1test"]]]

  COMMANDS += [["TEST_GT",
                ["sed -i 's|\(PWD_PATH=\).*$|\\1%s|' %s" % (join(BUILD_HOME,"secure"),
                                                            join(BUILD_HOME,"gtgmttest/daq/xaas/slim/gtgmttest/service/mf.service.settings")),
                "cd %s;make;make rpm;make install" % join(BUILD_HOME,"gtgmttest/daq/xaas/slim/gtgmttest"),
		"sudo rm -f /etc/cron.d/gtgmttest.jobcontrol.cron",
                "sudo /sbin/service xdaqd start gtgmttest",
                "sleep 30",
                "cd %s;python gt.py" % join(BUILD_HOME,"trunk/cactusprojects/gt/tests"),
                "sudo /sbin/service xdaqd stop gtgmttest"]]]

  COMMANDS += [["TEST_GMT",
                ["sudo /sbin/service xdaqd start gtgmttest",
                "sleep 30",
                "cd %s;python gmt.py" % join(BUILD_HOME,"trunk/cactusprojects/gmt/tests"),
                "sudo /sbin/service xdaqd stop gtgmttest"]]]

  COMMANDS += [["TEST_L1PAGE",
                ["sudo yum -y install cactusprojects-l1page-*",
                "mkdir -p %s" % join(BUILD_HOME, "triggerpro/l1page/data"),
                "sudo sed -i 's|%s|%s|g' %s" % ("/nfshome0/centraltspro", BUILD_HOME, join(L1PAGE_ROOT, "main/l1page.properties")),
                "sudo sed -i 's|%s|%s|g' %s" % ("/nfshome0", BUILD_HOME, join(L1PAGE_ROOT, "main/l1page.properties")),
                "sudo sed -i 's|%s|%s|g' %s" % ("log4j.appender","#log4j.appender", join(L1PAGE_ROOT, "WEB-INF/classes/log4j.properties")),
                "python %s" % join(L1PAGE_ROOT, "test/l1pageTest.py")]
                ]]

  ### Commands used for Central Cell Development, not nightlies
  COMMANDS += [["UPDATE_CENTRAL_RPM",
                ["cd %s/trunk/cactusprojects/central/cell && make clean && make && make rpm" % BUILD_HOME,
                "sudo rpm -Uvh --force %s/trunk/cactusprojects/central/cell/rpm/cactusprojects-centralcell-1.*.x86_64.rpm" % BUILD_HOME ]]]
                
  COMMANDS += [["UPDATE_TSITF_RPM",
                ["cd %s/trunk/cactuscore/ts/itf && make clean && make && make rpm" % BUILD_HOME,
                "sudo rpm -Uvh --force %s/trunk/cactuscore/ts/itf/rpm/cactuscore-tsitf-1.*.x86_64.rpm" % BUILD_HOME ]]]

  COMMANDS += [["UPDATE_SUBSYSTEM_RPM",
                ["cd %s/trunk/cactusprojects/subsystem && make clean && make && make rpm" % BUILD_HOME,
                "sudo rpm -Uvh --force %s/trunk/cactusprojects/subsystem/supervisor/rpm/cactusprojects-subsystemsupervisor-1.*.x86_64.rpm" % BUILD_HOME, 
                "sudo rpm -Uvh --force %s/trunk/cactusprojects/subsystem/worker/rpm/cactusprojects-subsystemworker-1.*.x86_64.rpm" % BUILD_HOME,]]]

  COMMANDS += [["STOP_XDAQD",
              ["sudo /sbin/service xdaqd stop &> /dev/null ",
                "sudo pkill -f \"xdaq.exe\" "]]]

  COMMANDS += [["START_XDAQD",
              ["sudo /sbin/service xdaqd start &> /dev/null "]]]

def cleanupLogs() :
  # The following lines are meant to delete old platform directories containing RPMs and logs
  target_platform = "unknown"
  if pseudo_platform == "slc5_i686":
      target_platform = "i686-with-redhat-5"
  elif pseudo_platform == "slc5_x86_64":
      target_platform = "x86_64-with-redhat-5"
  elif pseudo_platform == "slc6_x86_64":
      target_platform = "x86_64-with-redhat-6"
    
    
  system("mkdir -p %s" % NIGHTLY_BASE,exception=False)
  system("rm -f %s" % join(NIGHTLY_BASE,"..",pseudo_platform),exception=False)
  system("ln -s %s %s" % (NIGHTLY_BASE,join(NIGHTLY_BASE,"..",pseudo_platform)),exception=False)

  del_dirs = [d for d in listdir(join(NIGHTLY_BASE, "..")) if isdir(join(NIGHTLY_BASE, "..", d)) and d.find(target_platform) != -1 and d != platform()]
  for d in del_dirs:
      system("rm -rf %s" % join(NIGHTLY_BASE, "..", d), exception=False)
