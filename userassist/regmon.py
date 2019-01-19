import codecs
import hashlib
import logging
import win32api
import win32con
import win32event
import threading
import datetime
from box import Box
from userassist.userassist import UserAssist

LOGGER = logging.getLogger(__name__)

# Notify the caller of changes to a value of the key. This can include adding or deleting a value, or changing an existing value
win32api.REG_NOTIFY_CHANGE_LAST_SET
# Notify the caller if a subkey is added or deleted
win32api.REG_NOTIFY_CHANGE_NAME


def get_handle_mapping(user_assist_key, callback):
    mapping = {}
    sub_key_count, value_count, mod_time = win32api.RegQueryInfoKey(
        user_assist_key
    )
    for guid_index in range(sub_key_count):
        guid_name = win32api.RegEnumKey(
            user_assist_key,
            guid_index
        )
        LOGGER.info("Enumerating {}".format(guid_name))

        guid_count_key = win32api.RegOpenKeyEx(
            user_assist_key,
            guid_name + "\\Count",
            0,
            win32con.KEY_READ
        )

        mapping[guid_name] = MonitoredKey(
            guid_name,
            guid_count_key,
            callback
        )

    return mapping


class ValueCache(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def get_change(self, other):
        value = {k: other[k] for k, _ in set(other.items()) - set(self.items())}
        return value


class MonitoredKey(threading.Thread):
    def __init__(self, name, key_handle, callback):
        threading.Thread.__init__(self)
        self.name = name
        self.key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{}\\Count".format(
            self.name
        )
        self.key_handle = key_handle
        self.event = win32event.CreateEvent(
            None, False, False, self.name
        )
        self.callback = callback
        self.handle_original()

    def handle_original(self):
        current_values = self.enum_values()
        for key in current_values.keys():
            decoded_key = codecs.decode(key, 'rot-13')
            record = {
                "guid": self.name,
                "timestamp": "current",
                "key_name": self.key_path,
                "value_name": key,
                "value_decoded_name": decoded_key
            }

            value_data, value_type = win32api.RegQueryValueEx(
                self.key_handle,
                key
            )

            if len(value_data) >= 68:
                user_assist = UserAssist(
                    value_data
                )
                record.update(
                    user_assist.as_dict()
                )
                self.callback(
                    Box(record)
                )

    def run(self):
        old_cache = self.enum_values()
        while True:
            win32api.RegNotifyChangeKeyValue(
                self.key_handle,
                True,
                win32api.REG_NOTIFY_CHANGE_LAST_SET,
                self.event,
                True
            )

            # Check for event signal
            event_signal = win32event.WaitForSingleObject(
                self.event, 1
            )

            if event_signal == 0:
                # Event has been signalled
                new_cache = self.enum_values()
                this = old_cache.get_change(new_cache)

                for key, hash in this.items():
                    decoded_key = codecs.decode(key, 'rot-13')
                    record = {
                        "guid": self.name,
                        "timestamp": datetime.datetime.utcnow().time().strftime("%H:%M:%S"),
                        "key_name": self.key_path,
                        "value_name": key,
                        "value_decoded_name": decoded_key
                    }

                    value_data, value_type = win32api.RegQueryValueEx(
                        self.key_handle,
                        key
                    )

                    if len(value_data) >= 68:
                        user_assist = UserAssist(
                            value_data
                        )
                        record.update(
                            user_assist.as_dict()
                        )
                        self.callback(
                            Box(record)
                        )

                win32event.ResetEvent(self.event)
                win32api.RegNotifyChangeKeyValue(
                    self.key_handle,
                    True,
                    win32api.REG_NOTIFY_CHANGE_LAST_SET,
                    self.event,
                    True
                )

                old_cache = new_cache

    def enum_values(self):
        sub_key_count, value_count, mod_time = win32api.RegQueryInfoKey(
            self.key_handle
        )

        values = {}
        for value_index in range(value_count):
            value_name, value_object, value_type = win32api.RegEnumValue(
                self.key_handle,
                value_index
            )
            value_hash = hashlib.md5(value_object).hexdigest()
            values[value_name] = value_hash

        return ValueCache(values)

    def print_cache(self):
        for value_name, value_hash in self.cache.items():
            print("name: {}, hash: {}".format(value_name, value_hash))

    def __del__(self):
        LOGGER.debug("Closing Monitored Key".format(self.name))
        win32api.RegCloseKey(
            self.key_handle
        )


class UserAssistMonitor(threading.Thread):
    def __init__(self, callback):
        user_assist_key = win32api.RegOpenKeyEx(
            win32con.HKEY_CURRENT_USER,
            "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist",
            0,
            win32con.KEY_READ
        )
        self.guid_count_key_mapping = get_handle_mapping(
            user_assist_key,
            callback
        )
        threading.Thread.__init__(self)

    def run(self):
        event_handles = {}
        for guid_name, monitored_key in self.guid_count_key_mapping.items():
            monitored_key.start()

        while True:
            pass
