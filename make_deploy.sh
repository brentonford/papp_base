#!/bin/sh

set -o nounset
set -o errexit
set -x


echo "start version is $VER"

PAPP_NAME='papp_noop'

BUILD="${BUILD}"
VER="${VER}"
DATE="`date --utc`"

if [ "${VER}" != '${bamboo.jira.version}' ]; then
    TAR_DIR="${PAPP_NAME}_$VER"
else
    VER="b`date +%y%m%d.%H%M`"
    TAR_DIR="${PAPP_NAME}_$VER#$BUILD"
fi

DIR="deploy/$TAR_DIR"
mkdir -p $DIR

echo "New version is $VER"

# REMOVE ME, Temparary fix for
cp peek_agent_pof/src/run_peek_agent.py $DIR/run_agent.py

# REMOVE ME, Temportary fix for agent oracle recompile
( cd $DIR && wget 'https://pypi.python.org/packages/95/7f/3b74fe3adeb5948187b760330cb7e9175e3484bd6defdfeb9b504d71b4b3/cx_Oracle-5.2.1.tar.gz#md5=65a6bcc5217a9502c10e33fcea2982f3' )


# Source
cp -pr papp_base/src/peek_agent $DIR
cp -pr ${PAPP_NAME}/src/${PAPP_NAME} $DIR
cp -pr ${PAPP_NAME}/papp_changelog.txt $DIR
cp -pr ${PAPP_NAME}/papp_version.txt $DIR


find $DIR -iname .git -exec rm -rf {} \; || true
find $DIR -iname "test" -exec rm -rf {} \; 2> /dev/null || true
find $DIR -iname "tests" -exec rm -rf {} \; 2> /dev/null || true
find $DIR -iname "*test.py" -exec rm -rf {} \; || true
find $DIR -iname "*tests.py" -exec rm -rf {} \; || true
find $DIR -iname ".Apple*" -exec rm -rf {} \; || true
find $DIR -iname "*TODO*" -exec rm -rf {} \; || true
find $DIR -iname ".idea" -exec rm -rf {} \; || true


# Apply version number

for f in `grep -l -r  '#PAPP_VER#' .`; do
    echo "Updating version in file $f"
    sed -i "s/#PAPP_VER#/$VER/g" $f
done

for f in `grep -l -r  '#PAPP_BUILD#' .`; do
    echo "Updating build in file $f"
    sed -i "s/#PAPP_BUILD#/$BUILD/g" $f
done

for f in `grep -l -r  '#BUILD_DATE#' .`; do
    echo "Updating date in file $f"
    sed -i "s/#BUILD_DATE#/$DATE/g" $f
done

echo "Compiling all python modules"
( cd $DIR && python -m compileall -f . )

echo "Deleting all source files"
find $DIR -name "*.py" -exec rm {} \;

tar cjf ${TAR_DIR}.tar.bz2 -C deploy $TAR_DIR
