#!/usr/bin/env python
# ------------------------------------------------------------------------
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
 
import time
import sys
import os
import stomp
from signal import signal, SIGINT

user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
host = os.getenv("ACTIVEMQ_HOST") or "localhost"
port = os.getenv("ACTIVEMQ_PORT") or 61613
destination = sys.argv[1:2] or ["/topic/event"]
destination = destination[0]

messages = 10000
data = "Hello World from Python"

def handler(signal_received, frame):
  # Handle any cleanup here
  print('SIGINT or CTRL-C detected. Exiting gracefully')
  conn.send(destination, "SHUTDOWN", persistent='false')
  conn.disconnect()
  sys.exit(0)

if __name__ == '__main__':
  # Tell Python to run the handler() function when SIGINT is recieved
  signal(SIGINT, handler)

  print('Running. Press CTRL-C to exit.')

  conn = stomp.Connection(host_and_ports = [(host, port)])
  conn.start()
  conn.connect(login=user,passcode=password)

  while True:
    for i in range(messages):
      conn.send(destination, data, persistent='false')

    time.sleep(10)