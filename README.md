# monkey

Scalable IBM Websphere MQ multi-thread scheduler.

## Prerequisites

`IBM WebSphere 8.0`

Download the `mqadv_dev80_linux_x86-64.tar.gz` from [IBM Website](https://developer.ibm.com/messaging/mq-downloads/)
NOTICE THAT: You should download developer version

```bash
sudo apt-add-repository universe
sudo apt-get install rpm pax
mkdir mq8
tar -xvf mqadv_dev80_linux_x86-64.tar.gz -C mq75
cd mq8
mkdir rpms
sudo ./mqlicense.sh -text_only
sudo -H TMPDIR=$(readlink -f rpms) ./crtmqpkg mq
sudo rpm -ivh --nodeps --force-debian rpms/mq_rpms/mqipy/x86_64/MQSeriesRuntime*.rpm
sudo rpm -ivh --nodeps --force-debian rpms/mq_rpms/mqipy/x86_64/MQSeriesServer*.rpm
for pkg in rpms/mq_rpms/mqipy/x86_64/*.rpm; do sudo rpm -ivh --nodeps --force-debian $pkg; done
```

## Setup a MQ server for testing purposes:

Issue some variables to configure unittests:

```bash
source /opt/mqm/bin/setmqenv -s
export MQIPY_TEST_QUEUEMANAGER="TEST.QM"
export MQIPY_TEST_QUEUE="TEST.QUEUE"
export MQIPY_TEST_CHANNEL="TEST.CHANNEL"
export MQIPY_TEST_HOST="127.0.0.1"
export MQIPY_TEST_PORT="8000"
```

Create and start the `QueueManager`.

```bash
sudo -u mqm /opt/mqm/bin/crtmqm ${MQIPY_TEST_QUEUEMANAGER}
sudo -u mqm /opt/mqm/bin/strmqm ${MQIPY_TEST_QUEUEMANAGER}
```

Create the queue.

```bash
echo "DEFINE QLOCAL (${MQIPY_TEST_QUEUE})" | sudo -u mqm runmqsc ${MQIPY_TEST_QUEUEMANAGER}
```

#### TCP Listener


Configure the `QueueManager` to listen on TCP.

```bash
echo "
DEFINE CHL(${MQIPY_TEST_CHANNEL}) CHLTYPE(SVRCONN)
DEFINE LISTENER(TCP.LISTENER.1) TRPTYPE(TCP) PORT(${MQIPY_TEST_PORT}) CONTROL(QMGR) REPLACE
START LISTENER(TCP.LISTENER.1)
ALTER QMGR CHLAUTH(DISABLED)
" | sudo -u mqm runmqsc ${MQIPY_TEST_QUEUEMANAGER}
```

Permissions

```bash
sudo -u mqm setmqaut -m ${MQIPY_TEST_QUEUEMANAGER} -t qmgr -p mqm +all
sudo -u mqm setmqaut -m ${MQIPY_TEST_QUEUEMANAGER} -t queue -p mqm -n ${MQIPY_TEST_QUEUE} +all
echo "REFRESH SECURITY" | sudo -u mqm runmqsc ${MQIPY_TEST_QUEUEMANAGER}
```


#### Finally issue the `MQSERVER`:

```bash
export MQSERVER="${MQIPY_TEST_CHANNEL}/TCP/${MQIPY_TEST_HOST}(${MQIPY_TEST_PORT})"
```

```bash
cd /opt/mqm/samp/bin/
./amqsget ${MQIPY_TEST_QUEUE} ${MQIPY_TEST_QUEUEMANAGER}
```

Open another terminal and check the `amqsgetc` output:
```bash
cd /opt/mqm/samp/bin/
echo "HI" | ./amqsput ${MQIPY_TEST_QUEUE} ${MQIPY_TEST_QUEUEMANAGER}
```
