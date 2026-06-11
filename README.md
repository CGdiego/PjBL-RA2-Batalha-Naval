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
  <a href="#-licença">Licença</a>
</p>

---

## 👥 Autores

| Nome | GitHub |
| :--- | :--- |
| **Diego Soares** | [@CGdiego](https://github.com/CGdiego) |
| **João Victor Meiners Barboza** | [@JoaoVictorMB2008](https://github.com/JoaoVictorMB2008) |
| **Lucas Maximiano Rodrigues** | [@LucasMax-Rodrigues](https://github.com/LucasMax-Rodrigues) |

---

## 📝 Sobre o Projeto

Este é um clássico jogo de **Batalha Naval** desenvolvido inteiramente em Python, utilizando matrizes bidimensionais (10 × 10) para renderizar os tabuleiros e gerenciar as mecânicas de posicionamento e ataque em turnos contra a CPU.

O projeto conta com uma interface estilizada via terminal usando títulos em ASCII art gerados pela biblioteca `pyfiglet`, efeitos sonoros via `pygame`, e um quarto modo de jogo com interface gráfica completa.

---

## 🎮 Modos de Jogo

| Modo | Descrição | Status |
| :---: | :--- | :---: |
| **1️⃣ Humano x Computador** | O modo clássico completo. Posicione 5 navios de tamanhos diferentes (do Porta-aviões ao Destroier) e tente afundar a frota da CPU. Um navio só afunda quando todas as suas partes são atingidas. | ✅ |
| **2️⃣ Simplificado** | Versão direta com 5 navios de tamanho único para partidas rápidas. | ✅ |
| **3️⃣ Caça-Água** | Modo invertido: o mapa está cheio de navios e há apenas **1 bloco de água**. O primeiro a encontrar o espaço vazio vence. | ✅ |
| **4️⃣ Batalha Aérea** | Modo com janela gráfica (Pygame). Posicione 3 aviões, escolha a direção de voo de cada um e tente abater a frota inimiga. Os aviões se movem uma casa após cada rodada. | ✅ |

---

## 🎯 Critérios de Avaliação Atendidos

* **Matrizes:** Quatro matrizes 10×10 (`real_jogador`, `vis_jogador`, `real_cpu`, `vis_cpu`) controlam o estado real e a visão de cada jogador.
* **Modularização:** Funções separadas para entrada (`escolher_linha`, `escolher_coluna`, `escolher_direcao`), renderização (`exibir_tabuleiro`) e lógica de jogo (`posicionamento_valido`, `navio_afundou`).
* **5+ embarcações:** Todos os modos posicionam no mínimo 5 peças por jogador.
* **Feedback:** Mensagens em tempo real de acerto/erro, placar de embarcações restantes, identificação de qual navio afundou e anúncio do vencedor ao final.
* **Desafio (modo 1):** Implementação completa com todas as 5 embarcações originais em tamanhos distintos, posicionamento H/V, e lógica de afundamento parcial — o navio só é contado como destruído quando todas as suas posições forem atingidas.

---

## 📄 Licença

Este projeto está sob a licença **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. O trabalho pode ser compartilhado e adaptado livremente para fins não comerciais, desde que os créditos aos autores originais sejam mantidos.