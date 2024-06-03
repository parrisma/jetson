# Cooling Fan Control

## As Ubuntu Service

Service runs as root, so need to install python package psutil

```su root```
```pip3 install psutil```
```exit```

```cd /etc/systemd/system```
```cp ~/devroot/jetson/fan-ctrl.py ./```
```cp ~/devroot/jetson/fan-ctrl.service ./```
```sudo systemctl enable fan-ctr```
```sudo systemctl cat fan-ctrl```
```sudo systemctl status fan-ctrl```
