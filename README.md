# MonitorUserAssist
Tool that can monitor the UserAssist registry keys and decode UserAssist structs in real-time.

# scripts/usrasst_mon.py
```
usage: usrasst_mon.py [-h] [--format FORMAT] [--debug {ERROR,WARN,INFO,DEBUG}]

Monitor UserAssist Registry Keys. This tool will also display current values before monitoring starts.
Version: 0.1.0


optional arguments:
  -h, --help            show this help message and exit
  --format FORMAT       Python fstring.
  --debug {ERROR,WARN,INFO,DEBUG}
                        Debug level [default=ERROR]
```

Available keys:
```json
{
	"guid": "{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}",
	"timestamp": "current",
	"key_name": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}\\Count",
	"value_name": "{0139Q44R-6NSR-49S2-8690-3QNSPNR6SSO8}\\Nqzvavfgengvir Gbbyf\\Flfgrz Pbasvthengvba.yax",
	"value_decoded_name": "{0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}\\Administrative Tools\\System Configuration.lnk",
	"session": 5,
	"run_count": 0,
	"focus_count": 0,
	"focus_time": 3212836864,
	"last_execution": "2018-12-31 18:14:00.080000"
}

```

My favorite format: `"[{record.timestamp} {record.guid}] last_execution: {record.last_execution} run_count: {record.run_count} focus_count: {record.focus_count} focus_time: {record.focus_time} name: {record.value_decoded_name}"`

Run: 
```
python usrasst_mon.py --format "[{record.timestamp} {record.guid}] last_execution: {record.last_execution} run_count: {record.run_count} focus_count: {record.focus_count} focus_time: {record.focus_time} name: {record.value_decoded_name}"
```