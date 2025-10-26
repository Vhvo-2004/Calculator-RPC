# Documentação do Projeto Calculator-RPC

## Visão geral
O Calculator-RPC é um exemplo simples de aplicação distribuída construída com **gRPC** e **Python**. O projeto expõe um serviço remoto de calculadora que oferece operações aritméticas básicas (adição, subtração, multiplicação e divisão) por meio de chamadas de procedimento remoto (RPC). O objetivo é demonstrar a estrutura mínima necessária para definir um contrato `.proto`, gerar os stubs do cliente e do servidor e implementar a comunicação entre processos.

## Componentes principais
- **`calculadora.proto`** – Define o serviço `Calculadora` com quatro métodos RPC unários e as mensagens `Valores` e `Resposta`. Esse arquivo é o contrato compartilhado entre cliente e servidor.
- **`calculadora_pb2.py` e `calculadora_pb2_grpc.py`** – Arquivos gerados automaticamente pelo `protoc` a partir do `.proto`. Eles contêm as classes de mensagens, stubs e servicers necessários para compor o RPC.
- **`interceptors.py`** – Implementa os interceptors de log `LoggingServerInterceptor` e `LoggingClientInterceptor`, responsáveis por registrar chamadas, payloads e respostas durante o ciclo de vida das requisições.
- **`calculadora_server.py`** – Implementa a classe `CalculadoraService`, que herda de `CalculadoraServicer`, fornece a lógica de negócio para cada operação matemática e inicializa o servidor gRPC escutando na porta `50051`. O servidor utiliza o `LoggingServerInterceptor` para registrar automaticamente todas as chamadas recebidas.
- **`calculadora_client.py`** – Fornece uma interface de linha de comando para o usuário. O cliente utiliza o `LoggingClientInterceptor`, garantindo a rastreabilidade das chamadas e facilitando diagnósticos durante o desenvolvimento, além de validar a entrada para impedir divisões por zero antes de enviar a requisição.
- **`tests/grpcurl_tests.sh`** – Script automatizado que utiliza `grpcurl` para validar os métodos expostos pelo serviço, incluindo o cenário de erro de divisão por zero.

## Interceptores de log
Os interceptors adicionam um nível de observabilidade às chamadas gRPC sem alterar a lógica principal do serviço ou do cliente.

- **Servidor (`LoggingServerInterceptor`)**: registrado na criação do servidor. Cada chamada tem o método e os payloads solicitados e respondidos registrados via módulo `logging`. Em casos de erros, mensagens em nível `WARNING` são emitidas.
- **Cliente (`LoggingClientInterceptor`)**: aplicado ao canal gRPC antes de criar o stub. As requisições enviadas e as respostas recebidas são logadas, e eventuais erros são registrados com nível `ERROR`.

Ambos os interceptors utilizam `logging.basicConfig` para definir formato e nível de log padrão (`INFO`), permitindo que os registros sejam facilmente direcionados para arquivo ou outras soluções de observabilidade em implantações reais.

## Fluxo de execução
1. **Definição do contrato** – As operações disponíveis são descritas no arquivo `calculadora.proto`.
2. **Geração de código** – O comando `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculadora.proto` gera os módulos Python usados por cliente e servidor.
3. **Inicialização do servidor** – Ao executar `python calculadora_server.py`, o serviço gRPC é iniciado com o interceptor de log configurado e aguarda conexões.
4. **Interação do cliente** – O cliente abre um canal interceptado (`grpc.intercept_channel`) para `localhost:50051`, cria um stub `CalculadoraStub` e invoca os métodos remotos conforme a operação selecionada pelo usuário.

## Como executar localmente
1. Crie e ative um ambiente virtual Python (opcional, porém recomendado).
2. Instale as dependências necessárias:
   ```bash
   pip install grpcio grpcio-tools grpcurl
   ```
3. Gere os arquivos de suporte a partir do `.proto` sempre que o contrato for atualizado:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculadora.proto
   ```
4. Em um terminal, inicie o servidor:
   ```bash
   python calculadora_server.py
   ```
5. Em outro terminal, execute o cliente e siga as instruções interativas:
   ```bash
   python calculadora_client.py
   ```

## Testes com grpcurl
Com o servidor em execução, o script `tests/grpcurl_tests.sh` utiliza `grpcurl` para testar todos os métodos do serviço. Ele valida operações bem-sucedidas e captura o erro esperado em uma divisão por zero:

```bash
./tests/grpcurl_tests.sh
```

Os logs gerados pelos interceptors ajudam a correlacionar as chamadas disparadas pelo script com as mensagens registradas no servidor e no cliente.

## Referências para estudo
- [Documentação oficial do gRPC](https://grpc.io/docs/) – Descrição completa da arquitetura, guias de linguagem e tutoriais.
- [gRPC Basics – Python (Google Codelabs)](https://grpc.io/docs/languages/python/basics/) – Tutorial passo a passo para criar clientes e servidores gRPC em Python.
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/) – Referência da linguagem Proto3 usada na definição das mensagens.
- [Artigo "Building a Simple gRPC Calculator Service in Python"](https://medium.com/@studymattersinlife/building-a-simple-grpc-calculator-service-in-python-6c9a7fd33f34) – Fonte original que inspirou a implementação deste projeto.
