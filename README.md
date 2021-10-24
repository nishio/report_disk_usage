# Report disk usage

It runs `df /` and report it to an webhook (such as Slack or Mattermost)

# initial settings

Make `.env`. sample:

```
URL=https://mattermost.example.com/hooks/xxxxxxxxxxxxxxxxxx
LOG=/var/log/disk_usage_log.txt
```

You may want to run this script in regular basis. Make crontab record. sample:

```
# run script on 9:00
0  9  * * * 	/opt/minecraft_server/disk_usage.py 2>&1 | logger -t disk_usage
```

`2>&1 | logger -t disk_usage` is for debug. You can see error message by doing `sudo cat /var/log/syslog | grep "disk_usage"`.

You may want to specify a python executable. Easiest way is modofy shebang. sample: `#!/home/nishio/venv/bin/python`
