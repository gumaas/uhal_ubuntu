#!/usr/bin/env python
'''
'''

import optparse
import sys
import os

defaults = {
    'prefix':'.',
    'tag':'trunk',
}

def parse_args():

    # Usage
    usage = '%prog command'
    parser = optparse.OptionParser(usage)

    args = sys.argv[1:]

    if not args:
        parser.error('No plugin defined. Available plugins %s' % ', '.join(plugins.iterkeys()))
    elif args[0] not in plugins:
        parser.error('Plugin %s not found' % args[0])

    plugin = plugins[args[0]]

    parser.add_option_group( plugin.getOptions( parser ) )

    # define options here
    opts,args = parser.parse_args()

    plugin.validate(opts,args)

    # Arguments post-porcessing
    return plugin,opts,args

class DirSentry:

    def __init__(self, dir):
        if not os.path.exists(dir):
            raise RuntimeError('stocazzo '+dir)

        self._olddir = os.path.realpath(os.getcwd())
        # print self._olddir
        os.chdir(dir)

    def __del__(self):
        os.chdir(self._olddir)

class Plugin(object):

    @staticmethod
    def addStandardOptions(group):
        group.add_option('-p','--prefix', help='prefix for the checkout', default=defaults['prefix'])
        group.add_option('-t','--tag'   , help='tag to checkout (%default)', default=defaults['tag'])


class SvnDownloader(Plugin):

    def __init__(self, **kwargs ):
        for k,v in kwargs.iteritems():
            print k,v
            setattr(self,k,v)

        self.cactusRoot = os.path.realpath(self.prefix+'/cactus')
        self.tagRoot = os.path.join(self.cactusRoot, self.tag)

    @classmethod
    def getOptions(cls,parser):
        description = "This is to do an svn checkout"
        group = optparse.OptionGroup(parser,cls.__name__, description)
        Plugin.addStandardOptions(group)
        group.add_option('-u','--user'  , help='svn username')
        return group

    @classmethod
    def validate(cls,opts,args):
        if not opts.user:
            raise RuntimeError('username is missing!')

    def _checkoutCactus(self,svnpath):
        from os.path import exists,join
        if ( exists(self.cactusRoot) and exists(join(self.cactusRoot,'.svn'))):
            print self.cactusRoot,'already exists. Will try to use it'
            return
        cmd = 'svn co --depth=empty %s' % svnpath
        if self.prefix:
            cmd+=' '+self.cactusRoot


        print cmd
        os.system( cmd )

    def _update(self, subdir, depth='empty'):
        import os
        cmd = 'svn up --depth=%s %s %s' % (depth,svnpath,self.prefix)
        print cmd

    def _getEmpty(self, tag):
        tokens = [ d for d in tag.split('/') if d ]

#        partials = []
#        for i in xrange(len(tokens)):
#            partials.append( partials[i-1]+'/'+tokens[i] if i != 0 else tokens[0] )

        partials =  [ '/'.join(tokens[:i+1]) for i,_ in enumerate(tokens) ]

        # print partials
        csentry = DirSentry(self.cactusRoot)
        for s in partials:
            cmd = 'svn up --depth=empty %s' % s
            print cmd
            os.system( cmd )
            # os.chdir(s)
            # print os.getcwd()

        self.tagRoot = os.path.join(self.cactusRoot,tag)
        print self.tagRoot

    def _getsubdirs(self, subdirs):

        sentry = DirSentry(self.tagRoot)

        os.system('svn up '+' '.join(subdirs))

        os.system('ls -la')

    def _checkTag(self, svnurl ):

        retval = os.system('svn ls --depth=empty '+svnurl)

        if retval:
            raise RuntimeError(svnurl+' does not exists')

    def execute(self):
        import os

        if self.prefix and self.prefix != '.':
            os.system('mkdir -p %s' % self.prefix)

        svnpath = 'svn+ssh://%s@svn.cern.ch/reps/cactus' % self.user

        print 'Checking tag',self.tag
        self._checkTag(svnpath+'/'+self.tag)

        self._checkoutCactus(svnpath)

        self._getEmpty(self.tag)

        subdirs = ['boards','components']
        self._getsubdirs( subdirs )

