# VECTOR LAB

Calculadora vetorial desktop em Python para estudo de vetores 2D e 3D.

## Plano de entrega

1. Núcleo matemático e testes (concluído).
2. Explicações educativas com fórmulas, substituições e interpretação geométrica (concluído).
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

## Pacote 2

`educativo.py` oferece `explicar(nome, a, b=None, escalar=None)`. A resposta
contém fórmula, substituição, desenvolvimento, resultado e significado
geométrico. `texto()` reúne as partes para a futura interface. Os nomes das
operações são os mesmos das funções em `operacoes.py`. A apresentação usa seis
algarismos significativos, sem arredondar os cálculos internos.

Exemplo no terminal:

```powershell
.venv\Scripts\python -c "from educativo import explicar; print(explicar('soma', [3, 2], [2, 4]).texto())"
```

`main.py` será preenchido no pacote da interface. Ainda não há janela gráfica.
