#CACTUSDIR="tags/mp7_july_130723a"
CACTUSDIR="trunk"

HERE=$(dirname $(readlink -f $BASH_SOURCE) )
BOARD=mp7_690es

links=()
links+=(boards/mp7/base_fw/${BOARD})
links+=(boards/mp7/base_fw/sim)
links+=(components/ipbus)
links+=(components/mp7_algo)
links+=(components/mp7_buffers)
links+=(components/mp7_counters)
links+=(components/mp7_i2c)
links+=(components/mp7_ctrl)
links+=(components/mp7_ttc)
links+=(components/mp7_xpoint)
links+=(components/opencores_i2c)
links+=(components/mp7_mgt)

mkdir -p ${BOARD}
cd ${BOARD}

for i in ${links[@]}; do
ln -s ${HERE}/cactus/$i
done


cat > env_work.sh << EOF
HERE=\$(dirname \$(readlink -f \$BASH_SOURCE) )
export REPOS_FW_DIR=\${HERE}
export REPOS_BUILD_DIR=\${HERE}/${BOARD}/ise14
EOF

cat > env_sim.sh << EOF
HERE=\$(dirname \$(readlink -f \$BASH_SOURCE) )
export REPOS_FW_DIR=\${HERE}
export REPOS_BUILD_DIR=\${HERE}/sim/cfg
EOF

mkdir -p work

cat > work/Makefile << EOF

.setup:
	. \$(REPOS_FW_DIR)/ipbus/firmware/example_designs/scripts/setup.sh

.build:
	xtclsh \$(REPOS_BUILD_DIR)/build_project.tcl

.clean:
	ls | grep -v Makefile  | xargs rm -rf

all:
	echo "Choose target"

setup: .setup

build: .build

clean: .clean

.PHONY: setup build clean .install .build .clean

EOF

mkdir -p modsim
cat > modsim/Makefile << EOF

.setup:
	. \$(REPOS_FW_DIR)/ipbus/firmware/sim/scripts/setup.sh

.clean:
	ls | grep -v Makefile  | xargs rm -rf

all:
	echo "Choose target"

setup: .setup

clean: .clean

.PHONY: setup build clean .install .build .clean

EOF



cd $HERE
