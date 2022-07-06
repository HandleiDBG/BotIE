
class Contribuinte:
    def __init__(self):
        self.__cnpj = ''
        self.__ie = ''
        self.__razao_social = ''
        self.__uf = ''
        self.__cod_sit = -1
        self.__desc_sit = [
            'Não habilitado como Contribuinte na UF',
            'Habilitado como contribuinte na UF',
            'Exclusão lógica do Contribuinte na UF'
        ]
        self.__situacao = ''

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, value):
        self.__cnpj = ''.join(filter(lambda _i: _i.isdigit(), value))

    @property
    def ie(self):
        return self.__ie

    @ie.setter
    def ie(self, value):
        self.__ie = value

    @property
    def razao_social(self):
        return self.__razao_social

    @razao_social.setter
    def razao_social(self, value):
        self.__razao_social = value.replace('\'', '').replace('"', '').replace(';', '')

    @property
    def uf(self):
        return self.__uf

    @uf.setter
    def uf(self, value):
        self.__uf = value

    @property
    def cod_sit(self):
        return self.__cod_sit

    @cod_sit.setter
    def cod_sit(self, value):
        self.__cod_sit = value

    @property
    def situacao(self):
        return self.__situacao

    @situacao.setter
    def situacao(self, value):
        self.__situacao = value
        self.cod_sit = self.__desc_sit.index(value)
