#!/usr/bin/env bash
set -euo pipefail

# Script de testes utilizando grpcurl para validar o serviço de calculadora.
# O servidor precisa estar em execução antes de rodar este script.

function call_grpc() {
  local method="$1"
  local payload="$2"
  echo "Executando ${method} com payload ${payload}"
  grpcurl -plaintext -d "${payload}" localhost:50051 calculadora.Calculadora/${method}
}

call_grpc Add '{"valor1": 5, "valor2": 7}'
call_grpc Sub '{"valor1": 10, "valor2": 3}'
call_grpc Mul '{"valor1": 4, "valor2": 6}'
call_grpc Div '{"valor1": 10, "valor2": 2}'

# Exemplo de tratamento de erro
set +e
grpcurl -plaintext -d '{"valor1": 10, "valor2": 0}' localhost:50051 calculadora.Calculadora/Div
EXIT_CODE=$?
set -e

echo "Chamada de divisão por zero retornou código ${EXIT_CODE} (esperado: erro)"
