#!/usr/bin/env python
#coding:utf-8

from kafka import KafkaProducer
import time
import sys

def prn_obj(obj): 
  print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()]) 

if __name__ == '__main__':
  if len(sys.argv) < 5:
    print("para topic and pid and sleep interval and  send times are needed!!!")
    sys.exit()
  topic=sys.argv[1]
  pid=sys.argv[2]
  sleep_interval=sys.argv[3]
  send_times=sys.argv[4]
  try:
    DEFAULT_CONFIG = { 
      'key_serializer': None,  #key���л���ʽ
      'value_serializer': None, #key���л���ʽ
      'acks': 1,   #���͵���Ϣ��ȷ����ʽ��1������Ҫleaderȷ��
      'compression_type': None, #ѹ����ʽ
      'retries': 0, #���Դ���
      'buffer_memory': 33554432, #buffer�Ĵ�С,��batch_size���
      'batch_size': 65536,  #�������͵Ĵ�С
      'linger_ms': 1000,  #���ڵ�ʱ��
      'connections_max_idle_ms': 9 * 60 * 1000,
      'request_timeout_ms': 3000,
      'receive_buffer_bytes': None,
      'send_buffer_bytes': None,
      'reconnect_backoff_ms': 50,
      'reconnect_backoff_max': 1000,
      'max_block_ms': 10000,
      'max_request_size': 131072
    }
    #������,Ŀǰ���г涴��server��ַ��һ��
    DEFAULT_CONFIG['bootstrap_servers']='cdmqszentry01.data.mig:10005,cdmqszentry02.data.mig:10069'
    #����id,cdmqҳ�������������
    DEFAULT_CONFIG['client_id']=pid
    producer=KafkaProducer(**DEFAULT_CONFIG)
    #����֧�ֵĲ������Բμ��ٷ��ĵ�https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
    for i in range(send_times):
      data="hello world"
      futureRecordMetadata=producer.send(topic, data)
      timestamp=int(time.time())
      recordMetadata=futureRecordMetadata.get()
      print('data send succeed!! timestamp:{},topic:{},partition:{},offset:{}'.format(timestamp,recordMetadata.topic,recordMetadata.partition,recordMetadata.offset))      
      time.sleep(sleep_interval)
  except Exception as e:
    print(str(e))
