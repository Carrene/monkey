# monkey

Scalable IBM Websphere MQ multi-thread scheduler.

## Prerequisites

`IBM WebSphere 8.0`

Download the `mqadv_dev80_linux_x86-64.tar.gz` from [IBM Website](https://developer.ibm.com/messaging/mq-downloads/)
NOTICE THAT: You should download developer version IBM message queue

```bash
sudo apt-add-repository universe
sudo apt-get install rpm pax
mkdir mq8
tar xvzf mqadv_dev80_linux_x86-64.tar.gz -C mq8
cd mq8
mkdir rpms
sudo ./mqlicense.sh -text_only
sudo -H TMPDIR=$(readlink -f rpms) ./crtmqpkg mq
sudo rpm -ivh --nodeps --force-debian rpms/mq_rpms/mq/x86_64/MQSeriesRuntime*.rpm
sudo rpm -ivh --nodeps --force-debian rpms/mq_rpms/mq/x86_64/MQSeriesServer*.rpm
for pkg in rpms/mq_rpms/mq/x86_64/*.rpm; do sudo rpm -ivh --nodeps --force-debian $pkg; done

```

## Setup a MQ server for testing purposes:

Issue some variables to configure unittests:

```bash
source /opt/mqm/bin/setmqenv -s
export TEST_QUEUEMANAGER="TEST.QM"
export TEST_QUEUE="TEST.QUEUE"
export TEST_CHANNEL="TEST.CHANNEL"
export TEST_HOST="127.0.0.1"
export TEST_PORT="8000"
```

Create and start the `Queue Manager`.

```bash
sudo -u mqm /opt/mqm/bin/crtmqm ${TEST_QUEUEMANAGER}
sudo -u mqm /opt/mqm/bin/strmqm ${TEST_QUEUEMANAGER}
```

Create the queue.

```bash
echo "DEFINE QLOCAL (${TEST_QUEUE})" | sudo -u mqm runmqsc ${TEST_QUEUEMANAGER}
crtmqm ${TEST_QUEUE}
```

#### TCP Listener


Configure the `QueueManager` to listen on TCP.

```bash
echo "
DEFINE CHL(${TEST_CHANNEL}) CHLTYPE(SVRCONN)
DEFINE LISTENER(TCP.LISTENER.1) TRPTYPE(TCP) PORT(${TEST_PORT}) CONTROL(QMGR) REPLACE
START LISTENER(TCP.LISTENER.1)
ALTER QMGR CHLAUTH(DISABLED)
" | sudo -u mqm runmqsc ${TEST_QUEUEMANAGER}
```

Permissions

```bash
sudo -u mqm setmqaut -m ${TEST_QUEUEMANAGER} -t qmgr -p mqm +all
sudo -u mqm setmqaut -m ${TEST_QUEUEMANAGER} -t queue -p mqm -n ${TEST_QUEUE} +all
echo "REFRESH SECURITY" | sudo -u mqm runmqsc ${TEST_QUEUEMANAGER}
```


#### Finally issue the `MQSERVER`:

```bash
export MQSERVER="${TEST_CHANNEL}/TCP/${TEST_HOST}(${TEST_PORT})"
```

```bash
cd /opt/mqm/samp/bin/
./amqsget ${TEST_QUEUE} ${TEST_QUEUEMANAGER}
```

Open another terminal and check the `amqsgetc` output:
```bash
cd /opt/mqm/samp/bin/
echo "HI" | ./amqsput ${TEST_QUEUE} ${TEST_QUEUEMANAGER}
```


## IBM websphere useful commands
NOTICE THAT: Add the binaries to PATH:
```bash 
echo "export PATH=$PATH:/opt/mqm/bin"
echo "export PATH=$PATH:/opt/mqm/samp/bin"
source .bashrc
```
+ Create a queue manager:
```bash 
crtmqm $QUEUE_MANAGER_NAME
```

+ Delete a queue manager:
```bash
dltmqm $QUEUE_MANAGER_NAME
```

+ Start a queue manager
```bash
strmqm $QUEUE_MANAGER_NAME
```

+ Stopping queue manager:
You can wait for queue manager to shutdown:
```bash
endmqm -w $QUEUE_MANAGER_NAME
```
Or you can shut it down immediately:
```bash
endmqm -i $QUEUEU_MANAGER_NAME
```

+ In order to run a message queue as a service save the follwoing configuration
    on `/etc/systemd/system/mq@.service`

```bash
[Unit]
Description=IBM MQ V8 queue manager %I
After=network.target
[Service]
ExecStart=/opt/mqm/bin/strmqm %I
ExecStop=/opt/mqm/bin/endmqm -w %I
Type=forking
User=mqm
Group=mqm
KillMode=none
LimitNOFILE=10240
LimitNPROC=4096
[Install]
WantedBy=multi-user.target
```

+ Reload deamons:
```bash
systemctl daemon-reload
```

+ To start your queue manager use the following commands:
```bash
systemctl start mq@<QUEUE_MANAGER_NAME>.service
```

+ Display queue managers and their status:
```bash
dspmq
```

#### Write, pop and monitor messages in queue

+ Write a message in queue:
```bash
echo "MESSAGE" | amqsput $QUEUE_NAME $QUEUE_MANAGER_NAME
```

+ Get messages off a queue:
```bash
amqsget $QUEUE_NAME $QUEUE_MANAGER_NAME
```

+ Browse, in order to monitor messages in a queue:
```bash
amqsbcg $QUEUE_NAME $QUEUE_MANAGER_NAME
```
