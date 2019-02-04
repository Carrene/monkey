import pymqi
import time
from khayyam import JalaliDatetime as datetime

# export MQSERVER="ServerChannel/TCP/192.168.163.167(1418)"
# sudo -Eu mqm LD_LIBRARY_PATH=/opt/mqm/bin/lib64:/opt/mqm/bin/lib:/opt/mqm/ \
#    lib64:/usr/lib64 /home/vahid/.virtualenvs/pymqi/bin/python ./isc.py

# export MQSERVER="CHANN1/TCP/192.168.1.70(9000)"
queue_manager = 'TEST.QM'
channel = 'TEST.CHANNEL'
user = 'mqm'
password = '123'
queue = 'TEST.QUEUE'


qm = pymqi.connect(queue_manager, channel=channel, user=user, password=password)
putq = pymqi.Queue(qm, queue)


for i in range(100000):
  msg = '<token-register-bmi unique-id="%sSOTPREGISTER%06d" \
      phone-no="09123456789" source="SOTP-BMI-KAKISH" key="24567" />' % (
      datetime.now().strftime('%Y%m%d%H%M%S'), i
  )
  print(msg)
  putq.put(msg)


