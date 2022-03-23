import pendulum


class GcodeParser:
    _code = None
    _parsed = []

    def __init__(self, code):
        if not isinstance(code, str):
            raise Exception("Code is not a string")

        self._code = code.split("\n")

    @property
    def get_layer_height(self):
        """
        Altura da camada padrão"""
        for line in self._code:
            if line.startswith(";Layer height: "):
                return float(line.split(" ")[-1])

    @property
    def get_filament_used(self):
        """
        Irá retornar a quantidade de filemento utilizado em metros
        """
        for line in self._code:
            if line.startswith(";Filament used: "):
                return float(line.split(" ")[-1].replace("m", ""))

    @property
    def get_time(self):
        """
        Retorna a quantidade de tempo previsto para a impressão em segundos
        """
        for line in self._code:
            if line.startswith(";TIME:"):
                return int(line.split(":")[-1])

    @property
    def get_bed_temperature(self):
        """Retorna a temperatura da mesa aquecida"""
        for line in self._code:
            if line.startswith("M140 S"):
                return int(line.split(" S")[-1])

            if line.startswith("M190 S"):
                return int(line.split(" S")[-1])

    @property
    def get_nozzle_temperature(self):
        """Retorna a temperatura do bico de impressão"""
        for line in self._code:
            if line.startswith("M104 S"):
                return int(line.split(" S")[-1])

            if line.startswith("M109 S"):
                return int(line.split(" S")[-1])

    @property
    def get_time_left(self):
        """
        Retorna uma tupla com dias, horas e minutos para imprimir o arquivo"""
        time_left = self.get_time
        if not time_left:
            return (0, 0, 0)

        zero = pendulum.from_timestamp(0)
        dt = pendulum.from_timestamp(time_left)
        diff = dt - zero

        return (diff.days, diff.hours, diff.minutes)

    def debug(self):
        print(";Layer height:", self.get_layer_height)
        print(";Filament used:", self.get_filament_used)
        print(";Time:", self.get_time)
        print("Bed Temperature:", self.get_bed_temperature)
        print("Nozzle Temperature:", self.get_nozzle_temperature)
