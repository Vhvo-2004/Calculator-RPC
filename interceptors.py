"""Interceptors utilitários para adicionar logs às chamadas gRPC."""

from __future__ import annotations

import logging
from typing import Callable, Optional

import grpc


class LoggingServerInterceptor(grpc.ServerInterceptor):
    """Interceptor de servidor que registra o ciclo completo de cada chamada."""

    def intercept_service(  # type: ignore[override]
        self,
        continuation: Callable[[grpc.HandlerCallDetails], Optional[grpc.RpcMethodHandler]],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Optional[grpc.RpcMethodHandler]:
        method = handler_call_details.method
        logging.info("[SERVER] Chamado método %s", method)

        handler = continuation(handler_call_details)
        if handler is None:
            logging.warning("[SERVER] Nenhum handler encontrado para %s", method)
            return None

        if handler.unary_unary:

            def logging_unary_unary(request, context):
                logging.debug("[SERVER] Payload recebido: %s", request)
                response = handler.unary_unary(request, context)
                logging.debug("[SERVER] Payload de resposta: %s", response)
                return response

            return grpc.unary_unary_rpc_method_handler(
                logging_unary_unary,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        return handler


class LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    """Interceptor de cliente que registra requisições e respostas."""

    def intercept_unary_unary(  # type: ignore[override]
        self,
        continuation: Callable[[grpc.ClientCallDetails, object], grpc.Call],
        client_call_details: grpc.ClientCallDetails,
        request: object,
    ) -> grpc.Call:
        logging.info("[CLIENT] Chamando método %s", client_call_details.method)
        logging.debug("[CLIENT] Payload enviado: %s", request)

        response = continuation(client_call_details, request)

        def _on_finish(call_future: grpc.Call):
            try:
                result = call_future.result()
                logging.debug("[CLIENT] Payload de resposta: %s", result)
            except grpc.RpcError as exc:  # pragma: no cover - apenas log
                logging.error(
                    "[CLIENT] Erro ao executar chamada %s: %s", client_call_details.method, exc
                )

        response.add_done_callback(_on_finish)
        return response