class WorkAreaBuilder(Plugin):

    @classmethod
    def getOptions(cls,parser):
        description = "This is to make the working area"
        group = optparse.OptionGroup(parser,cls.__name__, description)
        Plugin.addStandardOptions(group)
        group.add_option('-b','--board' , help='mp7 board to build (%default)', default='mp7_690es')
        return group

    @classmethod
    def validate(cls,opts,args):
        pass

    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            print k,v
            setattr(self,k,v)

        self.cactusRoot = os.path.realpath(self.prefix+'/cactus')
        self.tagRoot = os.path.join(self.cactusRoot, self.tag)


    def execute(self):
        print 'Building working area for',self.board

        links=[
            'boards/mp7/base_fw/%s' % self.board,
            'boards/mp7/base_fw/sim',
            'boards/mp7/base_fw/common',
            'components/ipbus',
            'components/mp7_algo',
            'components/mp7_buffers',
            'components/mp7_counters',
            'components/mp7_ctrl',
            'components/mp7_i2c',
            'components/mp7_mezzanine',
            'components/mp7_links',
            'components/mp7_preproc',
            'components/mp7_spi',
            'components/mp7_ttc',
            'components/mp7_xpoint',
            'components/opencores_i2c',
        ]

        if not os.path.exists(self.tagRoot):
            raise RuntimeError('tag directory %s doesn\'t exist' % self.tagRoot)

        os.system('mkdir -p %s' % self.board)

        sentry = DirSentry(self.board)

        print 'making links'
        for link in links:
            os.system('ln -s %s/%s' % (self.tagRoot,link) )

        print 'making environment scripts'
        script = '''
HERE=$(dirname $(readlink -f $BASH_SOURCE) )
export REPOS_FW_DIR=${HERE}
export REPOS_BUILD_DIR=${HERE}/%s/ise14
        '''

        workEnv = open('env_work.sh','w')
        workEnv.write(script % self.board)
        workEnv.close()

        script = '''
HERE=$(dirname $(readlink -f $BASH_SOURCE) )
export REPOS_FW_DIR=${HERE}
export REPOS_BUILD_DIR=${HERE}/sim/cfg
        '''

        simEnv = open('env_sim.sh','w')
        simEnv.write(script)
        simEnv.close()

        print 'making working areas and Makefiles'
        os.system('mkdir -p work')

        makefile = '''
.setup:
\t. $(REPOS_FW_DIR)/ipbus/firmware/example_designs/scripts/setup.sh

.build:
\txtclsh $(REPOS_BUILD_DIR)/build_project.tcl

.clean:
\tls | grep -v Makefile  | xargs rm -rf

all:
\t@echo "No default target. Choose among 'setup','build','clean'"

setup: .setup

build: .build

clean: .clean

.PHONY: setup build clean .install .build .clean
        '''
        wkMake = open('work/Makefile','w')
        wkMake.write(makefile)
        wkMake.close()

        os.system('mkdir -p modelsim')

        makefile='''

.setup:
\t. $(REPOS_FW_DIR)/ipbus/firmware/sim/scripts/setup.sh

.clean:
\tls | grep -v Makefile  | xargs rm -rf

all:
\t@echo "No default target. Choose among 'setup','clean'"

setup: .setup

clean: .clean

.PHONY: setup build clean .install .build .clean

        '''

        msMake = open('modelsim/Makefile','w')
        msMake.write(makefile)
        msMake.close()


#---
plugins = {
    'svnco':SvnDownloader,
    'work' :WorkAreaBuilder
}


if __name__ == '__main__':

    pcls, opts, args = parse_args()

    print pcls, opts, args

    pinst = pcls(**vars(opts))
    pinst.execute()




