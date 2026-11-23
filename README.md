# VECTOR LAB

Calculadora vetorial desktop em Python para estudo de vetores 2D e 3D.

## Plano de entrega

1. Núcleo matemático e testes (concluído).
2. Explicações educativas com fórmulas, substituições e interpretação geométrica (concluído).
3. Gráficos 2D e 3D integráveis à interface (concluído).
4. Interface desktop, integração, documentação de uso e verificação final (concluído).

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

## Pacote 3

`graficos.py` oferece `criar_figura(nome, a, b=None, escalar=None)`, retornando
uma figura Matplotlib sem abrir outra janela. A e B têm cores distintas; o
resultado vetorial aparece em verde. Os gráficos 3D podem ser girados e
aproximados com o mouse quando incorporados à interface no pacote 4.

Para conferir um gráfico 2D antes da interface, execute:

```powershell
.venv\Scripts\python -c "from graficos import criar_figura; criar_figura('soma', [3, 2], [2, 4]).savefig('exemplo_2d.png')"
```

O arquivo `exemplo_2d.png` será criado na pasta do projeto. Pode apagá-lo após
conferir, antes de usar `git add .`.

## Pacote 4 — aplicativo desktop

Execute na pasta do projeto, pelo terminal do VS Code no Windows:

```powershell
.venv\Scripts\python main.py
```

Se ainda não criou o ambiente virtual, use os comandos de instalação acima.
Escolha 2D ou 3D, digite as coordenadas de A e B, selecione a operação e clique
em **CALCULAR**. Operações que exigem apenas A desativam B; a multiplicação por
escalar mostra o campo `k`. O produto vetorial está disponível apenas em 3D.
O painel inferior apresenta a fórmula, a substituição, as etapas, o resultado
e a interpretação geométrica. A barra sob o gráfico permite salvar a figura
e controlar a visualização; em 3D, arraste com o mouse para girar.

No gráfico 2D, arraste com o botão esquerdo para mover o plano. No 3D, o botão
esquerdo gira e o direito desloca. Em 2D e 3D, o gesto de dois dedos no touchpad
(ou a roda do mouse) aproxima e afasta. A operação Ângulo desenha a abertura e o valor em
graus no gráfico.

O aplicativo não usa internet nem banco de dados durante a execução. SymPy
poderá ser incluído futuramente se houver necessidade de cálculo simbólico;
os cálculos atuais são numéricos com NumPy.
