import struct
import datetime


class UserAssist(object):
    """
    Structure resources:
    https://github.com/EricZimmerman/RegistryPlugins/blob/8822318182ec28a385a9544422d8ae4d14df7fd9/RegistryPlugin.UserAssist/UserAssist.cs#L79
    https://www.aldeid.com/wiki/Windows-userassist-keys
    https://github.com/keydet89/RegRipper2.8/blob/master/plugins/userassist_tln.pl#L85
    """
    def __init__(self, buf):
        self.session = struct.unpack("<I", buf[0:4])[0]
        self.run_count = struct.unpack("<I", buf[4:8])[0]
        self.focus_count = struct.unpack("<I", buf[8:12])[0]
        self.focus_time = struct.unpack("<I", buf[32:36])[0]

        u64_timestamp = struct.unpack("<Q", buf[60:68])[0]
        self.last_execution = datetime.datetime(1601, 1, 1) + datetime.timedelta(
            microseconds=u64_timestamp / 10
        )

    def as_dict(self):
        return {
            "session": self.session,
            "run_count": self.run_count,
            "focus_count": self.focus_count,
            "focus_time": self.focus_time,
            "last_execution": self.last_execution.isoformat(" ")
        }
