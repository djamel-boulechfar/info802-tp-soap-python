import json
import os

from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

port = int(os.environ.get('PORT', 8000))

voitures = [
    {
        "nom": "Tesla Model 3",
        "autonomie": 500,
        "tempsDeRecharge": 25
    },
    {
        "nom": "La keskia",
        "autonomie": 300,
        "tempsDeRecharge": 300
    },
    {
        "nom": "Clio 2",
        "autonomie": 50,
        "tempsDeRecharge": 600
    }
]

'''class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(self, name, times):
        for i in range(times):
            yield u'Hello, %s' % name'''


class VoituresService(ServiceBase):
    @rpc(_returns=Unicode)
    def recupererListeVoitures(self):
        return json.dumps(voitures)


application = Application([VoituresService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    # Local test
    # server = make_server('127.0.0.1', port, wsgi_application)

    # Heroku
    server = make_server('0.0.0.0', port, wsgi_application)

    print("Server running on port : " + str(port))
    server.serve_forever()
