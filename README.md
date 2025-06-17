# 🤖 WebApp de Configuração e Automação DPE/AL

Este webapp permite que qualquer usuário configure, personalize e execute a automação dos sistemas DPE/AL de forma simples e segura, sem necessidade de conhecimentos técnicos.

## ✨ Funcionalidades

### 🔐 Segurança e Privacidade
- Armazenamento seguro de credenciais no arquivo `.env`
- Nenhum dado é enviado para a internet
- Ambiente isolado para cada usuário

### 🎯 Automação Flexível
- Escolha entre automação via URL/login/senha ou via reconhecimento de imagens
- Suporte para sistemas populares pré-configurados
- Adição de sistemas personalizados
- Configuração de ações específicas para cada etapa da automação

### 📦 Gerenciamento de Configurações
- Interface intuitiva para configuração
- Upload de imagens de referência
- Geração de pacote de instalação personalizado
- Instalador automático (.bat) incluído

## 🚀 Instalação

1. **Clone ou copie a pasta do projeto para o computador desejado**

2. **Crie e ative o ambiente virtual:**
   ```sh
   # Windows
   py -3.11 -m venv .venv
   .\.venv\Scripts\activate

   # Linux/Mac
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. **Atualize o pip:**
   ```sh
   python -m pip install --upgrade pip
   ```

4. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Instale o PyAudio (necessário para reconhecimento de voz):**
   ```sh
   pip install pipwin
   pipwin install pyaudio
   ```

## 📱 Como Usar

1. **Inicie o WebApp:**
   ```sh
   streamlit run webapp_streamlit.py
   ```

2. **Configure sua automação:**
   - Preencha seu nome e e-mail
   - Selecione os sistemas que deseja automatizar
   - Para cada sistema, escolha o método de automação:
     - **URL/Login/Senha:** Para automação via credenciais
     - **Reconhecimento de Imagens:** Para automação via cliques em elementos da tela

3. **Configure as imagens (se necessário):**
   - Use a ferramenta de captura de tela (Win + Shift + S)
   - Capture elementos importantes como:
     - Campos de login
     - Campos de senha
     - Botões
     - Menus
   - Nomeie as imagens de forma descritiva (ex: `login_gmail.png`)
   - Descreva a ação que deve ser executada após cada clique

4. **Gere o pacote de instalação:**
   - Clique em "Gerar pacote de instalação"
   - O sistema criará um arquivo .zip com:
     - Scripts de automação personalizados
     - Instalador automático (.bat)
     - Imagens de referência
     - Arquivo de instruções

5. **Instale em outro computador:**
   - Extraia o arquivo .zip
   - Execute o `install.bat`
   - Siga as instruções na tela

## 💡 Dicas e Boas Práticas

### Para Captura de Imagens
- Use a mesma resolução de tela onde a automação será executada
- Capture apenas os elementos necessários
- Evite capturar elementos que mudam frequentemente
- Use nomes descritivos para as imagens

### Para Automação
- Mantenha as janelas dos programas nas posições configuradas
- Não mova o mouse durante a automação
- Verifique se o microfone está funcionando (para comandos de voz)
- Teste a automação em um ambiente controlado primeiro

### Para Instalação
- Use Python 3.11 ou superior
- Mantenha o ambiente virtual ativado durante a instalação
- Verifique se todas as dependências foram instaladas corretamente
- Consulte o arquivo de instruções gerado para detalhes específicos

## 🔧 Solução de Problemas

### Problemas Comuns
1. **Erro ao instalar PyAudio:**
   - Use o comando `pipwin install pyaudio`
   - Se persistir, tente instalar o Visual C++ Build Tools

2. **Imagens não são reconhecidas:**
   - Verifique se a resolução da tela é a mesma
   - Recapture as imagens no computador de destino

3. **Automação não funciona:**
   - Verifique se as credenciais estão corretas
   - Confirme se as imagens estão na pasta correta
   - Verifique se o ambiente virtual está ativado

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Consulte o arquivo de instruções gerado
- Verifique a documentação do projeto
- Entre em contato com o responsável pela automação

---

Desenvolvido com ❤️ para DPE/AL 
