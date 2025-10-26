# Dupla: Diogo Gomes, Vitor Hugo
# Fonte: https://medium.com/@studymattersinlife/building-a-simple-grpc-calculator-service-in-python-6c9a7fd33f34

import grpc
import calculadora_pb2
import calculadora_pb2_grpc
from concurrent import futures


class CalculadoraService(calculadora_pb2_grpc.CalculadoraServicer):
    def Add(self, request, context):
        print(f"\nCliente solicitou a operação de adição com os números {request.valor1} e {request.valor2}")
        result = request.valor1 + request.valor2
        return calculadora_pb2.Resposta(result=result)
    
    def Sub(self, request, context):
        print(f"\nCliente solicitou a operação de subtração com os números {request.valor1} e {request.valor2}")
        result = request.valor1 - request.valor2
        return calculadora_pb2.Resposta(result=result)
    
    def Mul(self, request, context):
        print(f"\nCliente solicitou a operação de multiplicação com os números {request.valor1} e {request.valor2}")
        result = request.valor1 * request.valor2
        return calculadora_pb2.Resposta(result=result)
    
    def Div(self, request, context):
        print(f"\nCliente solicitou a operação de divisão com os números {request.valor1} e {request.valor2}")
        if request.valor2 == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Divisão por zero não é permitida")
            return calculadora_pb2.Resposta(result=0)

        result = request.valor1 / request.valor2
        return calculadora_pb2.Resposta(result=result)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculadora_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server iniciado, escutando na porta " + port)
    server.wait_for_termination()


if __name__=='__main__':
    serve()