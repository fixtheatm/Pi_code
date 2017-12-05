import threading
import datetime


class Sensor(object):
    """
    Basic sensor object that all others should extend. Provides support for collecting sensor values, monitoring a
    sensor for changes, and writing sensor values to file to be picked up by the send_json_to_server.sh script.

    All extending classes will need to implement get_value() or _monitor_value().
    """
    json_folder = '/usr/local/bin/BioReactor/'
    device_id = '00002'

    def __init__(self):
        self.continue_monitor = False
        self.monitor_thread = None

    def get_value(self):
        """
        Gets the current value of the sensor.
        :return: The value for the sensor at the current time.
        """
        raise NotImplementedError("Get value method for sensor not yet implemented.")

    def start_monitor(self, callback):
        """
        Starts the sensor monitor with the given callback.
        """
        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self.continue_monitor = True
            self.monitor_thread = threading.Thread(target=self._monitor_value, args=(callback,))
            self.monitor_thread.start()

    def stop_monitor(self, wait_for_stop=False):
        """
        Stops the monitor thread.
        :param wait_for_stop: Whether the method should wait for the monitor to stop before returning. If false, will
                              return immediately.
        """
        self.continue_monitor = False
        if wait_for_stop:
            self.wait_monitor()

    def wait_monitor(self):
        """
        Causes the calling thread to wait/sleep for as long as the monitor is running. Useful for when you want to start
        a monitor and have no need to stop it.
        """
        if self.monitor_thread is not None and self.monitor_thread.is_alive():
            self.monitor_thread.join()

    def _monitor_value(self, callback):
        """
        Watches a sensor for a trigger behavior that when seen, will run the given callback function with the sensor
        value or state as a parameter. This should have an infinite loop that runs as long as continue_monitor is true.
        :param callback:
        :return:
        """
        raise NotImplementedError("Monitor value method for sensor not yet implemented.")

    @staticmethod
    def generate_file(value_name, value, json_prefix, json_time):
        """
        Takes a sensor value and current time and creates a json file ready to be sent to the server.
        :param value_name: The name the server expects to be paired with the sensor value. E.g. 'temperature' or 'lux'.
        :param value: The value to send to the server. If not already a string, will be convered to one with str(value)
        :param json_prefix: The prefix to use for the json file name. E.g. 'bio_temp' or 'bio_light'
        :param json_time: The time to use for the json file name as well as the json 'recorded_on' parameter.
        """

        file_time = json_time.strftime( '%Y%m%d_%H%M%S' )
        recorded_on = json_time.strftime( '%Y-%m-%d %H:%M:%S' )
        json_file = '{}{}_{}.json'.format(Sensor.json_folder, json_prefix, file_time)
        value_str = str(value)

        print("Starting write to file: ", json_file)
        with open(json_file, 'w') as f:
            file_str = '[{' + '"deviceid":"{}","{}":"{}","recorded_on":"{}"'.format(Sensor.device_id, value_name, value_str, recorded_on) +'}]\n'
            f.write(file_str)
        # Append data value to log.
        log_file = "datalog/"+json_prefix+".csv"
        with open(log_file, 'a') as log_f:
            log_f.write(recorded_on + "," + value_str + "\n")
        
