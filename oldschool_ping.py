"""
The following code leverages the os.system() function
to ping all the old school runescape worlds and generate
a report with sorted ping times.
"""
import os
import re
import time
import datetime


class OldSchoolPing(object):
    def __init__(self):
        """
        Initializes world number range and results container.
        """
        self.worlds_list = range(1, 94)
        self.world_info = {}
        self.dns_pattern = re.compile(r'Pinging ([^ []*) .*')
        self.time_pattern = re.compile(r'\btime=(\d*)ms\b')
        self.report_name = r'_ping_results.log'

    def ping_worlds(self):
        for num in self.worlds_list:
            # Keeping track of world info via list/dict combo
            self.world_info['oldschool_{}'.format(num)] = {
                'dns_pattern': '',
                'ping_times': [],
            }
            # Carrying out actual ping
            os.system(r'START /B cmd /c "ping oldschool{0}.runescape.com -n 5 > oldschool_{0}"'.format(num))
        # Little pause to give processes time to fully complete.
        time.sleep(10)
        for item in self.world_info:
            # Resetting ping details
            server_dns_name = ''
            ping_time = ''
            ping_times = []
            # Parsing ping times from generated files
            with open(item) as _f:
                for line in _f:
                    # Getting DNS name (world number does not seem to match actual world)
                    server_dns_name = self.dns_pattern.findall(line)
                    if server_dns_name:
                        self.world_info[item]['dns_pattern'] = server_dns_name[0]
                    ping_time = self.time_pattern.findall(line)
                    if ping_time:
                        ping_times.append(int(ping_time[0]))
            # Computing average and storing in world_info dict
            if len(ping_times) > 0:
                self.world_info[item]['ping_times'] = sum(ping_times) / len(ping_times)

    def generate_report(self):
        """
        Sorts key/value pairs generated by the ping_worlds() method, and
        creates a results report using the objects report_name attr.
        """
        sorted_list = sorted(self.world_info, key=lambda x: (self.world_info[x]['ping_times']))
        # print(sorted_list)
        with open(self.report_name, 'w') as _w:
            _w.write('=======================================\n')
            _w.write('## Report Generation: {}\n'.format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
            _w.write('=======================================\n\n\n')
            for item in sorted_list:
                _w.write('{:<15} {:<35} {:<5}\n'.format(
                    item + ':',
                    self.world_info[item]['dns_pattern'],
                    self.world_info[item]['ping_times'])
                )
                _w.write('-' * 56 + '\n')


if __name__ == '__main__':
    ping_obj = OldSchoolPing()
    ping_obj.ping_worlds()
    ping_obj.generate_report()
