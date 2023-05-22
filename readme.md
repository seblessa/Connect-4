# Sumário

Aplicação python da nossa implementação do jogo 4 em linha.
Modos de jogo disponíveis:
- Player vs Player
- Player vs Algoritmo
- Algoritmo vs Algoritmo



**Autores**:
- [Sebastião Santos Lessa](https://github.com/seblessa/)
- [Margarida Vila Chã](https://github.com/margaridavc/)


# Versões

As versoes dos sistemas operativos usados para desenvolver e testar esta aplicação são:
- Fedora 37
- macOS Ventura 13.1

A versões do python testadas são:
- 3.10.6
- 3.11.2


# Requirements
   ```bash
   $ pip3 install -r requirements.txt
   ```


# Execução

- Para correr o jogo no modo `player vs player` é necessario executar:


```bash
python3 main.py
```


- Para correr o jogo no modo `player vs algoritmo` é necessario executar:

Exemplo:
```bash
python3 main.py miniMax
```



- Para correr o jogo no modo `algoritmo vs algoritmo` é necessario executar:

Exemplo:
```bash
python3 main.py alphaBeta miniMax
```

Os algorítmos disponíveis são:


```
miniMax
alphaBeta
monteCarlo
```

Importante: No modo `algoritmo vs algoritmo` é necessário passar dois algorítmos diferentes como argumentos.

<br/>

Possíveis argumentos:

- (--terminal/-t), o jogo realiza-se no terminal

