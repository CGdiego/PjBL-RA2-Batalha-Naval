<h1 align="center">
  <br>
  🏴‍☠️ Batalha Naval 🗺️
</h1>

<p align="center">
  <strong>Projeto Acadêmico (PjBL 02) — PUCPR (2026/1)</strong><br>
  Desenvolvido em Python para a disciplina de Raciocínio Computacional.
</p>

<p align="center">
  <a href="#-autores">Autores</a> •
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-modos-de-jogo">Modos de Jogo</a> •
  <a href="#-critérios-atendidos">Critérios</a> •
  <a href="#-ideias-para-o-futuro">Futuro</a> •
  <a href="#-licença">Licença</a>
</p>

---

## 👥 Autores

| Nome | GitHub |
| :--- | :--- |
| **Diego Soares** | [@DiegoSoares](#) |
| **João Victor Meiners Barbosa** | [@MeinersJ](#) |
| **Lucas Maximiano** | [@LucasMaximiano](#) |

---

## 📝 Sobre o Projeto

Este é um clássico jogo de **Batalha Naval** desenvolvido inteiramente em Python, utilizando matrizes bidimensionais ($10 \times 10$) para renderizar os tabuleiros e gerenciar as mecânicas de posicionamento e ataque em turnos contra a CPU. 

O projeto conta com uma interface estilizada via terminal usando títulos em ASCII art gerados pela biblioteca `pyfiglet`.

---

## 🎮 Modos de Jogo

O jogo oferece um menu interativo com diferentes dinâmicas de jogabilidade:

| Modo | Descrição | Status |
| :---: | :--- | :---: |
| **1️⃣ Humano x Computador** | O modo clássico. Você posiciona 5 navios estrategicamente e tenta afundar a frota da CPU antes que ela destrua a sua. | `W.I.P.` 🛠️ |
| **2️⃣ Simplificado** | Uma versão direta da disputa clássica para partidas rápidas e testes de mecânicas de tiro. | `Pronto` ✅ |
| **3️⃣ Caça-Água** | Um modo invertido e desafiador! O mapa está completamente tomado por embarcações ocultas e há apenas **1 bloco de água**. O objetivo é ser o primeiro a encontrar o espaço vazio. | `Pronto` ✅ |
| **4️⃣ Batalha Aérea** | Uma expansão do jogo trocando navios por aviões que se movem dinamicamente pelo mapa. | `Planejado` ⏳ |

---

## 🎯 Critérios de Avaliação Atendidos

Para garantir a nota máxima nos critérios da rubrica, o código foi estruturado com:

* **Utilização de Matrizes:** Implementação rigorosa de matrizes para os tabuleiros real e visual do jogador e da CPU.
* **Modularização (Funções):** Código limpo e sem duplicidade, dividindo as responsabilidades de entrada de dados (`escolher_linha`, `escolher_coluna`), renderização (`exibir_tabuleiro`) e lógicas de jogo.
* **Sistema de Feedback:** Mensagens claras em cores (`ANSI escape codes`) indicando se o jogador acertou o alvo ou errou, além de placar em tempo real de embarcações restantes.

---

## 🚀 Ideias para o Futuro (Backlog)

Nosso quadro de melhorias e próximas implementações inclui:
- [ ] Implementação de efeitos sonoros de explosão e splash utilizando a biblioteca `pygame`.
- [ ] Trilha sonora de fundo dinâmica durante as partidas.
- [ ] Transição visual dos tiros usando animações baseadas em emojis para simular a bomba caindo.
- [ ] Substituição completa dos caracteres convencionais `X` e `O` por emojis temáticos de explosão (💥) e água (🌊).

---

## 📄 Licença

Este projeto está sob a licença **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. Isso significa que o trabalho pode ser compartilhado e adaptado livremente, desde que para fins estritamente não comerciais e atribuindo os créditos aos autores originais.
