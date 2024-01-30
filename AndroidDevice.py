from colorama import Fore, Style


class AndroidDevice(object):
    def __init__(self, serial, product=None, model=None, device=None, transport=None):

        self.serial = serial
        self.product = product
        self.model = model
        self.device = device
        self.transport = transport

        self.adb_cmd = ['adb']
        if self.serial is not None:
            self.adb_cmd.extend(['-s', serial])
        if self.product is not None:
            self.adb_cmd.extend(['-p', product])
        self._linesep = None
        self._features = None

    def print(self, count):
        len0 = 2 * 2 - len(self.product) + len("product")
        len1 = 2 * 2 - len(self.model) + len("model")
        len2 = 2 * 3 - len(self.device) + len("device")
        len3 = 2 * 3 - len(self.transport) + len("transport_id")
        print(Fore.RED + "{:-2d}".format(count) + Style.RESET_ALL, len0 * ' ', self.product, len1 * ' ', self.model, len2 * ' ', self.device, len3 * ' ', self.transport, Style.RESET_ALL)
        return
