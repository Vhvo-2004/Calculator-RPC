# Dupla: Diogo Gomes, Vitor Hugo
# Fonte: https://medium.com/@studymattersinlife/building-a-simple-grpc-calculator-service-in-python-6c9a7fd33f34

import logging
from concurrent import futures

import grpc

import calculadora_pb2
import calculadora_pb2_grpc
from interceptors import LoggingServerInterceptor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class CalculadoraService(calculadora_pb2_grpc.CalculadoraServicer):
    def Add(self, request, context):
        logging.info(
            "Solicitação de adição: %s + %s", request.valor1, request.valor2
        )
        result = request.valor1 + request.valor2
        return calculadora_pb2.Resposta(result=result)

    def Sub(self, request, context):
        logging.info(
            "Solicitação de subtração: %s - %s", request.valor1, request.valor2
        )
        result = request.valor1 - request.valor2
        return calculadora_pb2.Resposta(result=result)

    def Mul(self, request, context):
        logging.info(
            "Solicitação de multiplicação: %s * %s", request.valor1, request.valor2
        )
        result = request.valor1 * request.valor2
        return calculadora_pb2.Resposta(result=result)

    def Div(self, request, context):
        logging.info(
            "Solicitação de divisão: %s / %s", request.valor1, request.valor2
        )
        if request.valor2 == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Divisão por zero não é permitida")
            logging.warning("Tentativa de divisão por zero detectada")
            return calculadora_pb2.Resposta(result=0)

        result = request.valor1 / request.valor2
        return calculadora_pb2.Resposta(result=result)


def serve():
    port = "50051"
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LoggingServerInterceptor()],
    )
    calculadora_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server iniciado, escutando na porta %s", port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
