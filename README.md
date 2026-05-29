# DublaJá 🎬🔊

Dublagem automática de vídeos do YouTube — converta inglês para português de forma rápida e fácil!

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 O que é DublaJá?

**DublaJá** automatiza o processo completo de dublagem de vídeos YouTube:
- 📥 Baixa vídeos do YouTube
- 🎙️ Extrai e transcreve o áudio
- 🌐 Traduz para português
- 🔊 Gera áudio dublado com sintetização de voz
- 🎞️ Monta o vídeo final com áudio português

Ideal para criadores de conteúdo, educadores e qualquer um que queira tornar vídeos em inglês acessíveis em português!

---

## 🚀 Como Funciona

```
Link YouTube → Download → Transcrição (Whisper) 
   → Tradução → Síntese de Voz → Vídeo Dublado
```

**Passo a Passo:**
1. Usuário envia link do vídeo YouTube
2. Vídeo é baixado via `yt-dlp`
3. Áudio é transcrito usando **Groq Whisper API**
4. Texto é traduzido para português
5. Áudio dublado gerado com `edge-tts` ou `gTTS`
6. Vídeo final montado com `ffmpeg`

---

## 🛠️ Stack Tecnológico

| Tecnologia | Uso |
|-----------|-----|
| **Python 3.12** | Linguagem principal |
| **FastAPI** | Framework web/API |
| **Groq Whisper API** | Transcrição de áudio |
| **deep-translator** | Tradução de texto |
| **edge-tts / gTTS** | Sintetização de voz |
| **yt-dlp** | Download de vídeos YouTube |
| **ffmpeg** | Processamento de vídeo/áudio |

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)
- ffmpeg instalado no seu sistema
- Chave de API da Groq (grátis em [console.groq.com](https://console.groq.com))

**Instalar ffmpeg:**
```bash
# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg

# macOS (com Homebrew)
brew install ffmpeg

# Windows
# Baixe em: https://ffmpeg.org/download.html
```

---

## 💻 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/Navas1/dublaja.git
cd dublaja
```

### 2. Crie um ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou no Windows:
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave de API da Groq:
```env
GROQ_API_KEY=sua_chave_aqui
```

---

## 🎬 Como Usar

### Via CLI (Linha de Comando)
```bash
python main.py
```

Siga as instruções para:
1. Inserir a URL do vídeo YouTube
2. Aguardar o processamento
3. Baixar o vídeo dublado

### Via API FastAPI
```bash
python main.py
# Acesse: http://localhost:8000
```

**Exemplo de requisição:**
```bash
curl -X POST "http://localhost:8000/dublaje" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=..."}'
```

---

## 📦 COMPLEMENTO: MVP MONETIZADO & OPERAÇÃO LEAN
> *Seção opcional para validar o DublaJá como cash cow via WhatsApp + PIX. Não altera a engine principal, a stack técnica ou a rota `/dublaje` já documentadas.*

### 🔐 Fluxo de Validação (Bot + PIX)
Conecte a API existente a um ciclo de pagamento automatizado:
1. **Recebimento**: Usuário envia link do YouTube no WhatsApp do bot.
2. **Gate de Pagamento**: Bot retorna chave PIX + valor (ex: `R$ 4,90/vídeo`).
3. **Confirmação**: Webhook do gateway (Mercado Pago, Stark Bank, etc.) valida `status: paid`.
4. **Processamento**: Bot dispara `POST /dublaje` com a URL recebida.
5. **Entrega**: Arquivo em `OUTPUT_DIR` é enviado automaticamente no chat.

### ✅ Critérios Objetivos de Qualidade
Substitua avaliações subjetivas por thresholds mensuráveis antes da liberação:
| Métrica | Threshold | Ação se falhar |
|---------|-----------|----------------|
| Whisper Confidence Score | `≥ 0.85` | Revisão manual ou reembolso automático |
| Termos não traduzidos | `≤ 3/min` | Fallback para `deep-translator` com contexto forçado |
| Sincronia Áudio-Vídeo | `≤ 200ms` de desvio | Ajuste automático via `ffmpeg -itsoffset` |
| Tamanho do arquivo | `≤ MAX_VIDEO_SIZE_MB` (do `.env`) | Compressão leve: `ffmpeg -crf 28 -preset fast` |

### 🤖 Integração com a API `/dublaje`
Use a rota já existente para automação de bots/webhooks:
```bash
curl -X POST "http://localhost:8000/dublaje" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://youtube.com/watch?v=SEU_ID", "language_target": "pt"}'
```
💡 **Dica Lean**: Mantenha o bot em worker separado. A API FastAPI responde com `{"status": "processing"}` e só inicia se `GROQ_API_KEY` estiver válida e houver espaço em `OUTPUT_DIR`. Adicione fila de jobs (item do roadmap) quando ultrapassar 3 requisições simultâneas.

### 📱 Notas para VPS & Termux
- O core é compatível com Linux ARM64 (VPS low-cost ou Termux no Realme).
- Em mobile/Termux: `pkg install python ffmpeg` → rode em background com `nohup uvicorn main:app --host 0.0.0.0 --port 8000 &`
- Em VPS dedicado: use `systemd` ou `Docker` (planejado no roadmap) para reinício automático e isolamento de `GROQ_API_KEY`.
- Recomendado: ativar `MAX_VIDEO_SIZE_MB` no `.env` para evitar estouro de disco em conexões 3G/4G.

### 🔄 Instrução para Indexação
Este bloco deve ser **appendado** ao final do `README.md` existente. Não modifica pré-requisitos, estrutura de pastas, variáveis de ambiente (`GROQ_API_KEY`, `OUTPUT_DIR`, `MAX_VIDEO_SIZE_MB`, `LANGUAGE_TARGET`) nem a rota `/dublaje`. Focado exclusivamente em validação lean, gate de pagamento e métricas objetivas de entrega.

## 📁 Estrutura do Projeto

```
dublaja/
├── main.py                 # Arquivo principal
├── requirements.txt        # Dependências Python
├── .env.example           # Variáveis de ambiente (exemplo)
├── .gitignore             # Arquivos ignorados
├── README.md              # Este arquivo
└── outputs/               # Vídeos processados (gerado)
```

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` com:

```env
# Groq API
GROQ_API_KEY=seu_token_aqui

# Configurações opcionais
OUTPUT_DIR=./outputs
MAX_VIDEO_SIZE_MB=500
LANGUAGE_TARGET=pt  # Idioma alvo (português)
```

---

## 🐛 Solução de Problemas

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | Execute `pip install -r requirements.txt` |
| Erro de chave API | Verifique se `GROQ_API_KEY` está configurado no `.env` |
| FFmpeg não encontrado | Instale ffmpeg (veja pré-requisitos) |
| Vídeo muito grande | YouTube limita vídeos muito longos, tente um mais curto |

---

## 🚀 Roadmap

- [ ] Interface web (frontend)
- [ ] Suporte para múltiplos idiomas
- [ ] Fila de processamento
- [ ] Histórico de dublagens
- [ ] Melhor síntese de voz (TTS aprimorado)
- [ ] Suporte a plataformas além do YouTube
- [ ] Docker para fácil deploy

---

## 📝 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

---

## 💬 Suporte

Tem dúvidas ou encontrou um bug? 
- Abra uma [Issue](https://github.com/Navas1/dublaja/issues)
- Deixe uma discussão em [Discussions](https://github.com/Navas1/dublaja/discussions)

---

## 🌟 Mostre seu Apoio

Se gostou do projeto, não esqueça de dar uma ⭐ no repositório!

---

**Desenvolvido com ❤️ por [Navas1](https://github.com/Navas1)**
