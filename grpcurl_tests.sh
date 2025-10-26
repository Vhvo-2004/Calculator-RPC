#!/usr/bin/env bash
set -euo pipefail

PROTO_FILE="calculadora.proto"
SERVICE="calculadora.Calculadora"
HOST="localhost:50051"

function call_grpc() {
  local method="$1"
  local payload="$2"
  echo "→ Executando ${method} com payload ${payload}"
  grpcurl -plaintext -import-path "." -proto "${PROTO_FILE}" -d "${payload}" "${HOST}" "${SERVICE}/${method}"
  echo
}

call_grpc Add '{"valor1": 5, "valor2": 7}'
call_grpc Sub '{"valor1": 10, "valor2": 3}'
call_grpc Mul '{"valor1": 4, "valor2": 6}'
call_grpc Div '{"valor1": 10, "valor2": 2}'

set +e
grpcurl -plaintext -import-path "." -proto "${PROTO_FILE}" -d '{"valor1": 10, "valor2": 0}' "${HOST}" "${SERVICE}/Div"
EXIT_CODE=$?
set -e

echo "Chamada de divisão por zero retornou código ${EXIT_CODE} (esperado: erro)"
