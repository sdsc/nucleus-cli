
CM=~/github/cloudmesh
mkdir -p $CM
cd $CM
git clone git@github.com:cloudmesh/cmd3light
git clone git@github.com:cloudmesh/client.git
cd $CM/client
python setup.py install
cd $CM/client
python setup.py cmd3light
