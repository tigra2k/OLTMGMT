from enum import Enum

onuDeviceIndex = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 1)  # read-only
onuName = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 2)  # read-write
onuMacAddress = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 7)  # read-only
llidONU = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 16)  # read-only
onuOperationStatus = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 8)  # read-only
onuAdminStatus = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 9)  # read-only
onuChipVendor = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 10)  # read-only
onuChipType = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 11)  # read-only
onuChipVersion = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 12)  # read-only
onuSoftwareVersion = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 13)  # read-only
onuFirmwareVersion = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 14)  # read-only
onuTestDistance = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 15)  # read-only
onuTimeSinceLastRegister = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 18)  # read-only
onuTimeLastRegister = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 29)  # read-only
resetOnu = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 1, 1, 17)  # read-write
# onu optical statistics
onuReceivedOpticalPower = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 2, 1, 4)  # read-only
onuTramsmittedOpticalPower = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 2, 1, 5)  # read-only
onuBiasCurrent = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 2, 1, 6)  # read-only
onuWorkingVoltage = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 2, 1, 7)  # read-only
onuWorkingTemperature = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 2, 1, 8)  # read-only

# system Objects 1.3.6.1.4.1.17409.2.3.1
saveConfig = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 1, 1, 14)  # read-write
saveConfigStatus = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 1, 1, 15)  # read-only

# onu Authentication PreConfig Entry 1.3.6.1.4.1.17409.2.3.4.5.2.1
onuAuthenMacAddress = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 5, 2, 1, 2)  # read-create
# onuAuthenAction = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 5, 2, 1, 3)  # read-create
onuAuthenRowStatus = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 5, 2, 1, 4)  # read-create

eponLineProfileName = (1, 3, 6, 1, 4, 1, 34592, 1, 3, 1, 1, 1, 2, 1, 1, 2)
eponSrvProfileName = (1, 3, 6, 1, 4, 1, 34592, 1, 3, 1, 1, 1, 3, 1, 1, 2)

# eponOnuAuthenticationConfigTable 1.3.6.1.4.1.34592.1.3.1.1.2.1.1.2
eponOnuAuthenLineProfileId = (1, 3, 6, 1, 4, 1, 34592, 1, 3, 1, 1, 2, 1, 1, 2, 1, 3)  # read-only
eponOnuAuthenServiceProfileId = (1, 3, 6, 1, 4, 1, 34592, 1, 3, 1, 1, 2, 1, 1, 2, 1, 4)  # read-only

onuAutoFindOnuIndex = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 6, 1, 1)
onuAutoFindMacAddress = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 6, 1, 2)
onuAutoFindTime = (1, 3, 6, 1, 4, 1, 17409, 2, 3, 4, 6, 1, 3)


# class onuAuthenActionStatus(Enum):
#     accept = 1
#     reject = 2


class RowStatus(Enum):
    active = 1
    notInService = 2
    notReady = 3
    createAndGo = 4
    createAndWait = 5
    destroy = 6


class saveConfigStatus(Enum):
    fail = 0
    success = 1
    inProcess = 2
