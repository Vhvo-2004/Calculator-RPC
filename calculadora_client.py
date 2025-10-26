# Dupla: Diogo Gomes, Vitor Hugo
# Fonte: https://medium.com/@studymattersinlife/building-a-simple-grpc-calculator-service-in-python-6c9a7fd33f34

import grpc
import calculadora_pb2
import calculadora_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculadora_pb2_grpc.CalculadoraStub(channel)

        while True:
            valor1 = float(input("\nInforme o valor 1: "))
            valor2 = float(input("Informe o valor 2: "))
            op = input("Informe a operação ([+] add; [-] sub; [*] mul; [/] div) ou digite 'sair' para sair: ")

            try:
                if op == '+':
                    print(f"Resultado {stub.Add(calculadora_pb2.Valores(valor1=valor1, valor2=valor2)).result}\n")
                elif op == '-':
                    print(f"Resultado {stub.Sub(calculadora_pb2.Valores(valor1=valor1, valor2=valor2)).result}\n")
                elif op == '*':
                    print(f"Resultado {stub.Mul(calculadora_pb2.Valores(valor1=valor1, valor2=valor2)).result}\n")
                elif op == '/':
                    print(f"Resultado {stub.Div(calculadora_pb2.Valores(valor1=valor1, valor2=valor2)).result}\n")
                elif op == 'sair':
                    break
                else:
                    print(f"Operador inválido")
            
            except grpc.RpcError as e:
                print(f"\nErro gRPC: {e.code().name} - {e.details()}")
            
            encerrar = input("Deseja encerrar [s/n]: ")
            if encerrar == 's':
                break


if __name__=='__main__':
    run()