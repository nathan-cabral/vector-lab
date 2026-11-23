# VECTOR LAB

Calculadora vetorial desktop em Python para estudo de vetores 2D e 3D.

## Plano de entrega

1. Núcleo matemático e testes (este pacote).
2. Explicações educativas com fórmulas, substituições e interpretação geométrica.
3. Gráficos 2D e 3D integráveis à interface.
4. Interface desktop, integração, documentação de uso e verificação final.

Cada pacote será apresentado antes de iniciar o seguinte.

## Pacote 1

`operacoes.py` implementa soma, subtração, multiplicação por escalar, módulo,
normalização, produto escalar, produto vetorial 3D, ângulo em graus e projeção
de A sobre B. Entradas devem conter 2 ou 3 números reais finitos; operações
entre dois vetores exigem dimensões iguais. Vetores nulos são aceitos quando
a operação é definida para eles.

Para criar um ambiente virtual e instalar as dependências no terminal do VS Code:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Para executar os testes:

```powershell
.venv\Scripts\python -m unittest discover -s tests -v
```

`main.py` será preenchido no pacote da interface. Este primeiro pacote ainda
não abre uma janela.
