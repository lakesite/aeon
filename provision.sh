#!/bin/sh

if [ ! -e "/home/vagrant/provisioned" ]
then
    apt-get update
    apt-get -y upgrade
    apt-get -y install supervisor git python3 python3-dev python3-setuptools python3-pip python-virtualenv mysql-client

    # Mysql install
    echo 'mysql-server mysql-server/root_password password aeon' | debconf-set-selections
    echo 'mysql-server mysql-server/root_password_again password aeon' | debconf-set-selections
    apt-get install -y mysql-server-5.5 > /dev/null 2>&1

    # Mysql setup
    mysqladmin -uroot -paeon create aeon || exit 1
    mysql -uroot -paeon -Bse "create user 'aeon'@'localhost' identified by 'aeon';"
    mysql -uroot -paeon -Bse "grant all privileges on \`aeon\`.* to 'aeon'@'localhost';"
    mysqladmin -uroot -paeon flush-privileges || exit 1

    # Install the virtualenv in ~vagrant but the project in /vagrant.
    sudo -u vagrant -s <<'EOF' || exit 1
cd /vagrant/
virtualenv -p /usr/bin/python3.4 /home/vagrant/env
source /home/vagrant/env/bin/activate
pip install -r requirements.txt
EOF

    cat <<'EOF' > /etc/supervisor/conf.d/runserver.conf
[program:runserver]
command=/home/vagrant/env/bin/python manage.py runserver 0.0.0.0:8000
directory=/vagrant/aeon_project
autostart=0
EOF
    supervisorctl reload || exit 1

    touch /home/vagrant/provisioned
fi

supervisorctl start runserver
