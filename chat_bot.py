import openai

# Configure a chave da API do ChatGPT
openai.api_key = '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'

# Defina a mensagem que você deseja enviar ao ChatGPT
mensagem = 'Oi, ChatGPT. Qual é a previsão do tempo hoje?'

# Envie a mensagem para o ChatGPT
response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=mensagem,
  max_tokens=50  # Defina o número máximo de tokens na resposta
)

# Extraia a resposta do ChatGPT
resposta = response.choices[0].text

# Faça algo com a resposta, como enviá-la de volta para sua automação Selenium
print(resposta)