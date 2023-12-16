import json


class Slavyanin:
    name = 'рус'
    yo = 100
    adress = 'Русь'

    def to_json(self):
        data = ('{' + f'"name": "{getattr(self, "name")}", "yo": {getattr(self, "yo")}, "address": "{getattr(self, "adress")}"' + '}')
        return json.loads(data)
        # по аналогии с generate_serialization_code,
        # где не нужно указывать обьект в to_json(),
        # но тогда в generate_serialization_code не будет смысла
        # return json.loads(str({key: getattr(self, key) for key in list(filter((lambda x: not '_' in x), dir(self)))}).replace("'", '"'))


def generate_serialization_code(clas):
    return type('DrevniiSlavyanin', (clas, ),
                {'to_json': lambda self: {key: getattr(self, key)
                                          for key in list(filter((lambda x: '_' not in x), dir(self)))}})


svarog = Slavyanin()
setattr(svarog, 'asdf', 123)
print(getattr(svarog, 'asdf'))
print(svarog.to_json())

yarilo = generate_serialization_code(Slavyanin)
setattr(yarilo, 'asdf', 123)
print(getattr(yarilo, 'asdf'))
print(yarilo.to_json(yarilo))
