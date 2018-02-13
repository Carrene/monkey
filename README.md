# monkey

Scalable IBM Websphere MQ multi-thread scheduler.

## Prerequisites

`IBM WebSphere 7.5` is required to build and install the `pymqi`

Download the `mqadv_dev75_linux_x86-64.tar.gz` from [IBM Website](https://www.ibm.com/developerworks/community/blogs/messaging/entry/develop_on_websphere_mq_advanced_at_no_charge?lang=en)

Following the https://www.ibm.com/support/knowledgecenter/en/SSFKSJ_7.5.0/com.ibm.mq.ins.doc/q115250_.htm

```bash
sudo apt-get install rpm pax
mkdir mq75
tar -xvf mqadv_dev75_linux_x86-64.tar.gz -C mq75
cd mq75
mkdir rpms
sudo ./mqlicense.sh -text_only
sudo ./crtmqpkg mqipy
sudo -H TMPDIR=$(readlink -f rpms) ./crtmqpkg mqipy
sudo rpm -ivh --nodeps --force-debian rpms/mq_rpms/mqipy/x86_64/MQSeriesRuntime_mqipy-*.rpm
sudo rpm -ivh --nodeps --force-debian rpms/mq_rpms/mqipy/x86_64/MQSeriesServer_mqipy-*.rpm
for i in rpms/mq_rpms/mqipy/x86_64/*.rpm; do sudo rpm -ivh --nodeps --force-debian $i; done
 
sysctl -w net.ipv4.tcp_keepalive_time=300
echo "net.ipv4.tcp_keepalive_time=300" | sudo tee -a /etc/sysctl.conf > /dev/null
echo "mqm soft nofile 10240" | sudo tee -a /etc/security/limits.conf > /dev/null
sudo su mqm -c "/opt/mqm/bin/mqconfig"
```

## Installation

```bash
cd path/to/monkey
pip install path/to/monkey
```

## Running

```bash
LD_LIBRARY_PATH=/opt/mqm/lib64 monkey
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
sudo -u mqm crtmqm ${MQIPY_TEST_QUEUEMANAGER}
sudo -u mqm strmqm ${MQIPY_TEST_QUEUEMANAGER}
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
./amqsgetc ${MQIPY_TEST_QUEUE} ${MQIPY_TEST_QUEUEMANAGER}
```

Open another terminal and check the `amqsgetc` output:
```bash
cd /opt/mqm/samp/bin/
echo "HI" | ./amqsputc ${MQIPY_TEST_QUEUE} ${MQIPY_TEST_QUEUEMANAGER}
```
