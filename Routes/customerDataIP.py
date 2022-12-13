


def getCustomersIP(ip,DeviceFingerprint):
    # get all Did with same IP
    Devices = DeviceFingerprint.find({"ipaddress":ip})
    