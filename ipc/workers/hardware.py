import time
import re
import ipc
import subprocess

class status(ipc.daemon.Demonize):
  def temperature(self):
    bash = '/opt/vc/bin/vcgencmd measure_temp'
    process = subprocess.run(bash.split(), capture_output=True)
    stdout = process.stdout.decode('utf-8')
    return self.response("%s°C" % re.findall(r'\d+', stdout)[0])

  def voltage(self):
    bash = '/opt/vc/bin/vcgencmd measure_volts core'
    process = subprocess.run(bash.split(), capture_output=True)
    stdout = process.stdout.decode('utf-8')
    return self.response("%sV" % ''.join(re.findall(r'\d+', stdout)))
